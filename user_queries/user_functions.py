#!/usr/bin/env python3

# Imports
from mysql.connector import connect, Error

# Globals
USER_TABLE = 'Users' 

# Functions
def add_user_to_Users(connection, username, name, email):

    # Define the Query
    mysql_user_insert_query = f'''
        INSERT INTO {USER_TABLE} (id, name, email)
        VALUES ({username}, '{name}', '{email}')
    '''

    # Check if user already in Users, but check is done internally so we're good

    # Execute Query using Cursor
    cursor = connection.cursor()
    cursor.execute(mysql_user_insert_query)
    connection.commit()

    # Close cursor
    cursor.close()

# Main Execution
def main():
    try:
        with connect(host="localhost", user="bgoodwin", password="pwpwpwpw", database="bgoodwin") as connection:
            # Do Stuff

            # TODO: Get these values from Google Sign in!! (we wanna execute this anytime someone signs in)
            add_user_to_Users(connection, 29492, 'Jean Francois Boueri', 'jbueri@nd.edu')

    except Error as e:
        print(e)

if __name__ == '__main__':
    main()
