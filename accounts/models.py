from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with role-based access"""
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('donor', 'Donor'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='donor')
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
