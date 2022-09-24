from email.policy import default
from django.db import models
from accounts.models import User
from datetime import datetime
from django.forms import model_to_dict

from retail_api.models import Inventory

class Cart(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.now)

class CartItem(models.Model):
    products = models.ForeignKey(Inventory, related_name='products', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', related_name='cart', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    def __str__(self):
        return  self.cart + " - " + self.products

    @property
    def cart_content(self):
        return model_to_dict(self.products, fields=['item_name', 'price'])

    cost = cart_content
    price = cost