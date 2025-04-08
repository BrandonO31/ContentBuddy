import obsws_python as obs


#using config.toml which provides host & pswd
cl = obs.ReqClient()

def start_rec_callback(sender, app_data, user_data):
    try:
        cl.start_record()
    except Exception as e:
        print(F"Failed to start recording: {e}")


#cl.stop_record()