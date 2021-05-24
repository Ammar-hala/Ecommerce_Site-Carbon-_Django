from django.db import models
from django.urls import reverse
# Create your models here.

gender_opts = ( ('M' , 'M') , ('F' , 'F') , )

class Category(models.Model):
    name = models.CharField(max_length=255 , unique=True) # add an M or F at the end of category name to differentiate from male and female
    slug = models.SlugField(max_length=50)
    gender = models.CharField(max_length=10 , choices=gender_opts , default='M')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='category' , blank=True)

    class Meta():
        ordering = ['name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        db_table = 'category'

    def get_url(self):
        return reverse('shop:products_by_category' , args=[self.gender , self.slug] )

    def __str__(self):
        return '{}'.format(self.name)


class Product(models.Model):
    name = models.CharField(max_length=255 , unique=True)
    slug = models.SlugField(max_length=255 , unique=True)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product' , blank=True)
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    stock = models.IntegerField()
    availible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)  # when prod is upadted it will change time to current time

    class Meta():
        ordering = ['name']
        verbose_name = 'product'
        verbose_name_plural = 'products'
        db_table = 'product'

    def get_url(self):
        return reverse('shop:ProdCatDetail' , args=[self.category.gender , self.category.slug , self.slug] )

    def __str__(self):
        return '{}'.format(self.name)


class VariationManager(models.Manager):
	def all(self):
		return super(VariationManager, self).filter(active=True)

	def sizes(self):
		return self.all().filter(category='size')


VAR_CATEGORIES = ( ('size' , 'size') , )

sizes = ( ('Small' , 'Small') , ('Medium' , 'Medium') , ('Large' , 'Large') , )

class Variation(models.Model):
    title = models.CharField(max_length=256, choices=sizes)
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    category = models.CharField(max_length=125 , choices=VAR_CATEGORIES , default='size')
    active = models.BooleanField(default=True)
    stock = models.IntegerField()

    objects = VariationManager()

    def __str__(self):
        return '{}'.format(self.title)
