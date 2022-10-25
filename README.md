# NDEats-Back-End

`sql.py` is just for reference for current dev branches with info from this [tutorial](https://realpython.com/python-mysql/#installing-mysql-server-and-mysql-connectorpython)

Users table created in database bgoodwin on db student machines
```
CREATE TABLE users(
    id INT PRIMARY KEY, # userinfo_response.json()["sub"]
    name VARCHAR(100),  # userinfo_response.json()["given_name"]
    email VARCHAR(100), # userinfo_response.json()["email"]
)
``` 
