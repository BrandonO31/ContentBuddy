import dearpygui.dearpygui as dpg
import database

class signUpGUI:
    def __init__(self):
        self.dpg = dpg
        self.dpg.create_context()
        self.build_gui()

    def build_gui(self):
        with dpg.font_registry():
            default_font = dpg.add_font(r"assets\Typographica-Blp5.ttf", 20)

        with dpg.window(label="SIGN UP" , pos=(20, 50), width = 350) as self.window:
            self.username_input = dpg.add_input_text(label="Enter Username")
            
            self.password_input = dpg.add_input_text(label="Enter Password", password= True)

            self.submit_button = dpg.add_button(label="Submit", callback=self.credentials_entered)

            # with dpg.group(vertical=True):
                
            
            
            
            
            

        
        # STYLING

        # with dpg.theme() as global_theme:

        #     with dpg.theme_component(dpg.mvAll):
                
            
        
        # with dpg.theme() as start_button_theme:

        #     with dpg.theme_component(dpg.mvButton):
                
        # with dpg.theme() as stop_button_theme:

        #     with dpg.theme_component(dpg.mvButton):
                

        # dpg.bind_theme(global_theme)

        # dpg.bind_item_theme(startRecButton , start_button_theme)
        # dpg.bind_item_theme(stopRecButton , stop_button_theme)

        dpg.bind_font(default_font)

    
    
    
    """ 
    Callback Functions
    """

    def credentials_entered(self):

        username = dpg.get_value(self.username_input)
        password = dpg.get_value(self.password_input)

        if username.strip() != "" and password.strip() != "":
            print(F"Username: {username}, Password: {password}")
        else:
            self.invalid_credentials()

    def invalid_credentials(self):
            
            
       
        with dpg.theme() as red_button_theme:
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 255))  # RGBA format

        
        dpg.bind_item_theme(self.submit_button, red_button_theme)

        
        if not dpg.does_item_exist("error_text"):
            dpg.add_text("Invalid Credentials, please try again.", tag="error_text", parent=self.window)

        
    def run(self):
        
        dpg.create_viewport(title='Content Buddy Sign Up', width= 400, height = 200, x_pos= 1100, y_pos= 250,)
        self.dpg.setup_dearpygui()
        self.dpg.show_viewport()
        self.dpg.start_dearpygui()
        self.dpg.destroy_context()


if __name__ == "__main__":

        gui = signUpGUI()
        gui.run()