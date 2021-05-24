from django.db import models

# Create your models here.
class Order(models.Model): # will be got from stripe
    name = models.CharField(max_length=250 , blank=True)
    emailAddress = models.EmailField(max_length=250 , blank=True , verbose_name='Email Address')
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=250 , blank=True)
    total = models.DecimalField(max_digits=10 , decimal_places=2 , verbose_name='Rs Order Total')
    city = models.CharField(max_length=250 , blank=True)
    zipcode = models.CharField(max_length=10 , blank=True)

    class Meta():
        db_table = 'Order'
        ordering = ['-created']

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.CharField(max_length=250)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10 , decimal_places = 2 , verbose_name='Rs Price')
    order = models.ForeignKey(Order , on_delete=models.CASCADE)

    class Meta():
        db_table = 'OrderItem'

    def sub_total(self):
        return (self.price * self.quantity)

    def __str__(self):
        return self.product
