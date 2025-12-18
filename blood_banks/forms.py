from django import forms
from .models import BloodBank, BloodInventory


class BloodBankForm(forms.ModelForm):
    """Blood bank form"""
    class Meta:
        model = BloodBank
        fields = ['name', 'address', 'city', 'state', 'zip_code', 'phone_number', 'email', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class BloodInventoryForm(forms.ModelForm):
    """Blood inventory form"""
    class Meta:
        model = BloodInventory
        fields = ['blood_bank', 'blood_group', 'units_available']
        widgets = {
            'blood_bank': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'units_available': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
