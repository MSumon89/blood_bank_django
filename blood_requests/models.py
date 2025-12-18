from django.db import models
from django.conf import settings


class BloodRequest(models.Model):
    """Blood Request model for managing blood requests"""
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
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('fulfilled', 'Fulfilled'),
    )
    
    URGENCY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )
    
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blood_requests')
    patient_name = models.CharField(max_length=200)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    units_required = models.DecimalField(max_digits=4, decimal_places=2)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    hospital_name = models.CharField(max_length=200)
    hospital_address = models.TextField()
    city = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    reason = models.TextField(help_text="Reason for blood requirement")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    requested_date = models.DateTimeField(auto_now_add=True)
    required_by_date = models.DateField()
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requests')
    approved_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.patient_name} - {self.blood_group} ({self.status})"
    
    class Meta:
        db_table = 'blood_requests'
        verbose_name = 'Blood Request'
        verbose_name_plural = 'Blood Requests'
        ordering = ['-requested_date']
