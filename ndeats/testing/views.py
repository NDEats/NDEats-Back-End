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


GMAIL_APP_PASSWD = 'idutlyhuycawqpuj'
SENDER_EMAIL = 'notredameeats@gmail.com'
PORT = 587  # For starttls
SMPT_SERVER = "smtp.gmail.com"

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
        current_items = OrderModel.objects.filter(ordererId=person, available=True)
        active_items = OrderModel.objects.filter(ordererId=person, available=False)
        old_items = OldOrderModel.objects.filter(ordererId=person)
        
        current_orders_count = current_items.count()
        active_orders_count = active_items.count()
        old_orders_count = old_items.count()

        orders = []
        for order in current_items:
            orders.append({
                'id' : order.id,
                'dropoff' : order.dropoff,
                'pickup' : order.pickup,
                'tip' : order.tip,
                'ordererId' : model_to_dict(order.ordererId),
                'readyby' : order.readyBy
            })
        
        active_orders = []
        for order in active_items:
            active_orders.append({
                'id' : order.id,
                'dropoff' : order.dropoff,
                'pickup' : order.pickup,
                'tip' : order.tip,
                'ordererId' : model_to_dict(order.ordererId),
                'delivererId' : model_to_dict(order.delivererId),
                'readyby' : order.readyBy
            })
            
        old_orders = []
        for order in old_items:
            old_orders.append({
                'id' : order.id,
                'dropoff' : order.dropoff,
                'pickup' : order.pickup,
                'tip' : order.tip,
                'ordererId' : model_to_dict(order.ordererId),
                'delivererId' : model_to_dict(order.delivererId),
                'readyby' : order.readyBy
            })
        
        data = {
            'current_orders' : orders,
            'current_count' : current_orders_count,
            'active_orders' : active_orders,
            'active_count' : active_orders_count,
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
    def get(self, request):
        items = OrderModel.objects.filter(available=True)
        items_count = items.count()

        items_data = []
        for item in items:
            items_data.append({
                'id' : item.id,
                'dropoff': item.dropoff,
                'pickup': item.pickup,
                'tip': item.tip,
                'ordererId': model_to_dict(item.ordererId),
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
        #GMAIL_APP_PASSWD = 'idutlyhuycawqpuj'
        #PORT = 587  # For starttls
        #SENDER_EMAIL = 'notredameeats@gmail.com'
        #SMPT_SERVER = "smtp.gmail.com"
        data = json.loads(request.body.decode("utf-8"))
        order = OrderModel.objects.get(id=order_id)
        order.available = False # False = unavailable
        #order.delivererId = PersonModel.objects.get(email=data.get('email'))
        # get deliverer 
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
            'id': order_id,
            'rlink': rlink
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
