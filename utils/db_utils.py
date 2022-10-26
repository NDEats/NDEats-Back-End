'''
Basic Utils file where we can keep all handy functions
'''

# Imports
import datetime
from mysql.connector import connect, Error

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
