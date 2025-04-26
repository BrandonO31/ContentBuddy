import sqlite3

def get_connection(db_name):
    try:
        return sqlite3.connect(db_name)
    except Exception as e:
        print (f"Error: {e}")
        raise

def create_table(connection):
    query = """
    
    """

    try:
        connection.execute(query)
        print("Table 'users' created / already exists")

    except Exception as e:
        print(f"Error creating table: {e}")

def insert_user(connection, username:str, age:int, email: str):
    query = ""

    try:
        with connection:
            
            print(f"User: {username} was added to database!!")
    except Exception as e:
        print(e)
            
    


    


def main():
    connection = get_connection("database.db")

    try:
        create_table(connection)

        start = input("Enter Option (Add, Delete, Update, Search, Add Many):").lower()
        

    finally:
        connection.close()
        

if __name__ =="__main__":
        main()