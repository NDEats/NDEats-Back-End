# NDEats-Back-End

[tutorial](https://realpython.com/python-mysql/#installing-mysql-server-and-mysql-connectorpython)

Users table
```
CREATE TABLE users(
    id INT PRIMARY KEY, # userinfo_response.json()["sub"]
    name VARCHAR(100),  # userinfo_response.json()["given_name"]
    email VARCHAR(100), # userinfo_response.json()["email"]
)
``` 
