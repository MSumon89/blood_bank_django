from django.db import models


class BloodBank(models.Model):
    """Blood Bank model for managing blood banks"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'blood_banks'
        verbose_name = 'Blood Bank'
        verbose_name_plural = 'Blood Banks'
        ordering = ['name']


class BloodInventory(models.Model):
    """Blood Inventory model for tracking blood units by group"""
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    
    blood_bank = models.ForeignKey(BloodBank, on_delete=models.CASCADE, related_name='inventory')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_available = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.blood_bank.name} - {self.blood_group}: {self.units_available} units"
    
    class Meta:
        db_table = 'blood_inventory'
        verbose_name = 'Blood Inventory'
        verbose_name_plural = 'Blood Inventories'
        unique_together = ['blood_bank', 'blood_group']
        ordering = ['blood_bank', 'blood_group']
