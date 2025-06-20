import cv2  
import numpy as np
from obsws_python import ReqClient
from obsws_python import EventClient
from pathlib import Path
import time
from automation import upload_image_to_imgur, automate_thumbnail_with_photopea
from database import *
from AppState import AppState



class OBScontroller:
    def __init__(self, app_state):
        """Initializes instance of OBS controller
        ReqClient auto detects config.toml in same dir as main.py o.w. creates file & user must manually add password
        EventClient also
        """

        #Global Variables
        self.state = app_state
        
        project_root = Path().resolve()
        config_path = project_root / "config.toml"

        if config_path.exists():
            self.client = ReqClient()
            self.clientEv = EventClient()
            print("Connection established from existing config")

        # apparently there's a toml library so look into using that but for now this works 
        else:
            config_template = """
            [connection]
            host = "localhost"
            port = 4455
            password = "___"
            """
            config_path.write_text(config_template)
            print("New Config File created, please enter your password into it, then re-run program")


        #Tracking states
        self.is_recording = False
        self.last_recording_path = None

        #Registering Events
        self.clientEv.callback.register(self.on_record_state_changed)


            
    
    def start_recording(self):
        """
        Start OBS recording 
        """

        try:
            response = self.state.get_scene_by_scenario("main_scene")
            print(f"The scene obtained for recording is: {response}", type(response))
            self.set_scene(response)

            self.client.start_record()

        except Exception as e:
            print(f"[OBSController] failed to stop recording: {e}")

    def stop_recording(self):
        """
        Stop OBS recording; all processes after recording is stopped are called here as well
        """

        try:
            self.client.stop_record()
            

        except Exception as e:
            print(f"[OBSController] failed to stop recording: {e}")

        
        self.video_file_handler()

    
    def on_record_state_changed(self, data):
        """
        outputActive	Boolean	Whether the output is active
        outputState	String	The specific state of the output
        outputPath	String	File name for the saved recording, if record stopped. null otherwise
        """

        self.last_recording_path = data.output_path
        self.is_recording = data.output_active

        print("AM I CURRENTLY RECORDING??", self.is_recording)

    
    def video_file_handler(self):
        """
        Rename most recent filepath OBS creates to proper naming scheme.
        Try-Except block bypasses windows/obs file locking, ensuring file renames after windwows/obs is done with it

        """

        retries = 10
        delay = 0.5

        # give the program a chance to get the recording path
        while not self.last_recording_path and retries > 0:
            time.sleep(delay)
            retries -= 1

        if not self.last_recording_path:
            print("Recording path not set — cannot rename file.")
            return

        old = Path(self.last_recording_path)
        new = old.with_name(self.state.get_next_episode_filename())

        for _ in range(5):
            try:
                old.rename(new)
                print(f"Renamed to {new}")
                self.state.increment_episode()
                break
            except Exception as e:
                print(f"Rename failed: {e}")
                time.sleep(0.5)
            

        print("File Renaming Method Called")

        self.thumbnail_creation_process()


    
    def thumbnail_creation_process(self):
        """
        Starts 10s thumbnail face recording, gets best frame, and saves 
        """

        print("Starting thumbnail face capture!")
        response = self.state.get_scene_by_scenario("thumbnail_scene")
        print(f"The scene obtained for recording is: {response}", type(response))
        self.set_scene(response)
        time.sleep(2)
        self.client.start_record()
        time.sleep(6)
        self.client.stop_record()

        time.sleep(2)

        ep_num_temp = self.state.get_episode()
        ep_num_temp -= 1

        face_vid_path = Path(self.last_recording_path).with_name(
            f"ep{ep_num_temp}_face.mkv"
        )
        
        for _ in range(5):
            try:
                Path(self.last_recording_path).rename(face_vid_path)
                print(f"Thumbnail face video saved as {face_vid_path}")
                self.extract_best_frame(face_vid_path)
                break
            except Exception as e:
                print(f"Rename failed: {e}")
                time.sleep(0.5)
        
        
            
    
    def extract_best_frame(self, video_path):
        """
        Extract sharpest frame using Laplacian variance
        """

        ep_num_temp = self.state.get_episode()
        ep_num_temp -= 1

        cap = cv2.VideoCapture(str(video_path))
        best_frame = None
        best_focus = 0
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            focus = cv2.Laplacian(gray, cv2.CV_64F).var()

            if focus > best_focus:
                best_focus = focus
                best_frame = frame

            frame_count += 1
        
        cap.release()

        if best_frame is not None:
            output_path = Path("Screenshots") / f"ep{ep_num_temp}_face_frame.png"
            output_path.parent.mkdir(exist_ok=True)
            cv2.imwrite(str(output_path), best_frame)
            print(f"Best thumbnail frame saved to {output_path}")
            upload_image_to_imgur(output_path)
            time.sleep(1)
            automate_thumbnail_with_photopea(output_path, ep_num_temp)
            
        
        else:
            print("No frame extracted")
        

            

    def get_all_scenes(self):
        scenes = self.client.get_scene_list()
        scene_names = [scenes['sceneName'] for scenes in scenes.scenes]

        return scene_names
    
    def set_scene(self, scene_name):

        self.client.set_current_program_scene(scene_name)


    
        



    



