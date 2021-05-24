from django.db import models
from shop.models import Product , Category , Variation
from django.urls import reverse
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250 , blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'Cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    product = models.ForeignKey(Product , on_delete=models.CASCADE )
    cart = models.ForeignKey(Cart , on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation , blank=True )
    quantity = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'CartItem'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return str( self.product.name)
