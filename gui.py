import dearpygui.dearpygui as dpg
import obs as obs
import threading
import time
from automation import open_chess_website
from database import *
from AppState import AppState


class GUI:
    def __init__(self, obs_controller, app_state):
        self.obs = obs_controller
        self.state = app_state
        self.dpg = dpg
        self.dpg.create_context()
        self.build_gui()

    def build_gui(self):
        
        with dpg.font_registry():
            default_font = dpg.add_font("assets\Typographica-Blp5.ttf", 30)

        with dpg.window(label="Chess Videos", pos=(0, 0), height=300,  width=250):

            with dpg.group(horizontal=True):
                startRecButton = dpg.add_button(label="Start Rec" , callback=self.start_recording, user_data="Fake user data")
                stopRecButton = dpg.add_button(label="Stop Rec", callback=self.stop_recording, user_data="Fake user data") 
            
            dpg.add_button(label="Open Chess.com", callback = open_chess_website)
            
            ep_num = self.state.get_episode()
            dpg.add_text(f"Current Episode #: {ep_num}", tag="episode_counter")


            dpg.add_text(tag="countdown_text")

                    # Toggle button to show/hide settings
            dpg.add_spacer(height=10)

            with dpg.collapsing_header(label="⚙️ Settings", default_open=False):

                # Dummy Field 1
                dpg.add_input_text(label="Main Recording Scene", tag="main_rec_scene")
                dpg.add_button(label="Submit", callback=lambda: print("Setting 1:", dpg.get_value("Recording Sce")))

                # Dummy Field 2
                dpg.add_input_text(label="Thumbnail Scene", tag="thumbnail_scene")
                dpg.add_button(label="Submit", callback=lambda: print("Setting 2:", dpg.get_value("setting_2_input")))

                # Dummy Field 3
                dpg.add_input_text(label="Setting 3", tag="setting_3_input")
                dpg.add_button(label="Submit Setting 3", callback=lambda: print("Setting 3:", dpg.get_value("setting_3_input")))


        
        # STYLING

        with dpg.theme() as global_theme:

            with dpg.theme_component(dpg.mvAll):
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 0, 0), category=dpg.mvThemeCat_Core)
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 1, category=dpg.mvThemeCat_Core)
            
        
        with dpg.theme() as start_button_theme:

            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (34, 177, 76), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (28, 151, 64), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (23, 124, 53), category=dpg.mvThemeCat_Core)
        
        with dpg.theme() as stop_button_theme:

            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (204, 51, 51), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (179, 45, 45), category=dpg.mvThemeCat_Core)
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (153, 40, 40), category=dpg.mvThemeCat_Core)

        dpg.bind_theme(global_theme)

        dpg.bind_item_theme(startRecButton , start_button_theme)
        dpg.bind_item_theme(stopRecButton , stop_button_theme)

        dpg.bind_font(default_font)

        
    
    """
    Callback Functions
    """
    def start_recording(self): 
        threading.Thread(target=self.countdown_and_start, args=(3,)).start()
        # self.obs.start_recording()

    def stop_recording(self): 
        self.update_episode_number()
        ep_num = self.state.get_episode()
        print(f"Stop Recording Button clicked. Current Episode number is: {ep_num}")
        self.obs.stop_recording()
        

    def update_episode_number(self): 
        ep_num = self.state.get_episode()
        dpg.set_value("episode_counter", f"Current Episode #: {ep_num}")



    
    def countdown_and_start(self, count: int):
        while count > 0:
            dpg.set_value("countdown_text", f"Starting in {count}")
            dpg.render_dearpygui_frame()  # Refresh the GUI
            time.sleep(1)  # Wait for 1 second
            count -= 1
        dpg.set_value("countdown_text", "Recording started!")
        self.obs.start_recording()
        

    def run(self):
    
        dpg.create_viewport(title='Content Buddy', width= 275, height = 400, x_pos= 1100, y_pos= 250)
        self.dpg.setup_dearpygui()
        self.dpg.show_viewport()
        self.dpg.start_dearpygui()
        self.dpg.destroy_context()