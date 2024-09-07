from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('category/<slug:slug>/', views.Category_details.as_view(), name='category_details'),
    path('dashboard/', views.users_dashboard, name='dashboard'),
    path('detail/<uuid:id>/<slug:slug>/', views.get_product_detail, name='product_details'),
]
