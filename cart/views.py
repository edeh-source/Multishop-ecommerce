from django.shortcuts import render
from  django.views.decorators.http import require_POST
from shop.models import Product
from django.contrib import messages
from .cart import Cart
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .forms import CART_ADD_PRODUCT_FORM, CART_OVERRIDE_PRODUCT
from django.core.exceptions import ValidationError


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CART_ADD_PRODUCT_FORM(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        quantity = cd['quantity']
        override = cd['override']  
        cart.add(product=product, quantity=quantity,  override_quantity=override)
        messages.success(request, 'PRODUCT ADDED SUCCESSFULLY')
        return redirect('cart_details')
    else:
        messages.error(request, 'ERROR WHILE ADDING PRODUCT')
        
        
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)
    messages.success(request, 'PRODUCT REMOVED SUCCESSFULLY')
    return redirect('cart_details')


def cart_details(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CART_ADD_PRODUCT_FORM(initial={
            'quantity': item['quantity'],
            'override': True
        })
    
    if cart.__len__() <= 0:
        messages.info(request, 'YOUR CART IS EMPTY')
        return redirect('home')
    else:
        pass    
      
    return render(request, 'shop/cart.html', {'cart': cart})
            
    