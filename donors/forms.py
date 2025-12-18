from django import forms
from .models import DonorProfile, DonationHistory


class DonorProfileForm(forms.ModelForm):
    """Donor profile form"""
    class Meta:
        model = DonorProfile
        fields = ['blood_group', 'date_of_birth', 'gender', 'address', 'city', 'state', 'zip_code', 
                  'is_available', 'medical_conditions', 'profile_photo']
        widgets = {
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'medical_conditions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'profile_photo': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DonationHistoryForm(forms.ModelForm):
    """Donation history form"""
    class Meta:
        model = DonationHistory
        fields = ['blood_bank', 'donation_date', 'units', 'notes']
        widgets = {
            'blood_bank': forms.Select(attrs={'class': 'form-control'}),
            'donation_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'units': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
