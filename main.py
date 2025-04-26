from obs import OBScontroller
from gui import GUI
import subprocess
import os
import time
import psutil

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

if __name__ == "__main__":
    launch_obs()
    obs = OBScontroller()
    gui = GUI(obs)
    gui.run()

    #tests
  


