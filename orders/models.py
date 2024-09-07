from django.db import models
from users.models import User
from shop.models import Product


class Order(models.Model):
    stripe_id = models.CharField(max_length=256, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    country = models.ForeignKey('cities_light.Country', on_delete=models.SET_NULL, null=True, blank=True) 
    city = models.ForeignKey('cities_light.City', on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey('cities_light.Region', on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f" The order {self.id} of {self.user.username}"
    
    
    def get_total_sum(self):
        return sum(item.get_cost() for item in self.items.all())
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='order_images', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"The orderItem's{self.id} of order{self.order.id}"
    
    def get_cost(self):
        return self.quantity * self.price    