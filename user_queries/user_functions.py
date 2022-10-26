#!/usr/bin/env python3

# Imports
from mysql.connector import connect, Error

# Globals
USER_TABLE = 'Users' 
ORDER_TABLE = 'Orders'
OLD_ORDER_TABLE = 'OldOrders'

# Functions
def add_user_to_Users(connection, username, name, email):

    # Define the Query
    mysql_user_insert_query = f'''
        INSERT INTO {USER_TABLE} (id, name, email)
        VALUES ({username}, '{name}', '{email}')
    '''

    # Execute Query using Cursor
    cursor = connection.cursor()

    # Check if user already in Users
    try:
        cursor.execute(mysql_user_insert_query)
    except Error as e:
        print(f'User already exists in database')
    
    connection.commit()

    # Close cursor
    cursor.close()

def get_user_orders_from_Orders(connection, username):

    # Define the Query
    mysql_get_user_orders_query = f'''
        SELECT *
        FROM {ORDER_TABLE}
        WHERE orderer_id_fk = '{username}' OR deliverer_id_fk = '{username}'
    '''

    # Execute Query using Cursor
    cursor = connection.cursor()
    cursor.execute(mysql_get_user_orders_query)

    # Print out result
    result = cursor.fetchall()
    print("Results from Orders:")
    for row in result:
        print(row)

    # Close Cursor
    cursor.close()


def get_user_orders_from_OldOrders(connection, username):

    # Define the Query
    mysql_get_user_old_orders_query = f'''
        SELECT *
        FROM {OLD_ORDER_TABLE}
        WHERE orderer_id_fk = '{username}' OR deliverer_id_fk = '{username}'
    '''

    # Execute Query using Cursor
    cursor = connection.cursor()
    cursor.execute(mysql_get_user_old_orders_query)

    # Print out result
    result = cursor.fetchall()
    print("Results from Old Orders:")
    for row in result:
        print(row)

    # Close Cursor
    cursor.close()




# Main Execution
def main():
    try:
        with connect(host="localhost", user="bgoodwin", password="pwpwpwpw", database="bgoodwin") as connection:
            # Do Stuff

            # TODO: Get these values from Google Sign in!! (we wanna execute this anytime someone signs in)
            add_user_to_Users(connection, 293942, 'Jean Francois Boueri', 'jbueri@nd.edu')

            get_user_orders_from_Orders(connection, 29492)
            get_user_orders_from_OldOrders(connection, 29492)

    except Error as e:
        print(e)

if __name__ == '__main__':
    main()
