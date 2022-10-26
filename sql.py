#!/usr/bin/env python3

from getpass import getpass
from mysql.connector import connect, Error

# saved: creation queries for all tables
create_users_table_query = """
CREATE TABLE Users(
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL
)
"""

create_orders_table_query = """
CREATE TABLE Orders(
    id INT AUTO_INCREMENT PRIMARY KEY,
    dropoff VARCHAR(100) NOT NULL,
    pickup VARCHAR(100) NOT NULL,
    tip FLOAT NOT NULL,
    deliverer_id_fk INT,
    orderer_id_fk INT NOT NULL,
    waiting_for_pickup INT DEFAULT 1,
    time_estimate DATETIME NOT NULL,
    FOREIGN KEY(deliverer_id_fk) REFERENCES Users(id),
    FOREIGN KEY(orderer_id_fk) REFERENCES Users(id)
)
"""

# old orders = orders but do not include status elements
create_oldorders_table_query = """
CREATE TABLE OldOrders(
    id INT AUTO_INCREMENT PRIMARY KEY,
    dropoff VARCHAR(100) NOT NULL,
    pickup VARCHAR(100) NOT NULL,
    tip FLOAT NOT NULL,
    deliverer_id_fk INT,
    orderer_id_fk INT NOT NULL,
    time_estimate DATETIME NOT NULL,
    FOREIGN KEY(deliverer_id_fk) REFERENCES Users(id),
    FOREIGN KEY(orderer_id_fk) REFERENCES Users(id)   
)
"""

# all the tables in the database
TABLES = {"usr": "Users", "ord": "Orders", "old": "OldOrders"}


# only to be called in emergancy / creating on new system
def create_tables(connection):
    with connection.cursor() as cursor:
        try: 
            cursor.execute(create_users_table_query)
        except Error as e:
            print(e)
        try:
            cursor.execute(create_orders_table_query)
        except Error as e:
            print(e)
        try:
            cursor.execute(create_oldorders_table_query)
        except Error as e:
            print(e)

# show schema of users table
def show_table(connection, table):
    users_query = f"DESCRIBE {table}"

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
            create_tables(connection)
            for tbl in TABLES.values():
                show_table(connection, tbl)
                print("")

    except Error as e:
        print(e)


if __name__ == "__main__":
    main()
