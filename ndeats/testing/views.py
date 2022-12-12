from sqlite3 import IntegrityError
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from .models import Order as OrderModel
from .models import Person as PersonModel
from .models import OldOrder as OldOrderModel
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.utils import IntegrityError
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from math import radians, cos, sin, asin, sqrt

# Globals (email related)

GMAIL_APP_PASSWD = 'idutlyhuycawqpuj'
SENDER_EMAIL = 'notredameeats@gmail.com'
PORT = 587  # For starttls
SMPT_SERVER = "smtp.gmail.com"

# Globals (Location Related)

LAT_LON_MAP = {
    'Duncan Student Center': {
        'lat': 41.6983809,
        'lon': -86.2352287
    },
    
    'Lafortune Student Center': {
        'lat': 41.701962,
        'lon': -86.237623
    },
    
    'Hesburgh Library': {
        'lat': 41.702358,
        'lon': -86.234192
    },
    
    'Hesburgh Center': {
        'lat': 41.696376,
        'lon': -86.237703
    },
    
    'Decio Faculty Hall': {
        'lat': 41.7002585,
        'lon': -86.2347036
    },
    
    'Hammes Book Store': {
        'lat': 41.692602,
        'lon': -86.2352639
    }
}

RESTAURANT_MAPPING = {
    'Chick-fil-A': 'Duncan Student Center',
    'Modern Market': 'Duncan Student Center',
    'Hagerty Family Cafe': 'Duncan Student Center',
    'Smashburger': 'Lafortune Student Center',
    'Taco Bell': 'Lafortune Student Center',
    'Starbucks': 'Lafortune Student Center',
    'Flip Kitchen': 'Lafortune Student Center',
    'The Noodle Nook': 'Lafortune Student Center',
    'Au Bon Pain': 'Hesburgh Library',
    'Garbanzo Mediterranean Fresh': 'Hesburgh Center',
    'Decio Cafe': 'Decio Faculty Hall',
    'The Gilded Bean': 'Hammes Book Store'
}

# Function to Calculate the Distance Between Two Points (Latitude / Longitude)
# Returns the Distance in KM or Miles if mi == True
def earth_distance(lat1, lat2, lon1, lon2, mi=False):
    
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371 if mi == False else 3956
      
    # calculate the result
    return(c * r)



### Person methods
@method_decorator(csrf_exempt, name='dispatch')
class Person(View):

    # Creating a new user
    def post(self, request):
       
        # Get user data
        data = json.loads(request.body.decode("utf-8"))
        
        # Seeing if Name in data sent, ie. Signup, Not Login
        if 'name' in data:
            personData = {
                'name' : data.get('name'),
                'email' : data.get('email'),
                'password' : data.get('password'),
                'venmo' : data.get('venmo')
            }

            # Create the object
            try:
                person = PersonModel.objects.create(**personData)
                data = {
                    'message': f'User created with ID: {person.id}',
                    'id': person.id,
                    'email': person.email,
                    'name': person.name,
                    'venmo': person.venmo
                }
                return JsonResponse(data, status=201)

            except IntegrityError:
                user_id = PersonModel.objects.get(email=data.get('email')).id
                data = {
                    'message': f'A user with the same email already exists with ID: {user_id}',
                    'id': 0
                }
                return JsonResponse(data, status=202)  # Not sure if 202 is right
        
        else:
            personData = {
                'email' : data.get('email'),
                'password' : data.get('password')
            }
            
            # See if user exists
            person_list = PersonModel.objects.filter(email=data.get('email'))
            if person_list.count() == 0:
                data = {
                    'message': f'This email does not exist in the database.',
                    'id': 0
                }
                return JsonResponse(data, status=202)
            
            # User exists, check if passwords match
            for person in person_list:
                if person.password != personData['password']:
                    data = {
                        'message': f'Incorrect password.',
                        'id': 0
                    }
                    return JsonResponse(data, status=202)

                # Matching Passwords
                data = {
                    'message': f'User successfully logged in with ID: {person.id}',
                    'id': person.id,
                    'email': person.email,
                    'name': person.name
                }
                return JsonResponse(data, status=200)
    
    
    # return all orders associated with a user
    def get(self, request, person_id):
        
        person = PersonModel.objects.get(id=person_id)
        
        # Orders that the user is currently picking up
        pickedup_items = OrderModel.objects.filter(delivererId=person)

        # Current Items are My Orders that haven't been picked up
        current_items = OrderModel.objects.filter(ordererId=person)

        # Completed Orders that were created by user and delivered by user
        old_items = OldOrderModel.objects.filter(ordererId=person) | OldOrderModel.objects.filter(delivererId=person)
        
        pickedup_count = pickedup_items.count()
        current_orders_count = current_items.count()
        old_orders_count = old_items.count()
        
        pickedup_orders = []
        for order in pickedup_items:
            pickedup_orders.append({
                'id' : order.id,
                'dropoff' : order.dropoff,
                'pickup' : order.pickup,
                'tip' : order.tip,
                'orderer_name' : order.ordererId.name,
                'orderer_email' : order.ordererId.email,
                'deliverer_name' : order.delivererId.name,
                'deliverer_email' : order.delivererId.email,
                'readyby' : order.readyBy
            })


        current_orders = []
        for order in current_items:
            if order.delivererId:
                current_orders.append({
                    'id' : order.id,
                    'dropoff' : order.dropoff,
                    'pickup' : order.pickup,
                    'tip' : order.tip,
                    'orderer_name' : order.ordererId.name,
                    'orderer_email' : order.ordererId.email,
                    'deliverer_name' : order.delivererId.name,
                    'deliverer_email' : order.delivererId.email,
                    'readyby' : order.readyBy
                })
            else:
                current_orders.append({
                    'id' : order.id,
                    'dropoff' : order.dropoff,
                    'pickup' : order.pickup,
                    'tip' : order.tip,
                    'orderer_name' : order.ordererId.name,
                    'orderer_email' : order.ordererId.email,
                    'deliverer_name' : 'Searching for deliverer ...',
                    'deliverer_email' : 'Searching for deliverer ...',
                    'readyby' : order.readyBy
                })
                
            
        old_orders = []
        for order in old_items:
            old_orders.append({
                'id' : order.id,
                'dropoff' : order.dropoff,
                'pickup' : order.pickup,
                'tip' : order.tip,
                'orderer_name' : order.ordererId.name,
                'orderer_email' : order.ordererId.email,
                'deliverer_name' : order.delivererId.name,
                'deliverer_email' : order.delivererId.email,
                'readyby' : order.readyBy
            })
        
        data = {
            'pickedup_orders' : pickedup_orders,
            'pickedup_count' : pickedup_count,
            'current_orders' : current_orders,
            'current_count' : current_orders_count,
            'old_orders' : old_orders,
            'old_count' : old_orders_count
        }

        return JsonResponse(data)
                
            
### Order Methods
@method_decorator(csrf_exempt, name='dispatch')
class Order(View):
    # TODO: change so order_id is in the url, like OrderUpdate
    def post(self, request):
        # get user specified data
        data = json.loads(request.body.decode("utf-8"))
        do = data.get('dropoff')
        pu = data.get('pickup')
        t = data.get('tip')
        orderer_email = data.get('email')
        rb = data.get('readyBy')

        # save order data in dict to create order class
        orderData = {
            'dropoff' : do,
            'pickup' : pu,
            'tip' : t,
            'delivererId': None,
            'ordererId': PersonModel.objects.get(email=orderer_email),
            'available': True,
            'readyBy': rb,
        }
        
        # create instance of order (automatically stores order in orders table)
        order = OrderModel.objects.create(**orderData)

        # send response with order ID
        data = {
            'message': f'Order created with ID: {order.id}',
            'id': order.id
        }
        return JsonResponse(data, status=201)


    # For now, this will return all available Orders
    # This is where we want to do the GPS shit
    def get(self, request):
        items = OrderModel.objects.filter(available=True)
        items_count = items.count()
        
        # Get user latitude / longitude info
        #data = json.loads(request.body.decode("utf-8"))
        #user_latitude = data['latitude']
        #user_longitude = data['longitude']
        
        # TODO: Think about how we will sort the items_data by distance

        items_data = []
        for item in items:
            items_data.append({
                'id' : item.id,
                'dropoff': item.dropoff,
                'pickup': item.pickup,
                'tip': item.tip,
                'orderer_name': item.ordererId.name,
                'orderer_email': item.ordererId.email,
                'available': item.available,
                'readyBy': item.readyBy,
            })

        data = {
            'items': items_data,
            'count': items_count
        }

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class OrderUpdate(View):
    def patch(self, request, order_id):
        data = json.loads(request.body.decode("utf-8"))
        order = OrderModel.objects.get(id=order_id)
        order.available = False # False = unavailable
        deliverer = PersonModel.objects.get(email=data.get('email'))
        order.delivererId = deliverer
        order.save()
        # get orderer
        orderer   = order.ordererId

        # generate venmo request link from deliverer
        note="Pay me to deliver your order posted on NDEats"
        note = note.replace(" ", "%20")
        request_from = order.ordererId.venmo
        amount = order.tip
        rlink = f"https://venmo.com/?txn=charge&audience=private&recipients={request_from}&amount={amount}&note={note}"

        data = {
            'message': f'Order {order_id} has been updated',
            'id': order_id
        }

        # send confirmation emails
        context = ssl.create_default_context()

        deliverer_message = MIMEMultipart("alternative")
        deliverer_message["Subject"] = "NDEats Pickup Confirmation"
        deliverer_message["From"] = 'NDEats'
        deliverer_message["To"] = deliverer.email

        orderer_message = MIMEMultipart("alternative")
        orderer_message["Subject"] = "NDEats Pickup Confirmation"
        orderer_message["From"] = 'NDEats'
        orderer_message["To"] = orderer.email

        # build deliverer email
        text = ''
        text += f'Hello, {deliverer.name}!\n'
        text += f'\n'
        text += f'Your pickup of order #{order_id} has been confirmed. '
        text += f'You may request your tip of ${order.tip} on Venmo: {rlink}\n\n'
        text += f'Please pickup {orderer.name}\'s order from {order.pickup} at {order.readyBy}, '
        text += f'and deliver it to {order.dropoff}.\n\n'
        text += f'Remember, it\'s not a bad idea to ensure your Venmo request has been '
        text += f'fulfilled before handing over the food!\n\n'
        text += f'Happy delivering,\nNDEats'

        html = ''
        html += f'<html><body><p>Hello, {deliverer.name}!<br><br>'
        html += f'Your decision to pick up order #{order_id} has been confirmed. '
        html += f'<a href="{rlink}">Click here</a>'
        html += f' to request your tip of ${order.tip} on Venmo.<br><br>'
        html += f'Please pickup {orderer.name}\'s order from {order.pickup} at {order.readyBy}, '
        html += f'and deliver it to {order.dropoff}.<br><br>'
        html += f'Remember, it\'s not a bad idea to ensure your Venmo request has been '
        html += f'fulfilled before handing over the food!<br><br>'
        html += f'Happy delivering,<br>NDEats'
        html += '</p></body></html>'

        # build orderer email (no links = no need for html)
        orderer_text = ''
        orderer_text += f'Hello, {orderer.name}!\n'
        orderer_text += f'\n'
        orderer_text += f'Your order from {order.pickup} (#{order_id}) has been selected for pickup by {deliverer.name}. '
        orderer_text += f'Please keep an eye out for a Venmo request of ${order.tip}!\n\n'
        orderer_text += f'Happy munching,\nNDEats'

        # convert to email format
        body_plain = MIMEText(text, 'plain')
        body_html = MIMEText(html, 'html')
        orderer_body = MIMEText(orderer_text, 'plain')

        deliverer_message.attach(body_plain)
        deliverer_message.attach(body_html)
        # email client will try to render the last subpart first (html) and render the first
        # one if that fails (plain)
        orderer_message.attach(orderer_body)

        # send the emails 
        try:
            server = smtplib.SMTP(SMPT_SERVER,PORT)
            server.starttls(context=context)
            server.login(SENDER_EMAIL, GMAIL_APP_PASSWD)
            server.sendmail(SENDER_EMAIL, deliverer.email, deliverer_message.as_string())
            server.sendmail(SENDER_EMAIL, orderer.email, orderer_message.as_string())
        except Exception as e:
            print(e)
        finally:
            server.quit()

        return JsonResponse(data)

    def delete(self, request, order_id):
        order = OrderModel.objects.get(id=order_id)
        
        order_data = {    
            'dropoff' :    order.dropoff,
            'pickup' :     order.pickup,
            'tip' :        order.tip,
            'delivererId': order.delivererId,
            'ordererId':   order.ordererId,
            'readyBy':     order.readyBy,
        }
        
        oldorder = OldOrderModel.objects.create(**order_data)

        data = {
            'message': f'Order {order_id} was moved to Old Orders with new id {oldorder.id}',
            'order_id': order_id,
            'oldorder_id': oldorder.id
        }
        order.delete()

        return JsonResponse(data)
