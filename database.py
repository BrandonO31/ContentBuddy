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

    

def create_user_table(connection):
    
    """
    Creates table for User
    """

    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL UNIQUE
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
    

def initialize_db():
    """
    Function to be used elsewhere in program to initialize a connection with the DB & do whatever
    """
    pass

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

    

def get_user_by_username(username):
    pass

def verify_user_login(username, password):
    pass


# Start of Video Series functions -------------------------------------------------------------------------------------


def add_video_series(connection, user_id:int, seriesName:str, episodeNum:str):
    query = "INSERT INTO series (user_id, seriesName, episodeNumber) VALUES (?, ?, ?)"

    #LOGIC FOR VALID USERNAME & PASSWORD ...

    try:
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id, seriesName, episodeNum))
        print(f"Series: {seriesName} has been added to the database!")
    except Exception as e:
        print(e)

def get_series_by_user(user_id):
    pass

def update_episode_number(series_id, new_episode_number):
    pass

            
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