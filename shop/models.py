from django.db import models
import cv2
import uuid
from django.conf import settings
from ckeditor.fields import RichTextField
from django.urls import reverse
from users.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Category(models.Model):
    id = models.UUIDField(unique=True, editable=False, primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, db_index=True)
    image = models.ImageField(upload_to='categories_images')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-name']
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse("category_details", args=[self.slug])
    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            image = cv2.imread(self.image.path)
            image_size = (100, 100)
            image_resize = cv2.resize(image, image_size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.image.path, image_resize)
        else:
            pass    


class ProductImage(models.Model):
    name = models.CharField(max_length=256, db_index=True)
    image = models.ImageField(upload_to='product_images')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):       
        super().save(*args, **kwargs) 
        img = cv2.imread(self.image.path)
        height, width = 630, 900
        dim = (width, height)
        resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
        cv2.imwrite(self.image.path, resized_img)
        
      
    

class Product(models.Model):
    id = models.UUIDField(editable=False, primary_key=True, unique=True, default=uuid.uuid4, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=256, db_index=True)
    slug = models.SlugField(max_length=256, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    featured = models.BooleanField(default=False)
    discount = models.DecimalField(max_digits=10,decimal_places=2)
    special = models.BooleanField(default=False)
    image = models.ManyToManyField(ProductImage, related_name='products')
    active = models.BooleanField(default=True)
    text = models.TextField()
    information = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("product_details", args=[self.id, self.slug])
    
    
    
class Review(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField(blank=True)
    polartity = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} rated {self.product.name} with {self.rating} stars"
    
