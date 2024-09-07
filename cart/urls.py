from django.urls import path

from . import views


urlpatterns = [
    path('add/<uuid:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<uuid:product_id>/', views.cart_remove, name='cart_remove'),
    path('', views.cart_details, name='cart_details'),
]