#!/usr/bin/env python3

# Imports
import datetime
import sys
from mysql.connector import connect, Error
import os

# Import Utils from other directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + '/../'
sys.path.insert(0, os.path.join(ROOT_DIR, 'utils'))
from db_utils import desc_table, show_table

# Globals
ORDERS_TABLE = 'Orders'
OLDORDERS_TABLE = 'OldOrders'

# Functions

# insert user into users table: execute every time someone places an order
def add_order(connection, dropoff, pickup, tip, usrid, readyby):
    sql = f'''
    INSERT INTO {ORDERS_TABLE}
        (dropoff, pickup, tip, orderer_id_fk, time_estimate)
        VALUES ( %s, %s, %s, %s, %s )
    '''
    vals = (dropoff, pickup, tip, usrid, readyby)

    with connection.cursor() as cursor:
        try:
            cursor.execute(sql, vals)
            connection.commit()
        except Error as e:
            print(e)
            return False

    return True

# assign order to be delivered by usrid
def pickup_order(connection, usrid, orderid):
    # ensure order is available
    q = f'SELECT waiting_for_pickup FROM {ORDERS_TABLE} WHERE id={orderid}'
    with connection.cursor() as cursor:
        try:
            cursor.execute(q)
            result = cursor.fetchall()
            # TODO: error check as this might be out of range
            if len(result) > 0 and len(result[0]) > 0:
                if result[0][0] == 0:
                    print(f'ERROR: Order {orderid} is not available for pickup')
                    return False
            else:
                print(f'ERROR: Order {orderid} does not match any orders in DB')
                return False
        except Error as e:
            print(e)
            return False

    # add usrid as deliverer for the order with orderid in the orders table
    deliv = f'UPDATE {ORDERS_TABLE} SET deliverer_id_fk={usrid} WHERE id={orderid}' 
    # set waiting_for_pickup to 0 so it no longer is listed as available 
    unavailab = f'UPDATE {ORDERS_TABLE} SET waiting_for_pickup=0 WHERE id={orderid}'

    with connection.cursor() as cursor:
        try:
            cursor.execute(deliv)
            cursor.execute(unavailab)
            connection.commit()
        except Error as e:
            print(e)
            return False
    
    return True

# remove from Orders table, add to OldOrders table
def deliver_order(connection, orderid):
    # get order info
    get_info = f'SELECT * from {ORDERS_TABLE} where id={orderid}'
    # delete order from Orders table
    delete_order = f'DELETE FROM {ORDERS_TABLE} WHERE id={orderid}'
    # insert into the OldOrders table 
    add_order = f'''
    INSERT INTO {OLDORDERS_TABLE}
        (id, dropoff, pickup, tip, deliverer_id_fk, orderer_id_fk, time_estimate)
        VALUES ( %s, %s, %s, %s, %s, %s, %s )
    '''

    with connection.cursor() as cursor:
        # remove from Orders table
        try:
            # get order info
            cursor.execute(get_info)
            result = cursor.fetchall()
            # remove the waiting_for_pickup column
            try:
                result = list(result[0])
                result.pop(-2)
                result = tuple(result)
            except:
                return False
            
            # delete order from table
            cursor.execute(delete_order)
            connection.commit()
        except Error as e:
            print(e)
        # insert into OldOrders table 
        try:
            cursor.execute(add_order, result)
            connection.commit()
        except Error as e:
            print(e)
            return False

    return True

# Get available orders from orders page
def get_available_orders(connection):

    # Query
    mysql_get_available_orders_query = f'''
        SELECT pickup, dropoff, tip, time_estimate
        FROM {ORDERS_TABLE}
        WHERE waiting_for_pickup = 1
        ORDER BY tip DESC
    '''

    # Ececute Query
    cursor = connection.cursor()
    cursor.execute(mysql_get_available_orders_query)

    # Results
    result = cursor.fetchall()
    for row in result:
        print(row)

    # Close cursor
    cursor.close()

# Delete order
def delete_order(connection, userid, orderid):

    # Query
    mysql_delete_order_query = f'''
        DELETE FROM {ORDERS_TABLE}
        WHERE id = {orderid} AND orderer_id_fk = {userid}
    '''

    # Execute Query
    cursor = connection.cursor()

    # Checking if order exists
    try:
        cursor.execute(mysql_delete_order_query)
    except Error as e:
        print('No such order exists. ERROR:')
        print(e)

    connection.commit()

    # Close Cursors
    cursor.close()



# just for manual testing right now
def main():
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
            show_table(connection, ORDERS_TABLE)
            pickup_order(connection, 29492, 11)
            deliver_order(connection, 11)
            show_table(connection, ORDERS_TABLE)
            show_table(connection, OLDORDERS_TABLE)
            
    except Error as e:
        print(e)


if __name__ == "__main__":
    main()
