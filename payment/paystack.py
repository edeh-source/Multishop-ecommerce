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
from .tasks import payment_completed

api_key = settings.PAYSTACK_SECRET_KEY
url = "https://api.paystack.co/transaction/initialize"

def paystack_payment(request):
    order_id = request.session.get('order_id', None)
    order = Order.objects.get(id=order_id)
    success_url = request.build_absolute_uri(reverse('paystack_complete'))
    cancel_url = request.build_absolute_uri(reverse('cancelled'))
    user = request.user
    unique_id = secrets.token_urlsafe(16)
    if request.method == 'POST':
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "email": user.email,
            "amount": int(order.get_total_sum() * 100),
            "reference": unique_id,
            "currency": "NGN",
            "callback_url": success_url,
            }
        
        data_json = json.dumps(data)    
        response = requests.post(url=url, data=data_json, headers=headers) 
        if response.status_code == 200:
            response_data = response.json()
            payment_url = response_data["data"]["authorization_url"]
            return redirect(payment_url)
        else:
            pass
        
            
    else:
        return render(request, 'shop/payment.html', locals()) 
    
    
# views.py



def paystack_completed(request):
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
                base_url = request.build_absolute_uri()
                payment_completed.delay(order.id, base_url)
                return redirect('dashboard')
            else:
                return render(request, 'shop/payment_failed.html', {'error': 'Payment verification failed'})
        else:
            return render(request, 'shop/payment_failed.html', {'error': 'Payment verification failed'})
           

    except requests.exceptions.RequestException as e:
        return render(request, 'shop/payment_failed.html', {'error': 'Payment verification failed'})    
    
#def paystack_completed(request):
    order_id = request.session.get('order_id', None)
    order = Order.objects.get(id=order_id)
    print(order)
    
    reference = request.GET.get('reference', '')
    
    base_url = "https://api.paystack.co/transaction/verify/{reference}"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url=base_url, headers=headers)
    
    if response.status_code == 200:
        print(response.status_code)
        response_data = response.json()
        if response_data["data"]["status"] == "success":
            order.paid = True
            print(order.paid)
            base_url = request.build_absolute_uri()
            payment_completed_task.delay(order.id, base_url)
            return render(request, 'shop/completed.html', {'order': order})
        else:
            # Return an error message or a failure page
            return render(request, 'shop/payment_failed.html', {'error': 'Payment failed'})
    else:
        # Return an error message or a failure page
        return render(request, 'shop/payment_failed.html', {'error': 'Payment verification failed'})
        
        
        
        

    
    