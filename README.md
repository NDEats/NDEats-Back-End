# NDEats-Back-End

## Running the backend server 
1. Checkout branch `main` 
2. Run `./install.sh`
3. `cd ndeats`
4. `/usr/bin/python3 manage.py runserver`

This will run the server on port 8000 (optional: `python3 manage.py runserver 8001` to specify different port), and the server will be listening for requests over the API.

## Running the frontend 
### Setup requirements
* npm 8.19.2 (default on db8: v8.11.0)
* node 16.15.1 (default on db8: v10.24.0)

1. Install nvm and clone the `.nvm` directory to your home directory with: `wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash` 
2. check `.bashrc` to ensure the following lines were added:
```
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
```
3. `source ~/.bashrc` to load nvm 
4. `nvm -v` to check nvm was installed; mine was `0.39.1`
5. `nvm install v16.15.1` install required version of node
6. `nvm alias default v16.15.1` make required version of node the default version
7. Check `node -v` is v16.15.1
8. `npm install -g npm@8.19.2` to install required version of npm
9. Check `npm -v` is 8.19.2
### Install and run app 
10. `git clone git@github.com:NDEats/NDEats-Front-End.git`
11. `cd NDEats-Front-End/nd-eats-front`
12. (Note: this step might not be necessary, feel free to test if it is or not) remove the `package-lock.json` file
13. `npm install gh-pages --save-dev`
14. `npm i` to install 
15. `npm start` to start app 
16. This command should open http://localhost:3000 and you should be able to view the app; use VSCode for automatic port forwarding from db8

After all this, you should be able to run just with `npm start`

## RESTful API Documentation
[How to consume a RESTful API in React](https://pusher.com/tutorials/consume-restful-api-react/)
[Pretty much how the entire backend works](https://stackabuse.com/creating-a-rest-api-in-python-with-django/)
Once you run the server, you can run SOME of the examples below. You have to check that your IDs are available; i.e. you have to check that the order ID is in the `testing_orders` table and available before requesting to pickup an order. 

Notes: 
* Variables are in <>, i.e. <string: dropoff location> can be replaced with Hesburg or <float: tip> can be replaced with 5.50
* These should all be just in one line 
* The ID of each person/order is returned in the response from the server when you add a person/order
* Deleting an order and dropping off an order are the same request; both move the order from the orders table to the old orders table 
* All the IDs (Primary Keys in the DB) are being automatically created by Django

### Syntax

Add/login User (login = don't inculde name, signup = include name:
```
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/persons/ -d 
    {"\"name\":\"<str: name of user>\", 
    \"email\":\"<str: email of user>\",
    \"password\":\"<str: password of user>\"}"
```
Add Order:
```
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/orders/ -d 
    "{\"dropoff\":\"<string: dropoff location>\",
    \"pickup\":\"<string: pickup location>\",
    \"tip\":\"<float: tip>\",
    \"email\":\"<str: email of the person placing the order>\",
    \"readyBy\":\"<timestamp (weird formatting, see exs)>\"}"
```
Pickup Order:
```
curl -X PATCH http://127.0.0.1:8000/update-order/<int: id of the order being picked up> -d 
    "{\"email\":\"<str: email of the person picking up the order>\"}"
```
Get All Available Orders:
```
curl -X GET http://127.0.0.1:8000/orders/
```
Dropoff or Delete Order:
```
curl -X DELETE http://127.0.0.1:8000/update-order/<int: id of the order>
```

Get a User's Orders:
```
curl -X GET http://127.0.0.1:8000/persons/<int: id of the current user>
```

### Examples
Add User: 
`curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/persons/ -d {"\"name\":\"Jean Boueri\", \"email\":\"jboueri@nd.edu\",\"password\":\"sqlislife\", \"venmo\":\"jeanfboueri\"}"`

Add Order:
`curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/orders/ -d "{\"dropoff\":\"Duncan Hall\",\"pickup\":\"Modern Market\",\"tip\":\"1\",\"email\":\"jboueri@nd.edu\",\"readyBy\":\"18:00:00\"}"`

Pickup Order:
`curl -X PATCH http://127.0.0.1:8000/update-order/4 -d "{\"email\":\"bgoodwin@nd.edu\"}"`

> e.g. the '4' in `update-order/4` is the order id

Get Available Orders:
`curl -X GET http://127.0.0.1:8000/orders/`

Delete Order:
`curl -X DELETE http://127.0.0.1:8000/update-order/11`

Get a User's Orders:
`curl -X GET http://127.0.0.1:8000/persons/6`

### Database
The data is stored in Django-created tables the `cboumalh` database on the `mysql` setup on `db8.cse.nd.edu`; the tables have names like `testing_order` and `testing_person`; to insert data you must be on `db8.cse.nd.edu`
* User: `cboumalh`
* Pass: `pwpwpwpw`

The project is called `ndeats` and is stored in `ndeats/ndeats`, the app that handles the API is currently called `ndeatsApp` and is located in `ndeats/ndeatsApp`. 
