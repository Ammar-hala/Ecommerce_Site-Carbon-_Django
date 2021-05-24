from django.shortcuts import render
from shop.models import Product
from django.db.models import Q
from django.core.paginator import Paginator , EmptyPage , InvalidPage , PageNotAnInteger
# Create your views here.

def searchResult(request):
    products_list = None
    query = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        query = query.capitalize()
        products_list = Product.objects.all().filter( Q(name__contains=query) | Q(description__contains=query) | Q(category__name__contains=query) )

    #PAGINATOR
    paginator = Paginator(products_list, 9) # 9 posts per page
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    return render(request , 'search_app/search.html' , {'query':query , 'products':products} )
