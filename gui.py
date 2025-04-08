import dearpygui.dearpygui as dpg

dpg.create_context()




with dpg.window(label="Record", width=1000, height=1000):
    with dpg.group(horizontal=True):
        startRec = dpg.add_button(label="Start Rec" , callback=start_Rec, user_data="Fake user data")
        endRec = dpg.add_button(label="End Rec")

dpg.create_viewport(title="Content Buddy" , width=1000 , height = 200)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()