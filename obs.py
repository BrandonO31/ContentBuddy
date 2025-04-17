from obsws_python import ReqClient
from obsws_python import EventClient
from pathlib import Path
import time



class OBScontroller:
    def __init__(self):
        """Initializes instance of OBS controller
        ReqClient auto detects config.toml in same dir as main.py o.w. creates file & user must manually add password
        EventClient also
        """
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
            self.client.start_record()

        except Exception as e:
            print(f"[OBSController] failed to stop recording: {e}")

    def stop_recording(self):
        """
        Stop OBS recording 
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
        Rename most recent filepath OBS creates to customName.
        Try-Except block bypasses windows/obs file locking, ensuring file renames after windwows/obs is done with it

        """
        old = Path(self.last_recording_path)
        new = old.with_name("RoadTo2000Eloep##.mkv")

        retries = 10
        delay = 0.5

        for _ in range(retries):
            try:
                old.rename(new)

            except Exception as e:
                print(e)
                time.sleep(delay)
        

        print("File Renaming Method Called")

        pass



    



