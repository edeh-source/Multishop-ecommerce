from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from orders.models import Order, OrderItem
from django.views.generic.list import ListView
from textblob import TextBlob
from shop.forms import RatingForm
from .recommendations import get_top_recommendations
from .models import Product, Category, Review
from django.db.models import Count
from .filters import  ProductFilterSet
from cart.forms import CART_ADD_PRODUCT_FORM
from django.contrib import messages
from django.views.decorators.http import require_POST
from django_filters.views import FilterView
from django.shortcuts import get_object_or_404

class HomePage(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'shop/index.html'
    
    def get_queryset(self):
        return Product.objects.filter(active=True, featured=False).exclude(special=True).order_by('-created')[:20]
    
    
def category_details(request):
    category = Category.objects.annotate(categories_count=Count('products'))    
    return {'category': category}



def get_product_detail(request, id, slug):
    form = CART_ADD_PRODUCT_FORM()
    rating = None
    user_id = request.user.id  # Assuming the user is logged in
    product_det = get_object_or_404(Product, id=id, slug=slug)
    recommendations = get_top_recommendations(user_id)
    print("This is the recommendations", recommendations)
    recommended_products = []
    for rec in recommendations:
        try:
            prod = Product.objects.get(id=rec[0])  # Assuming rec[0] is the product ID
            recommended_products.append(prod)
        except Product.DoesNotExist:
            continue  # Skip if product doesn't exist
    ratings = Review.objects.filter(product=product_det)
    print(ratings)
    if request.method == 'POST':
        forms = RatingForm(request.POST)
        if forms.is_valid():
            rating = forms.save(commit=False)
            rating.user = request.user
            rating.product = product_det
            review_text = forms.cleaned_data['review']
            blob = TextBlob(review_text)
            if blob.sentiment.polarity > 0:
                rating.polartity = True
            elif blob.sentiment.polarity < 0:  
                rating.polartity = False
            messages.success(request, 'REVIEW DROPPED SUCCESSFULLY')
            rating.save()
        else:
            messages.error(request, 'ERROR WHILE SUBMITTING REVIEW')    
    else:
                
        form = CART_ADD_PRODUCT_FORM()
        forms = RatingForm()
    return render(request, 'shop/detail.html', {'product_det': product_det, 'form': form, 'forms': forms, 'rating': rating, 'ratings': ratings, 'recommended_products': recommended_products})

class Category_details(FilterView):
    model = Product
    context_object_name = 'products'
    filterset_class = ProductFilterSet
    template_name = 'shop/shop.html'
    paginate_by = 6
    
    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs['slug'])
        products = Product.objects.filter(category=category, active=True)
        return products
    
    
def get_special_product(request):
    special = Product.objects.filter(special=True).order_by('-created')[:2]
    return {'special': special}    

def get_special(request):
    product_special = Product.objects.filter(special=True).order_by('-created')[:4]
    return {'product_special': product_special}

def get_recent_product(request):
    recent_products = Product.objects.filter(featured=True).exclude(special=True).order_by('-created')[:20]
    return {'recent_products': recent_products}


def users_dashboard(request):
    user = request.user
    order = OrderItem.objects.filter(order__user=user, order__paid=True).order_by('-created')
    print(order)
    return render(request, 'shop/dashboard.html', {'user': user, 'order': order})