#!/usr/bin/env python3

from getpass import getpass
from mysql.connector import connect, Error

# info from google sign in
# unique_id = userinfo_response.json()["sub"]
# users_email = userinfo_response.json()["email"]
# users_name = userinfo_response.json()["given_name"]
create_users_table_query = """
CREATE TABLE users(
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)
"""

def show_tables(connection):
    users_query = "DESCRIBE users"
    
    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)

def top_5(connection):
    users_query = "SELECT * FROM users LIMIT 5"
    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)


def insert_user(connection, usrid, name, email): 
    insert_users_query = """
    INSERT INTO users
        (id, name, email)
        VALUES ( %s, %s, %s )
    """
    user = [(usrid, name, email)]
    with connection.cursor() as cursor:
        cursor.executemany(insert_users_query, user)
        connection.commit()

def main():
    
    # try to connect to SQL server and print current tables
    try:
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "),
            database="bgoodwin",
        ) as connection:
            print(connection)
            show_tables(connection)
            #insert_user(connection, 12345, "Bridget Goodwine", "bgoodwin@nd.edu")
            top_5(connection)
    except Error as e:
        print(e)

if __name__ == "__main__":
    main()
