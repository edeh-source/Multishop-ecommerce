from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import ValidationError
import uuid
from django.core.exceptions import ValidationError
import cv2
from phone_field import PhoneField


class UserManager(BaseUserManager):
    """
    A Class Used in creating a User 
    """
    def create_user(self, username, email, phone_number, password, **kwargs):
        if username is None:
            raise ValidationError("User Must Have A Username")
        if email is None:
            raise ValidationError("User Must Have An Email")
        if phone_number is None:
            raise ValidationError("User Must Have A phone Number")
        if password is None:
            raise ValidationError("User Must Have A Password")
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, phone_number, password, **kwargs):
        if username is None:
            raise ValidationError("User Must Have A Username")
        if email is None:
            raise ValidationError("User Must Have An Email")
        if phone_number is None:
            raise ValidationError("User Must Have A phone Number")
        if password is None:
            raise ValidationError("User Must Have A Password")
        user = self.model(username=username, email=self.normalize_email(email), phone_number=phone_number, **kwargs)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid.uuid4)
    username = models.CharField(max_length=256, db_index=True, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    email = models.EmailField(unique=True, max_length=256)
    phone_number = PhoneField()
    image = models.ImageField(upload_to='users_Images')
    bio = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
    @property
    def name(self):
        return f"{self.first_name} {self.username}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            image = cv2.imread(self.image.path)
            image_size = (100, 100)
            image_resize = cv2.resize(image, image_size, interpolation=cv2.INTER_AREA)
            cv2.imwrite(self.image.path, image_resize)
        else:
            pass    
    
    objects = UserManager()
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'phone_number']
   
    
    
    
    
    