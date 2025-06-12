from obs import OBScontroller
from gui import GUI
from sign_up_GUI import signUpGUI
from database import *
from AppState import *
import subprocess
import os
import time
import psutil
import socket
import threading
import queue


def is_obs_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and "obs64.exe" in proc.info['name']:
            return True
    return False

def launch_obs():
    obs_path = r"C:\Program Files\obs-studio\bin\64bit\obs64.exe"
    if not is_obs_running():
        obs_dir = os.path.dirname(obs_path)
        subprocess.Popen([obs_path], cwd=obs_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    while not is_obs_running():
        time.sleep(0.5)
        print("OBS is opening...")
    


def is_obs_websocket_ready(host="localhost", port=4455):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.settimeout(1)
            s.connect((host, port))
            return True
        except (ConnectionRefusedError, socket.timeout):
            return False

def await_obs_initialization():
    max_retries = 10
    for _ in range(max_retries):
        try:
            scenes = obs.get_all_scenes()
            print(scenes)
            break
        except Exception as e:
            print(f"OBS not ready yet, standby")
            time.sleep(1)

if __name__ == "__main__":

    DB_PATH = "database.db"
    app_state = AppState(db_path=DB_PATH)

    with connect_db(DB_PATH) as connection:
        create_user_table(connection)
    
    
        if not user_exists(connection):
            print("No user found. Proceeding to sign-up...")
            signUpPrompt = signUpGUI(app_state)
            signUpPrompt.run()  
            
    connection.close()  
        
    with connect_db(DB_PATH) as connection:
        print("Now Launching OBS and Main UI")
        
        if user_exists(connection):

            
            launch_obs()  
            
            while not is_obs_websocket_ready():
                print("Waiting for OBS WebSocket to be ready...")
                time.sleep(1)
            obs = OBScontroller(app_state)
            await_obs_initialization() 
            gui = GUI(obs, app_state)
            
            gui.run()


