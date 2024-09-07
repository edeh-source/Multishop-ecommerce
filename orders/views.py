from django.shortcuts import render
from django.contrib import messages
from .forms import OrderForm
from cart.cart import Cart
from django.http import HttpResponse
from .models import Order, OrderItem
from django.contrib.admin.views.decorators import staff_member_required

from .tasks import order_created
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.conf import settings
import os
from shop.models import Product
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import weasyprint

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/admin.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    for item in order.items.all():
        product = Product.objects.get(name=item.product.name)
        images = product.image.all().first()
        print(images)
    html = render_to_string('shop/pdf.html', {'order': order, 'images': images})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
    return response


def order_create(request):
    order = None
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            print(order)
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], image=item['image'], price=item['price'])
                print("This is the item of the product and image inclusive", item['product'])
                print("This is the item", item)
                messages.success(request, 'ORDER CREATED SUCCESSFULLY')
            cart.clear()
            base_url = request.build_absolute_uri()
            order_created.delay(order.id, base_url)
            request.session['order_id'] = order.id
            return redirect('payment')
        
                
        else:
            messages.error(request, 'CORRECT THE ERROR BELOW')
    else:
        form = OrderForm()
    return render(request, 'shop/checkout.html', {'form': form, 'order': order})            
                    
                
