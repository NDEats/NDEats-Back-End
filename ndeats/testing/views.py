from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from .models import Order as OrderModel
from .models import Person as PersonModel
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class Order(View):
    # TODO: change so order_id is in the url, like OrderUpdate
    def post(self, request):
        # get user specified data
        data = json.loads(request.body.decode("utf-8"))
        do = data.get('dropoff')
        pu = data.get('pickup')
        t = data.get('tip')
        oid = data.get('ordererId')
        rb = data.get('readyBy')

        # save order data in dict to create order class
        orderData = {
            'dropoff' : do,
            'pickup' : pu,
            'tip' : t,
            'delivererId': PersonModel.objects.get(id=2),
            'ordererId': PersonModel.objects.get(id=oid),
            'available': True,
            'readyBy': rb,
        }
        
        # create instance of order (automatically stores order in orders table)
        order = OrderModel.objects.create(**orderData)

        # send response with order ID
        data = {
            'message': f'Order created with ID: {order.id}\n'
        }
        return JsonResponse(data, status=201)

@method_decorator(csrf_exempt, name='dispatch')
class OrderUpdate(View):
    def patch(self, request, order_id):
         
        data = json.loads(request.body.decode("utf-8"))
        order = OrderModel.objects.get(id=order_id)
        order.available = data['available']
        order.delivererId = PersonModel.objects.get(id=data['deliverer'])
        order.save()

        data = {
            'message': f'Order {order_id} has been updated\n'
        }

        return JsonResponse(data)

