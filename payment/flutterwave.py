import secrets
import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse
from orders.models import Order
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

def flutterwave_payment(request):
    user = request.user
    unique_id = secrets.token_urlsafe(16)
    order_id = request.session.get('order_id', None)
    
    if not order_id:
        return HttpResponse("Order ID not found in session.", status=400)
    
    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return HttpResponse("Order does not exist.", status=404)
    
    success_url = request.build_absolute_uri(reverse('flutterwave_complete'))
    auth_token = env('FLUTTERWAVE_SECRET_KEY')
    
    if not auth_token:
        return HttpResponse("Flutterwave Secret Key not found in environment variables.", status=500)
    
    print(f"Auth Token: {auth_token}")  # Debugging line to check the auth token
    
    if request.method == 'POST':
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Content-Type": "application/json"
        }

        data = {
            "tx_ref": unique_id,
            "amount": str(order.get_total_sum()),
            "currency": "NGN",
            "redirect_url": success_url,
            "payment_options": "card",
            "meta": {
                "consumer_id": str(user.id),
                "consumer_mac": "92a3-912ba-1192a"
            },
            "customer": {
                "email": user.email,
                "name": user.username
            },
            "customizations": {
                "title": "Supa Electronics Store",
                "description": "Best store in town",
                "logo": "https://getbootstrap.com/docs/4.0/assets/brand/bootstrap-solid.svg"
            }
        }

        json_data = json.dumps(data)
        url = "https://api.flutterwave.com/v3/payments"

        try:
            response = requests.post(url=url, data=json_data, headers=headers, timeout=30)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            
            response_data = response.json()
            payment_url = response_data["data"]["link"]
            return HttpResponseRedirect(payment_url)
        except requests.exceptions.HTTPError as e:
            print(f"HTTPError: {e.response.status_code} - {e.response.text}")  # Debugging line for HTTP errors
            if e.response.status_code == 403:
                return HttpResponse("Authentication failed. Please check your API key.", status=403)
            elif e.response.status_code == 400:
                return HttpResponse("Bad request. Please check your request data.", status=400)
            else:
                return HttpResponse(f"An error occurred: {str(e)}", status=e.response.status_code)
        except requests.exceptions.ConnectionError as e:
            print(f"ConnectionError: {str(e)}")  # Debugging line for connection errors
            return HttpResponse(f"A network error occurred: {str(e)}", status=500)
        except requests.exceptions.Timeout as e:
            print(f"Timeout: {str(e)}")  # Debugging line for timeout errors
            return HttpResponse(f"Request timed out: {str(e)}", status=500)
        except Exception as e:
            print(f"Exception: {str(e)}")  # Debugging line for general exceptions
            return HttpResponse(f"An unexpected error occurred: {str(e)}", status=500)
    else:
        return render(request, 'shop/payment.html', locals())

def flutterwave_complete(request):
    return render(request, 'shop/completed.html')
