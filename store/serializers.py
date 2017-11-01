from rest_framework import serializers

from . import models

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title',
            'description',
            'url',
        )
        model = models.ProductType

class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email',
            'name',
            'last_name',
            'address',
            'phone_number'
        )

        model = models.Producer

class ProducerOfferSerializer(serializers.ModelSerializer):

    productType = ProductTypeSerializer(read_only=True)
    producer = ProducerSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'editable',
            'state',
            'unit_price',
            'count',
            'unit_type',
            'available_at',
            'productType',
            'producer',
        )
        model = models.ProducerOffer

class ProducerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email',
            'name',
            'last_name',
            'address',
            'phone_number'
        )

        model = models.Producer

class ProducerAllOfferSerializer(serializers.ModelSerializer):

    productType = ProductTypeSerializer(read_only=True)
    producer = ProducerSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'editable',
            'create_at',
            'state',
            'unit_price',
            'count',
            'unit_type',
            'available_at',
            'productType',
            'producer'
        )
        model = models.ProducerOffer

class PaymentTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'title'
        )
        model = models.PaymentType

class PaymentSerializer(serializers.ModelSerializer):

    paymentType = PaymentTypeSerializer(read_only=True)

    class Meta:
        fields = (
            'amount',
            'state',
            'paymentType'
        )
        model = models.Payment

class ConsumerSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'email',
            'name',
            'last_name',
            'phone_number',
        )
        model = models.Consumer


class AdminOfferSerializer(serializers.ModelSerializer):

    productType = ProductTypeSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'unit_price',
            'unit_type',
            'count',
            'create_at',
            'delivery_date',
            'productType'
        )
        model = models.AdminOffer

class OrderSerializer(serializers.ModelSerializer):

    consumer = ConsumerSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'delivery_at',
            'shipping_address',
            'consumer',
            'state'
        )
        model = models.Order

class OrderItemSerializer(serializers.ModelSerializer):

    offer = AdminOfferSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        fields = (
            'count',
            'offer',
            'order'
        )
        model = models.Order_Item
