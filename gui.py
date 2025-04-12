import dearpygui.dearpygui as dpg
import obs as obs

class GUI:
    def __init__(self, obs_controller):
        self.obs = obs_controller
        self.dpg = dpg
        self.dpg.create_context()
        self.build_gui()

    def build_gui(self):
        with dpg.window(label="Content Buddy"):

            with dpg.group(horizontal=True):
                startRec = dpg.add_button(label="Start Rec" , callback=self.start_recording, user_data="Fake user data")
                endRec = dpg.add_button(label="End Rec", callback=self.stop_recording, user_data="Fake user data") 

    """
    Callback Functions
    """
    def start_recording(self): self.obs.start_recording()

    def stop_recording(self): self.obs.stop_recording()

    def run(self):
        
        dpg.create_viewport(title='Content Buddy1', width= 1000, height = 800)
        self.dpg.setup_dearpygui()
        self.dpg.show_viewport()
        self.dpg.start_dearpygui()
        self.dpg.destroy_context()