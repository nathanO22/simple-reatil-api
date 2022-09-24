from rest_framework import serializers
from .models import Inventory

class InventorySerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField()

    class Meta:
        model = Inventory
        fields = '__all__'

