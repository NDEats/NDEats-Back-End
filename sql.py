#!/usr/bin/env python3
from getpass import getpass
from mysql.connector import connect, Error

try:
    with connect(
        host="localhost",
        user=input("Enter username: "),
        password=getpass("Enter password: "),
        database="cse30246",
    ) as connection:
        print(connection)
except Error as e:
    print(e)
