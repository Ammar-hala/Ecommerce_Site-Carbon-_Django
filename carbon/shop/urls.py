from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('' , views.allProdCat , name='allProdCat'),
    path('M/' , views.maleProdCat , name='maleProdCat'),
    path('F/' , views.femaleProdCat , name='femaleProdCat'),
    path('<str:c_gender>/<slug:c_slug>/' , views.allProdCat , name='products_by_category'),
    path('<str:c_gender>/<slug:c_slug>/<slug:product_slug>/' , views.ProdCatDetail , name='ProdCatDetail'),
]
