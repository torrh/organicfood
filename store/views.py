# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.views.decorators.csrf import csrf_exempt

from .models import Category, Consumer, ProductType, ProducerOffer, AdminOffer, Producer, Sales_Parameters
from django.http import HttpResponse, JsonResponse
from django.core import serializers as jsonserializer
from rest_framework import generics, status
from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404
from itertools import chain
from rest_framework.response import Response

from . import models
from . import serializers


# Create your views here.

class ListCreateProductType(generics.ListCreateAPIView):
    queryset = models.ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer


class RetriveUpdateDestroyProductType(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProductType.objects.all()
    serializer_class = serializers.ProductTypeSerializer


@csrf_exempt
def register_consumer(request):
    mensaje = 'error'
    data = 'none'
    if request.method == 'POST':
        json_data = json.loads(request.body)
        uid = json_data['uid']
        name = json_data['name']
        email = json_data['email']
        lastname = json_data['lastname']
        password = json_data['password']
        address = json_data['address']

        phone_number = json_data['phone_number']
        num_results = Consumer.objects.filter(email=email).count()
        if num_results==0:
            new_consumer = Consumer.objects.create(uid=uid, name=name, last_name=lastname, email=email, address=address,
                                               password=password,
                                               phone_number=phone_number, type="CLIENTE")
            new_consumer.save();
            mensaje = 'ok'
            data = {'name': name,
                'last_name': lastname,
                'email': email,
                'address': address,
                'phone_number': phone_number,
                'type': 'CLIENTE'
         }
        return JsonResponse({"estado": mensaje, "data": data})


@csrf_exempt
def login(request):
    mensaje = 'error'
    data = 'none'
    if request.method == 'POST':
        json_data = json.loads(request.body)
        email = json_data['email']
        password = json_data['password']
        consumer_bd = Consumer.objects.get(email=email)
        if consumer_bd.password == password:
            mensaje = 'ok'
            data = {'name': consumer_bd.name,
                    'last_name': consumer_bd.last_name,
                    'email': email,
                    'address': consumer_bd.address,
                    'phone_number': consumer_bd.phone_number
                    }
    return JsonResponse({"estado": mensaje, "data": data})


@csrf_exempt
def consumer_details(request, email):
    mensaje = "Consumer not found"
    if request.method == 'GET':

        consumer_bd = Consumer.objects.get(email=email)

        if consumer_bd.email == email:
            data = {'name': consumer_bd.name,
                    'last_name': consumer_bd.last_name,
                    'email': email,
                    'address': consumer_bd.address,
                    'phone_number': consumer_bd.phone_number
                    }
        return JsonResponse({"data": data})
    return JsonResponse({"error": mensaje})


@csrf_exempt
def prueba(request):
    if request.method == 'POST':
        return JsonResponse({"estado": "ok"})
    else:
        return JsonResponse({"estado": "ok"})

class ListOrderItemsToProducer(generics.ListAPIView):
    queryset = models.Order_Item.objects.all()
    serializer_class = serializers.OrderItemSerializer

    def get_queryset(self):
        return models.Order_Item.objects.filter(Q(offer__productType__producer_id=self.kwargs.get('producer_pk')))

class RetrieveOrderByConsumer(generics.RetrieveAPIView):
    serializer_class = serializers.OrderSerializer

    def get_object(self):
        return models.Order.objects.filter(consumer_id=self.kwargs.get('consumer_pk')).last()


@csrf_exempt
def all(request):
    products = ProductType.objects.all();

    return HttpResponse(jsonserializer.serialize("json", products))


@csrf_exempt
def create_offer_producer(request):
    mensaje = 'error'
    data = 'none'
    print request.body
    if request.method == 'POST':
        json_data = json.loads(request.body)
        producto = json_data['idProductNewOffer']
        cantidad = json_data['amountNewOffer']
        precio = json_data['priceNewOffer']
        unidad = json_data['unit']
        productor = json_data['idProducer']
        fechaCreacion = json_data['createdAt']
        fechaEntrega = json_data['deliveryDateNewOffer']
        modificable = True
        estado = 'PENDIENTE'
        mensaje = 'ok'
        consumer_bd = ProducerOffer.objects.create(create_at=fechaCreacion, editable=modificable, state=estado,
                                                   unit_price=precio, count=cantidad, unit_type=unidad,
                                                   available_at=fechaEntrega,
                                                   producer_id=productor, productType_id=producto)
        consumer_bd.save();
    return JsonResponse({"estado": mensaje, "data": data})


@csrf_exempt
def give_all_producersoffers(request):
    offers = ProducerOffer.objects.all()
    return HttpResponse(jsonserializer.serialize("json", offers))


@csrf_exempt
def create_offer_admin(request):
    mensaje = 'error'
    data = 'none'
    print request.body
    if request.method == 'POST':
        json_data = json.loads(request.body)
        producto = json_data['idProductNewOffer']
        cantidad = json_data['amountNewOffer']
        precio = json_data['priceNewOffer']
        unidad = json_data['unit']
        fechaCreacion = json_data['createdAt']
        fechaEntrega = json_data['deliveryDateNewOffer']

        mensaje = 'ok'
        consumer_bd = AdminOffer.objects.create(create_at=fechaCreacion,
                                                unit_price=precio, count=cantidad, unit_type=unidad,
                                                delivery_date=fechaEntrega
                                                , productType_id=producto)
        consumer_bd.save();
    return JsonResponse({"estado": mensaje, "data": data})


@csrf_exempt
def give_all_adminoffers(request):
    offers = AdminOffer.objects.all()
    return HttpResponse(jsonserializer.serialize("json", offers))




@csrf_exempt
def create_order(request):
    mensaje = 'error'
    data = 'none'

    if request.method == 'POST':
        json_data = json.loads(request.body)
        create_at_data = json_data['create_at']
        delivery_at_data = json_data['delivery_at']
        shipping_address_data = json_data['shipping_address']
        consumer_data = json_data['consumer_id']
        order_items = json_data['order_items']

        order_bd = models.Order.objects.create(create_at=create_at_data,
                                               delivery_at=delivery_at_data, shipping_address=shipping_address_data,
                                               consumer_id=consumer_data)
        order_bd.save()

        for order_item in order_items:
            count_order = order_item['count']
            offer_order = order_item['offer_id']

            offer = models.AdminOffer.objects.get(id=offer_order)
            offer.count = int(offer.count) - int(count_order)  # actualiza la cantidad de la oferta
            offer.save()

            order_item = models.Order_Item.objects.create(count=count_order, offer_id=offer_order, order_id=order_bd.id)
            order_item.save()

        mensaje = 'ok'

    return JsonResponse({"estado": mensaje, "data": data})


class ListOrderItems(generics.ListAPIView):
    queryset = models.Order_Item.objects.all()
    serializer_class = serializers.OrderItemSerializer


@csrf_exempt
def save_producer_offers(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        acceptedIds = json_data['acceptedIds']
        canceledIds = json_data['canceledIds']
        for accepted in acceptedIds:
            uid = accepted['id']
            p = ProducerOffer.objects.get(id=uid)
            p.state = 'ACEPTADA'
            p.save()
        for canceled in canceledIds:
            cuid = canceled['id']
            c = ProducerOffer.objects.get(id=cuid)
            c.state = 'CANCELADA'
            c.save()
    return JsonResponse({"estado":"ok"})


@csrf_exempt
def getproducerbyid(request, id):
    if request.method == 'GET':
        total = Producer.objects.get(uid=id)
        return JsonResponse({"id": total.id, "email": total.email,"name":total.name,
                             "lastname":total.last_name,"address":total.address,"latitude":total.latitude,
                             "longitude":total.longitude,"phone_number":total.phone_number})


@csrf_exempt
def getacceptedproduceroffers(request):
    total = ProducerOffer.objects.filter(state="ACEPTADA")
    return HttpResponse(jsonserializer.serialize("json", total))


@csrf_exempt
def getoffersbyproductorbyid(request,id):
    if request.method =='GET':
        response = ProducerOffer.objects.filter(producer_id=id)

        for obj in response:
            product = ProductType.objects.get(id=obj.productType_id)
            title = product.title

        return HttpResponse( jsonserializer.serialize("json", response ))

class RetriveUpdateDestroyProductOffer(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.ProducerOffer.objects.all()
    serializer_class = serializers.ProducerOfferSerializer

class ListProducerOffers(generics.ListAPIView):
    queryset = models.ProducerOffer.objects.all()
    serializer_class = serializers.ProducerAllOfferSerializer

class ListOffersByProducer(generics.ListAPIView):
    queryset = models.ProducerOffer.objects.all()
    serializer_class = serializers.ProducerAllOfferSerializer

    def get_queryset(self):
        return models.ProducerOffer.objects.filter(producer_id=self.kwargs.get('producer_pk'))

class ListAdminOffersItems(generics.ListAPIView):
    queryset = models.AdminOffer.objects.all()
    serializer_class = serializers.AdminOfferSerializer

class updatePartialOrder(generics.UpdateAPIView):

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = serializers.OrderSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def suggested_retail_price(request):

    if request.method == 'POST':
        json_data = json.loads(request.body)

        parameters = Sales_Parameters.objects.last()

        price = json_data['precio_producto']
        amount = json_data['cantidad_oferta']

        marketing = 15000
        shipping = 3000
        cost = int(price) * int(amount)

        total = cost + marketing + shipping
        unit_cost = total / amount

        retail_price = round(unit_cost / (1 - parameters.profit_margin))

        return JsonResponse({"precio_venta": retail_price})