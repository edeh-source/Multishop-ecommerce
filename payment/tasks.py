from celery import  shared_task
from django.core.mail import send_mail
from orders.models import Order
from io import BytesIO
from shop.models import Product
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import EmailMessage




@shared_task
def payment_completed(order_id, base_url):
    """
    A Task to send an e-mail notification when an order is created successfully
    """
    order = Order.objects.get(id=order_id)
    for item in order.items.all():
        product = Product.objects.get(name=item.product.name)
        images = product.image.all().first()
        print(images)
    subject = f'MULTI SHOP - INVOICE NUMBER {order.id}'
    message = 'Please, Find attached the invoice for your recent purchase'
    email = EmailMessage(subject, message, 'edehchetachukwu23@gmail.com', [order.user.email])
    html = render_to_string('shop/pdf.html', {'order': order, 'images': images})
    out = BytesIO()
    weasyprint.HTML(string=html, base_url=base_url).write_pdf(out)
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    email.send()  