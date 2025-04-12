from obsws_python import ReqClient
from pathlib import Path



class OBScontroller:
    def __init__(self):
        """Initializes instance of OBS controller
        ReqClient auto detects config.toml in same dir as main.py ow fill in params
        """
        project_root = Path().resolve()
        config_path = project_root / "config.toml"

        if config_path.exists():
            self.client = ReqClient()
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
            print("Connection established from newly created config")
    
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



