#!/usr/bin/env python3

from getpass import getpass
from mysql.connector import connect, Error

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

ORDERS_TABLE = 'Orders'
OLDORDERS_TABLE = 'OldOrders'


# insert user into users table
def add_order(connection, dropoff, pickup, tip, orderer_id, readyby):
    sql = f'''
    INSERT INTO {ORDERS_TABLE}
        (dropoff, pickup, tip, orderer_id_fk, time_estimate)
        VALUES ( %s, %s, %s, %s, %s )
    '''
    vals = (dropoff, pickup, tip, orderer_id, readyby)

    with connection.cursor() as cursor:
        try:
            cursor.execute(sql, vals)
            connection.commit()
        except Error as e:
            if 'foreign key constraint' in e:
                print('ERROR: User does not exist')
            return False

    return True


# show schema of users table
def show_table(connection, table):
    users_query = f'DESCRIBE {table}'

    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)


# show data in a given table
def show_table(connection, table):
    users_query = f'SELECT * FROM {table}'

    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)




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
            #show_table(connection, ORDERS_TABLE)
            added = add_order(connection, 'Farley Hall', 'Chic-fil-a', 8.25, 1, '1998-01-23 12:45:56')
            show_table(connection, ORDERS_TABLE)
            
    except Error as e:
        print(e)


if __name__ == "__main__":
    main()
