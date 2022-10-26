'''
Basic Utils file where we can keep all handy functions
'''

# Imports
import datetime
from mysql.connector import connect, Error

# Queries

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

# Functions

# show schema of users table
def desc_table(connection, table):
    users_query = f'DESCRIBE {table}'

    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print("")


# show data in a given table
def show_table(connection, table):
    users_query = f'SELECT * FROM {table}'

    with connection.cursor() as cursor:
        cursor.execute(users_query)
        result = cursor.fetchall()
        for row in result:
            print(row)
        print("")

# create all the tables with these queries
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


# NOTE: users may have to agree that payments may not be fulfilled & agree 
# they're trusting randos to venmo them (?)

# :param request_from: venmo username to send the request to 
# :param amount: amount to request in USD
# :param txn: type of payment; "charge" or "pay"
# :param note: venmo note
# :returns: link to venmo to request delivery fee
def generate_venmo_request_link(request_from, amount, txn="charge", 
        note="Pay me to deliver your order posted on NDEats", verbose=False):
    # link format source: https://venmo.com/paymentlinks
    # replace spaces with %20 for venmo link to work
    note = note.replace(" ", "%20")
    # insert fields into venmo request link
    rlink = f"https://venmo.com/?txn=charge&audience=private&recipients={request_from}&amount={amount}&note={note}"
    
    if verbose:
        print(f"Payment link: {rlink}")

    return rlink



def main():
    pass

if __name__ == '__main__':
    main()
