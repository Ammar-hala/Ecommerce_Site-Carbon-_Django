from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('' , views.cart_detail , name='cart_detail'),

    path('add/<int:product_id>/' , views.add_cart , name='add_cart'),
    path('add/<int:product_id>/<int:var_id>/' , views.add_cart , name='add_cart_var'),

    path('remove/<int:product_id>/' , views.cart_remove , name='cart_remove'),
    path('remove/<int:product_id>/<int:var_id>/' , views.cart_remove , name='cart_remove_var'),
    path('full_remove/<int:product_id>/' , views.full_remove , name='full_remove'),
    path('full_remove/<int:product_id>/<int:var_id>/' , views.full_remove , name='full_remove_var'),

    path('checkout/', views.checkout_cart , name='checkout'),
]
