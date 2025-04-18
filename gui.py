import dearpygui.dearpygui as dpg
import obs as obs
import threading
import time
from automation import open_chess_website

class GUI:
    def __init__(self, obs_controller):
        self.obs = obs_controller
        self.dpg = dpg
        self.dpg.create_context()
        self.build_gui()

    def build_gui(self):
        
        with dpg.font_registry():
            default_font = dpg.add_font("assets\Typographica-Blp5.ttf", 20)

        with dpg.window(label="Chess Videos" , pos=(35, 50)):

            with dpg.group(horizontal=True):
                startRecButton = dpg.add_button(label="Start Rec" , callback=self.start_recording, user_data="Fake user data")
                stopRecButton = dpg.add_button(label="Stop Rec", callback=self.stop_recording, user_data="Fake user data") 
            
            dpg.add_button(label="Open Chess.com", callback = open_chess_website)
            
            dpg.add_text(f"Chess Video Ep#:", tag="episode_counter")
            dpg.add_text(tag="countdown_text")

        
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
        self.obs.stop_recording()
        self.update_episode_number()

    def update_episode_number(self): 
        
        episode_num = self.obs.get_episode_number()
        dpg.set_value("episode_counter" , f"Chess Video Ep#: {episode_num}")

    
    def countdown_and_start(self, count: int):
        while count > 0:
            dpg.set_value("countdown_text", f"Starting in {count}")
            dpg.render_dearpygui_frame()  # Refresh the GUI
            time.sleep(1)  # Wait for 1 second
            count -= 1
        dpg.set_value("countdown_text", "Recording started!")
        self.obs.start_recording()
        

    def run(self):
        
        dpg.create_viewport(title='Content Buddy', width= 250, height = 200)
        self.dpg.setup_dearpygui()
        self.dpg.show_viewport()
        self.dpg.start_dearpygui()
        self.dpg.destroy_context()