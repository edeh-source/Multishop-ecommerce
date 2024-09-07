import requests
from django.conf import settings
from orders.models import Order
from django.shortcuts import reverse
import secrets
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json
from django.shortcuts import render
from django.shortcuts import redirect



api_key = settings.OPAY_PUBLIC_KEY
merchant_id = settings.OPAY_MERCHANT_ID
url = "https://sandboxapi.opaycheckout.com/api/v1/international/cashier/create"

def opay_payment(request):
    order_id = request.session.get('order_id', None)
    order = Order.objects.get(id=order_id)
    success_url = request.build_absolute_uri(reverse('opay_complete'))
    cancel_url = request.build_absolute_uri(reverse('opay_cancelled'))
    user = request.user
    unique_id = secrets.token_urlsafe(16)
    if request.method == 'POST':
        headers = {
            "Authorization": f"Bearer {api_key}",
            "MerchantId": merchant_id,
            "Content-Type": "application/json"
        }
        for item in order.items.all():
            
            data = {
                "country": "EG",
                "reference": unique_id,
                "amount": {
                    "total": int(order.get_total_sum() * 100),
                    "currency": "EGP"
                },
                "returnUrl": success_url,
                "callbackUrl": success_url,
                "userInfo":{
                    "userEmail": user.email,
                    "userId": str(user.id),
                    "userMobile": str(user.phone_number),
                    "userName": str(user.username)
                },
                "productList":[
                    {
                        "productId": str(item.product.id),
                        "name": str(item.product.name),
                        "price": int(item.price),
                        "quantity": int(item.quantity),
                        "description": "description",
                        
                    }
                ],
                "payMethod":"BankCard"
            }
            
            json_data = json.dumps(data)
            response = requests.post(url=url, data=json_data, headers=headers) 
            if response.status_code == 200:
                response_data = response.json()
                print(response_data)
                payment_url = response_data["data"]["cashierUrl"]
                return redirect(payment_url)
            else:
                pass
        
    else:
        
        return render(request, 'shop/payment.html', locals()) 
        
    
    

def opay_cancelled(request):
    return render(request, 'shop/payment_failed.html')


def opay_completed(request):
    order_id = request.session.get('order_id', None)
    order = Order.objects.get(id=order_id)
    print(order)
    # Get the reference from the URL parameters
    reference = request.GET.get('reference', '')
    print("This is the reference: ",reference)

    if not reference:
        return JsonResponse({'status': 'failed', 'message': 'No reference provided'}, status=400)

    # Construct the Paystack verification URL
    url = f'https://api.paystack.co/transaction/verify/{reference}'

    # Set up the headers with your secret key
    headers = {
        'Authorization': f'Bearer {api_key}',
    }

    try:
        # Make a GET request to Paystack
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()
            
            # Check the status of the transaction
            if response_data['data']['status'] == 'success':
                order.paid = True
                order.save()
                return redirect('dashboard')
            else:
                return render(request, 'shop/payment_failed.html', {'error': 'Payment verification failed'})
        else:
            return render(request, 'shop/payment_failed.html', {'error': 'Payment verification failed'})
           

    except requests.exceptions.RequestException as e:
        return render(request, 'shop/payment_failed.html', {'error': 'Payment verification failed'})    
    