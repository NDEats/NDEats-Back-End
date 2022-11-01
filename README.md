# NDEats-Back-End

## Running the server 
1. Checkout branch `DjangoSetUp` 
2. Run `./install.sh`
3. `cd ndeats`
4. `/usr/bin/python3 manage.py runserver`

Once you run the server, you can run SOME of the examples below. You have to check that your IDs are available; i.e. you have to check that the order ID is in the `testing_orders` table and available before requesting to pickup an order. 

## RESTful API
[How to consume a RESTful API in React](https://pusher.com/tutorials/consume-restful-api-react/)

Notes: 
* Variables are in <>, i.e. <string: dropoff location> can be replaced with Hesburg or <float: tip> can be replaced with 5.50
* These should all be just in one line 
* The ID of each person/order is returned in the response from the server when you add a person/order
* Deleting an order and dropping off an order are the same request; both move the order from the orders table to the old orders table 

### Syntax

Add User:
```
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/persons/ -d 
    "\"name\":\"<str: name of user>\", 
    \"email\":\"<str: email of user>\"}"
```
Add Order:
```
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/orders/ -d 
    "{\"dropoff\":\"<string: dropoff location>\",
    \"pickup\":\"<string: pickup location>\",
    \"tip\":\"<float: tip>\",
    \"ordererId\":\"<int: id of the person placing the order>\",
    \"readyBy\":\"<timestamp (weird formatting, see exs)>\"}"
```
Pickup Order:
```
curl -X PATCH http://127.0.0.1:8000/update-order/<int: id of the order being picked up> -d 
    "{\"deliverer\":\"<int: id of the person picking up the order>\"}"
```
Get All Available Orders:
```
curl -X GET http://127.0.0.1:8000/orders/
```
Dropoff or Delete Order:
```
curl -X DELETE http://127.0.0.1:8000/update-order/<int: id of the order>
```

### Examples
Add User: 
`curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/persons/ -d "\"name\":\"Pat\", \"email\":\"pcarr2@nd.edu\"}"`

Add Order:
`curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/orders/ -d "{\"dropoff\":\"Duncan Hall\",\"pickup\":\"Modern Market\",\"tip\":\"1\",\"ordererId\":\"1\",\"readyBy\":\"18:00:00\"}"`

Pickup Order:
`curl -X PATCH http://127.0.0.1:8000/update-order/4 -d "{\"deliverer\":\"2\"}"`

Get Available Orders:
`curl -X GET http://127.0.0.1:8000/orders/`

Delete Order:
`curl -X DELETE http://127.0.0.1:8000/update-order/11`
