from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class DonorProfile(models.Model):
    """Donor Profile model with personal and medical information"""
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
    
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='donor_profile')
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    is_available = models.BooleanField(default=True, help_text="Available for donation")
    last_donation_date = models.DateField(null=True, blank=True)
    medical_conditions = models.TextField(blank=True, help_text="Any medical conditions or allergies")
    profile_photo = models.ImageField(upload_to='donor_photos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.blood_group}"
    
    class Meta:
        db_table = 'donor_profiles'
        verbose_name = 'Donor Profile'
        verbose_name_plural = 'Donor Profiles'
        ordering = ['-created_at']


class DonationHistory(models.Model):
    """Donation history for tracking donor's donations"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    )
    
    donor = models.ForeignKey(DonorProfile, on_delete=models.CASCADE, related_name='donations')
    blood_bank = models.ForeignKey('blood_banks.BloodBank', on_delete=models.SET_NULL, null=True, blank=True)
    donation_date = models.DateField()
    units = models.DecimalField(max_digits=4, decimal_places=2, help_text="Blood units donated")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_donations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donor.user.username} - {self.donation_date} ({self.status})"
    
    class Meta:
        db_table = 'donation_history'
        verbose_name = 'Donation History'
        verbose_name_plural = 'Donation Histories'
        ordering = ['-donation_date']
