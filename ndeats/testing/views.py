from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from .models import Order
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class Order(View):
    def post(self, request):
        # get user specified data
        data = json.loads(request.body.decode("utf-8"))
        do = data.get('dropoff')
        pu = data.get('pickup')
        t = data.get('tip')
        oid = data.get('ordererId')
        rb = data.get('readyBy')

        # set default values user cannot specify
        did = None # delivererId
        a = True   # available
        
        # save order data in dict to create order class
        orderData = {
            'dropoff' : do,
            'pickup' : pu,
            'tip' : t,
            'delivererId': did,
            'ordererId': oid,
            'available': a,
            'readyBy': rb,
        }
        
        # create instance of order (automatically stores order in orders table)
        order = Order.objects.create(**orderData)

        # send response with order ID
        data = {
            'message': f'Order created with ID: {order.id}'
        }
        return JsonResponse(data, status=201)

