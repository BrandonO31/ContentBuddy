import sqlite3

def connect_db(db_name):
    """
    Returns connection object to interac w/ DB
    """
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f"Error: {e}")
        raise

    
# User Functions
def create_user_table(connection):
    
    """
    Creates table for User
    """

    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
        print("User Table was created!")
    except Exception as e:
        print(f"User Table NOT created: {e}")
    pass

def user_exists(connection):
    """
    Checks if a user exists in database.
    Returns True is user exists, False o.w
    """
    query = "SELECT COUNT(*) FROM users"
    
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
            result = cursor.fetchone()
            return result[0] > 0  # Returns True if count > 0, indicating users exist
    except Exception as e:
        print(f"Error checking user existence: {e}")
        return False

def add_user(connection, username:str, password:str):
    query = "INSERT INTO users (username, password) VALUES (?, ?)"

    #LOGIC FOR VALID USERNAME & PASSWORD ...

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (username, password))
        print(f"User: {username} has been added to the database!")
    except Exception as e:
        print(e)


# Video Series functions -------------------------------------------------------------------------------------

def create_video_series_table(connection):
    """
    Creates table for Video Series
    """

    query = """
    CREATE TABLE IF NOT EXISTS series (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        seriesName TEXT NOT NULL,
        episodeNumber INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
        print("User Table was created!")
    except Exception as e:
        print(f"User Table NOT created: {e}")



def add_video_series(connection, user_id:int, seriesName:str, episodeNum:str):
    query = "INSERT INTO series (user_id, seriesName, episodeNumber) VALUES (?, ?, ?)"

    #LOGIC FOR VALID USERNAME & PASSWORD ...

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id, seriesName, episodeNum))
            return cursor.lastrowid
        print(f"Series: {seriesName} has been added to the database!")
    except Exception as e:
        print(e)

def get_series_names_by_user(connection, user_id):
    """
    Returns a list of series names for the given user ID.
    """
    query = "SELECT seriesName FROM series WHERE user_id = ?"
    
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            results = cursor.fetchall()
            return [row[0] for row in results]  # Extract just the names
    except Exception as e:
        print(f"Error fetching series names: {e}")
        return []

def get_latest_episode_by_user(connection, user_id):
    """
    Gets the latest episode number for the given user.
    Assumes only one series per user.
    """
    query = "SELECT episodeNumber FROM series WHERE user_id = ? LIMIT 1"

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0
    except Exception as e:
        print(f"Error fetching episode number: {e}")
        return 0


def increment_episode_number_for_user(connection, user_id):
    """
    Increments the episode number by 1 for the user's video series.
    Assumes each user has only one video series.
    """
    query = "UPDATE series SET episodeNumber = episodeNumber + 1 WHERE user_id = ?"

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            
            print(f"Episode number incremented for user_id: {user_id}")
    except Exception as e:
        print(f"Failed to increment episode number: {e}")



# User Settings Functions --------------------------------------------------------------------------------------------------------------------------------

def create_series_settings_table(connection):
    """
    Creates table for User Settings
    """

    query = """
    CREATE TABLE IF NOT EXISTS series_settings (
        id INTEGER PRIMARY KEY,
        series_id INTEGER,
        main_scene TEXT,
        thumbnail_scene TEXT,
        file_name TEXT,
        FOREIGN KEY(series_id) REFERENCES series(id) ON DELETE CASCADE
    )
    """
    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query)
        print("Series Settings Table was created!")
    except Exception as e:
        print(f"User Table NOT created: {e}")



def add_series_setting(connection, series_id:int,):
    query = "INSERT INTO series_settings (series_id) VALUES (?)"

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (series_id,))
        print(f"Series Setting Table has been added for the following series: {series_id}")
    except Exception as e:
        print(f"Error in add_series_setting: {e}")


def main():
    connection = connect_db("database.db")

    try:
        

        userInput = input("Enter Option (Add, Delete, Update, Search, Add Many):").lower()

        if userInput == "add":
            username = input("Enter a Username: ")
            password = input("Enter a Password: ")

            try:
                add_user(connection, username, password)
            except Exception as e:
                print(f"User NOT added!: {e}")
        

    finally:
        connection.close()
        

if __name__ =="__main__":
        main()