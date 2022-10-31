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


    # For now, this will return all available Orders
    def get(self, request):
        items = OrderModel.objects.filter(available=True)
        items_count = items.count()

        items_data = []
        for item in items:
            items_data.append({
                'dropoff': item.dropoff,
                'pickup': item.pickup,
                'tip': item.tip,
                'delivererId': model_to_dict(item.delivererId),
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
         
        data = json.loads(request.body.decode("utf-8"))
        order = OrderModel.objects.get(id=order_id)
        order.available = False # False = unavailable
        order.delivererId = PersonModel.objects.get(id=data['deliverer'])
        order.save()

        data = {
            'message': f'Order {order_id} has been updated\n'
        }

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
            'message': f'Order {order_id} was moved to Old Orders with new id {oldorder.id}'
        }
        order.delete()

        return JsonResponse(data)
