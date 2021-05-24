from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator , EmptyPage , InvalidPage

from .models import Category , Product
# Create your views here.

def index(request):
    return allProdCat(request)

# gets all products for home page or products of a particular category
def allProdCat(request , c_gender = None , c_slug = None):
    c_page = None
    products_list = None

    if c_slug != None: # provided from url
        c_page = get_object_or_404(Category , gender=c_gender , slug=c_slug) # get category object
        products_list = Product.objects.filter(category=c_page , availible=True)

    else:
        products_list = Product.objects.all().filter(availible=True)


    # Pagination code
    paginator = Paginator(products_list, 10) # 6 products per page
    try:
        page = int(request.GET.get('page', '1')) #getting page 1
    except:
        page = 1
    try:
        products = paginator.page(page) #page will be first (1)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages) #total number of pages

    return render(request , 'shop/category.html' , {'category' : c_page , 'products' : products} )



#Product Detail view
def ProdCatDetail(request , c_gender , c_slug , product_slug):
    try:
        product = Product.objects.get(category__gender=c_gender , category__slug=c_slug , slug=product_slug)

    except Exception as e:
        raise e

    return render(request , 'shop/product.html' , {'product':product} )

# FOR MALE AND FEMALE ALL PRODUCTS LISTING

def maleProdCat(request):
    c_page = None
    products_list = None

    products_list = Product.objects.filter(category__gender = 'M' , availible=True)

#    else:
#        products_list = Product.objects.all().filter(availible=True)


    # Pagination code
    paginator = Paginator(products_list, 10) # 6 products per page
    try:
        page = int(request.GET.get('page', '1')) #getting page 1
    except:
        page = 1
    try:
        products = paginator.page(page) #page will be first (1)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages) #total number of pages

    return render(request , 'shop/category.html' , {'category' : c_page , 'products' : products} )



def femaleProdCat(request):
    c_page = None
    products_list = None

    products_list = Product.objects.filter(category__gender = 'F' , availible=True)


    # Pagination code
    paginator = Paginator(products_list, 10) # 6 products per page
    try:
        page = int(request.GET.get('page', '1')) #getting page 1
    except:
        page = 1
    try:
        products = paginator.page(page) #page will be first (1)
    except (EmptyPage, InvalidPage):
        products = paginator.page(paginator.num_pages) #total number of pages

    return render(request , 'shop/category.html' , {'category' : c_page , 'products' : products} )
