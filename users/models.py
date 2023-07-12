from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)



def validate_image_size(image):
    max_upload_size = 2 * 1024 * 1024  # 2MB
    if image.size > max_upload_size:
        raise ValidationError("The uploaded image size is too large. Please upload an image smaller than 2MB.")

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None 
    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        default='default.png',
        blank=True,
        null=True,
        validators=[validate_image_size]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()
