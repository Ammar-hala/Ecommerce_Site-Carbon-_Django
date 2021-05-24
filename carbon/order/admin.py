from django.contrib import admin
from .models import Order , OrderItem
# Register your models here.

# DUplicate product is showing on admin page of order... removed by editing tabular.html page and pasting it here in order app.. .see in end of video 19
class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [ # shown on order page of admin
    ('Product', {'fields':['product'],}),
    ('Quantity', {'fields': ['quantity'], }),
    ('Price', {'fields': ['price'], }),
    ]
    readonly_fields = ['product', 'quantity', 'price']
    can_delete = False # to disbale delete option where order items are shown
    max_num = 0 # to remove add another item option


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'emailAddress', 'created']
    list_display_links = ('id', 'name') # on clicking this.. will be redirected to order summary
    search_fields = ['id', 'name', 'emailAddress'] # order can appear when we look these 3 are looked up
    readonly_fields = ['id', 'total', 'emailAddress', 'created', 'name',
                       'city', 'zipcode', ]
    fieldsets = [
        ('ORDER INFORMATION', {'fields': ['id' , 'total', 'created']}),
        ('SHIPPING INFORMATION', {'fields': ['name', 'address', 'city', 'zipcode', 'emailAddress']}),
    ]

    inlines = [ # in order to see order items of order record
        OrderItemAdmin, # in order to see order items of order record
    ]

    def has_delete_permission(self, request, obj=None): # to disable delete in backend
        return False

    def has_add_permission(self, request):
        return False
