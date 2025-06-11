import dearpygui.dearpygui as dpg
from database import *

class signUpGUI:
    def __init__(self):
        self.dpg = dpg
        self.dpg.create_context()
        self.build_gui()
        self.exit_flag = False

    def build_gui(self):
        with dpg.font_registry():
            default_font = dpg.add_font(r"assets\Typographica-Blp5.ttf", 20)

        with dpg.window(label="SIGN UP" , pos=(20, 50), width = 350) as self.window:
            self.username_input = dpg.add_input_text(label="Enter  Username")
            
            self.password_input = dpg.add_input_text(label="Enter  Password", password= True)

            self.series_name_input = dpg.add_input_text(label="Name of Series")

            self.episode_input = dpg.add_input_int(label="Current Episode Number", min_value=0)

            self.submit_button = dpg.add_button(label="Submit", callback=self.credentials_entered)

        dpg.bind_font(default_font)

    
    
    
    """ 
    Callback Functions
    """

    def credentials_entered(self):
        """
        Called when submit button is pressed
        Checks for Valid Username & Password
        """

        username = dpg.get_value(self.username_input)
        password = dpg.get_value(self.password_input)
        seriesName = dpg.get_value(self.series_name_input)
        episodeNumber = dpg.get_value(self.episode_input)

        if username.strip() != "" and password.strip() != "":
            print(F"Username: {username}, Password: {password}")
            try:
                connection = connect_db("database.db")
                add_user(connection, username, password)

                
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT id FROM users WHERE username = ? AND password = ?", 
                    (username, password)
                )
                user_id = cursor.fetchone()[0]

                create_video_series_table(connection)

                series_id = add_video_series(connection, user_id, seriesName, episodeNumber)

                print(f"Inserting into settings with series_id: {series_id} (type: {type(series_id)})")


                #creating corresponding series settings table

                create_series_settings_table(connection)

                add_series_setting(connection, series_id)
                
                connection.close()
                self.exit_flag = True
                print(f"Exit Flag State: {self.exit_flag} ")

            except Exception as e:
                print(e)
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
        self.dpg.create_viewport(title='Content Buddy Sign Up', width= 425, height = 300, x_pos= 1100, y_pos= 250,)
        self.dpg.setup_dearpygui()
        self.dpg.show_viewport()
        print("RUN SIGN UP GUI STARTED")
        
        while self.dpg.is_dearpygui_running():
            if self.exit_flag:
                self.dpg.stop_dearpygui()
            self.dpg.render_dearpygui_frame()
        self.dpg.destroy_context()


if __name__ == "__main__":

        gui = signUpGUI()
        gui.run()