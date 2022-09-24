from rest_framework import serializers
from retail_api.serializers import InventorySerializer
from .models import Cart, CartItem
# Inv =InventorySerializer

class CartSerializer(serializers.ModelSerializer):
    cart= serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = '__all__'

class Cart_Serializer(serializers.ModelSerializer):
    cart_content = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['products', 'quantity', 'cart_content']