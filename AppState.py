from database import *

class AppState:
    def __init__(self, db_path="database.db", user_id=1, series_id=1): # user_id, series_id = 1 b/c i only have 1 user and series for now
        self.db_path = db_path
        self.user_id = user_id
        self.series_id = series_id

    def get_episode(self):
        conn = connect_db(self.db_path)
        ep = get_latest_episode_by_user(conn, self.user_id)
        conn.close()
        return ep

    def increment_episode(self):
        conn = connect_db(self.db_path)
        increment_episode_number_for_user(conn, self.user_id)
        conn.close()

    def get_next_episode_filename(self):
        ep = self.get_episode()
        return f"RoadTo2000Eloep{ep}.mkv"
    
    def get_scene_by_scenario(self, key):
        conn = connect_db(self.db_path)
        result = get_series_setting(conn, self.series_id, key)

        return result
