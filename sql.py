#!/usr/bin/env python3

from getpass import getpass
from mysql.connector import connect, Error

# query to create users table w/ info from google sign in
create_users_table_query = """
CREATE TABLE users(
    id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100)
)
"""

# show schema of users table
def show_tables(connection):
    users_query = "DESCRIBE users"

    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)


# show data in users table
def show_users(connection):
    users_query = "SELECT * FROM users LIMIT 5"

    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)


# insert user into users table
def insert_user(connection, usrid, name, email):
    # TODO: print into single string, this is a method for many insertions
    insert_users_query = """
    INSERT INTO users
        (id, name, email)
        VALUES ( %s, %s, %s )
    """
    user = [(usrid, name, email)]

    with connection.cursor() as cursor:
        cursor.executemany(insert_users_query, user)
        connection.commit()


# just for manual testing right now
def main():
    # try to connect to SQL server w/ input user & password
    # to use current database: bgoodwin & pwpwpwpw
    try:
        with connect(
            host="localhost",
            #user=input("Enter username: "),
            user="bgoodwin",
            #password=getpass("Enter password: "),
            password="pwpwpwpw",
            database="bgoodwin",
        ) as connection:
            print(connection)
            show_tables(connection)
            show_users(connection)

    except Error as e:
        print(e)


if __name__ == "__main__":
    main()
