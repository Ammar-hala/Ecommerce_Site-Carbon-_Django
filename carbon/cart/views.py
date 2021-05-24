from django.shortcuts import render , redirect , get_object_or_404
from django.core.exceptions import ObjectDoesNotExist

from shop.models import Product , Variation
from .models import Cart , CartItem
from .forms import CheckoutForm

from django.conf import settings

# FOr EMAIL
from django.template.loader import get_template
from django.core.mail import EmailMessage

from order.models import Order , OrderItem

#to check if a session id has been created on the customer browser
def _cart_id(request):
    cart = request.session.session_key
    if not cart: # if cart is not created
        cart = request.session.create() #create a session in cart

    return cart #returning session key


def add_cart(request , product_id , var_id = None):
    product = Product.objects.get(id=product_id)

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request) )

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id = _cart_id(request) )
        cart.save()

    product_var = [] #when a product is added first time with var... this used

    if request.method == 'POST':
        for item in request.POST:
            key = item
            val = request.POST[key]

            try:
                v = Variation.objects.get(product = product , title__iexact=val , category__iexact=key)
                product_var.append(v)

                if( len(product_var) > 0 ):
                    try:
                        cart_item = CartItem.objects.get(product=product , cart=cart , variations__id = v.id )

                        if cart_item.quantity < v.stock:
                            cart_item.quantity += 1

                    except CartItem.DoesNotExist:
                        cart_item = CartItem.objects.create(product=product , cart=cart , quantity=1)
                        cart_item.variations.add(*product_var)

                    cart_item.save()
                    return redirect('cart:cart_detail')

            except:
                pass


    try:
        if(var_id):
            v = Variation.objects.get(id=var_id , product = product)
            cart_item = CartItem.objects.get(product=product , cart=cart , variations__id = var_id )

            if cart_item.quantity < v.stock: # quantity dose not increase on pressing add to cart if already added. and got all products
                cart_item.quantity += 1


        else:
            cart_item = CartItem.objects.get(product=product , cart=cart)

            if cart_item.quantity < cart_item.product.stock: # quantity dose not increase on pressing add to cart if already added. and got all products
                cart_item.quantity += 1

        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product , cart=cart , quantity=1)
        cart_item.save()

    return redirect('cart:cart_detail')



def cart_detail(request , total=0 , counter=0 , cart_items=None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request) )
        cart_items = CartItem.objects.filter(cart=cart , active=True)

        for cart_item in cart_items:
            for a in cart_item.variations.all():
                print('var_id = ',a.id)
            counter += cart_item.quantity
            total += (cart_item.quantity * cart_item.product.price)

    except ObjectDoesNotExist:
        pass

    description = 'Carbon Shop - New Order'

    return render(request, 'cart/cart.html', dict(cart_items = cart_items, total = total, counter = counter, description = description))



def checkout_cart(request , total=0 , counter=0 , cart_items=None):
    context = {}
    form = CheckoutForm()
    context['form'] = form

    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart , active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity

    except ObjectDoesNotExist:
        pass


    if request.GET:
        name = request.GET['name']
        email = request.GET['email']
        address = request.GET['address']
        city = request.GET['city']
        if city == 'K':
            city = 'Karachi'
        else:
            city = 'Lahore'
#        print(city)
        zip = request.GET['zip']

        #Creatin the Order
        try:
            order_details = Order.objects.create(
                    name = name,
                    emailAddress = email,
                    address = address,
                    city = city,
                    zipcode = zip,
                    total = total,
                    )
            order_details.save()

            for order_item in cart_items: # creating ordder item record for each item
                  oi = OrderItem.objects.create(
                      product=order_item.product.name,
                      quantity=order_item.quantity,
                      price=order_item.product.price,
                      order=order_details
                    )
                  oi.save()

                  var_id = None 

                  for a in order_item.variations.all(): # through this.. can access attrib of m2m field
                      var_id = a.id

                  # Reduce Stock Level when order is placed or saved
                  products = Product.objects.get(id=order_item.product.id) # or product_id ?


                  if(var_id):
                      v = Variation.objects.get(id=var_id , product = products)

                  products.stock = int(order_item.product.stock - order_item.quantity)

                  if(var_id):
                      v.stock = int(v.stock - order_item.quantity)
                      if v.stock <= 0:
                          v.active = False

                      v.save()

                  products.save()
                  order_item.delete()
                  # The terminal will print message when the order is saved
                  print('The Order has been created')

            '''
            Calling the Send Email Function
            '''
            try:
                sendEmail(order_details.id)
                print('Email has been sent')

            except IOError as e:
                return e

            return redirect('order:thanks' , order_details.id)

        except ObjectDoesNotExist:
            pass



#        return redirect('cart:cart_detail')



    return render(request, 'cart/checkout.html' , context)






def cart_remove(request , product_id , var_id = None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product , id=product_id) # getting a specific product
    print('var_id = ',var_id)

    if(var_id):
        cart_item = CartItem.objects.get(cart=cart , product=product , variations__id=var_id) # item for a specific product
    else:
        cart_item = CartItem.objects.get(cart=cart , product=product)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()

    return redirect('cart:cart_detail')


# For trash icon
def full_remove(request , product_id , var_id = None):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product , id=product_id) # getting a specific product
    print('var_id = ',var_id)
    if(var_id):
        cart_item = CartItem.objects.get(cart=cart , product=product , variations__id=var_id) # item for a specific product
    else:
        cart_item = CartItem.objects.get(cart=cart , product=product)

    cart_item.delete()
    return redirect('cart:cart_detail')





# this function is called in checkout function
def sendEmail(order_id):
    # Use order id to get the Order object and the OrderItems
    transaction = Order.objects.get(id=order_id)
    order_items = OrderItem.objects.filter(order=transaction)

    try:
        # Sending order to costumer
        subject = "HHA Outlet - New Order #{}".format(transaction.id)
        to = ['{}'.format(transaction.emailAddress)]
        from_email = 'orders@perfectcushionstore.com'
        order_info = {
            'transaction': transaction,
            'order_items': order_items
        }
        message = get_template('email/email.html').render(order_info) # Render html template with order_info context
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()

    except IOError as e:
        print(e)
        return e
