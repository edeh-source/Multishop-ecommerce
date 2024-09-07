from django.shortcuts import render
from django.shortcuts import redirect
from orders.models import Order
from django.conf import settings
import requests
from urllib.parse import urlencode
import json
from django.shortcuts import reverse
import secrets
import requests
import json
from django.http import JsonResponse
from django.http import HttpResponse

api_key = settings.MONNIFY_ENCODED
urls_monnify = 'https://sandbox.monnify.com/api/v1/auth/login'

url = 'https://sandbox.monnify.com/api/v1/auth/login'

def monnify_payment(request):
    order_id = request.session.get('order_id', None)
    order = Order.objects.get(id=order_id)
    success_url = request.build_absolute_uri(reverse('monnify_completed'))
    cancel_url = request.build_absolute_uri(reverse('cancelled'))
    unique_id = secrets.token_urlsafe(16)
    user = request.user
    if request.method == 'POST':
        
        head = {
            "Authorization": f"Basic {api_key}",
            "Content-Type": "application/json"
            }
        
        response = requests.post(url=url, headers=head)
        response_data = response.json()
        access_token = response_data["responseBody"]["accessToken"]    
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        data = {
            "amount": int(order.get_total_sum()),
            "customerName": user.username,
            "customerEmail": user.email,
            "paymentReference": unique_id,
            "paymentDescription": "Payment For Goods",
            "currencyCode": "NGN",
            "contractCode":"0884771654",
            "redirectUrl": success_url,
            "paymentMethods":["CARD","ACCOUNT_TRANSFER"]
            }
        
        datas = json.dumps(data)
        urls = 'https://sandbox.monnify.com/api/v1/merchant/transactions/init-transaction'
        respond = requests.post(url=urls, data=datas, headers=headers)
        if respond.status_code == 200:
            response_data = respond.json()
            payment_url = response_data["responseBody"]["checkoutUrl"]
            return redirect(payment_url)
        else:
            return render(request, 'shop/payment_failed.html', locals())
        
    else:
        return render(request, 'shop/payment.html', locals())
    



def monnify_completed(request):
    order_id = request.session.get('order_id', None)
    order = Order.objects.get(id=order_id)
    reference = request.GET.get('paymentReference', '')

    # Get access token
    head = {
        "Authorization": f"Basic {api_key}",
        "Content-Type": "application/json"
    }
    urls_monnify = 'https://sandbox.monnify.com/api/v1/auth/login'
        
    response = requests.post(url=urls_monnify, headers=head)
    response_data = response.json()
    access_token = response_data["responseBody"]["accessToken"]    
        
    # Get transaction status
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }    
    
    params = {
        "paymentReference": reference
    }
    
    url = 'https://sandbox.monnify.com/api/v2/merchant/transactions/query'
    
    response = requests.get(url=url, params=params, headers=headers)
    
    if response.status_code == 200:
        transaction_status = response.json()
        print(transaction_status)
        # Update order status based on transaction status
        if transaction_status['responseBody']['paymentStatus'] == 'PAID':
            order.paid = True
            order.save()
            return redirect('dashboard')
        else:
            order.paid = False
            order.save()
    else:
        return render(request, 'shop/payment_failed.html', locals())
        
        
    

  
        
        
        
        