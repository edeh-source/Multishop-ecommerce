from django.urls import path
from . import views
from . import paystack
from . import webhooks
from . import opay
from . import monnify
from . import paypal
urlpatterns = [
    path('process/', views.payment_process, name='payment'),
    path('paystack/', paystack.paystack_payment, name='paystack'),
    path('paystack_complete/', paystack.paystack_completed, name='paystack_complete'),
    path('cancelled/', views.payment_canceled, name='cancelled'),
    path('opay/', opay.opay_payment, name='opay_payment'),
    path('opay_completed/', opay.opay_completed, name='opay_complete'),
    path('opay_cancelled/', opay.opay_cancelled, name='opay_cancelled'),
    path('monnify_completed/', monnify.monnify_completed, name='monnify_completed'),
    path('complete/',views.payment_completed, name='completed'),
    path('create_payment/', paypal.create_payment, name='create_payment'),
    path('payment_failed/', paypal.payment_failed, name='payment_failed'),
    path('execute_payment/', paypal.execute_payment, name='execute_payment'),
    path('monnify/', monnify.monnify_payment, name='monnify'),
    path('webhook/', webhooks.stripe_webhook, name='stripe-webhook'),
    
]
