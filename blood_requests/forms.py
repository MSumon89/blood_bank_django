from django import forms
from .models import BloodRequest


class BloodRequestForm(forms.ModelForm):
    """Blood request form"""
    class Meta:
        model = BloodRequest
        fields = ['patient_name', 'blood_group', 'units_required', 'urgency', 
                  'hospital_name', 'hospital_address', 'city', 'contact_number', 
                  'reason', 'required_by_date']
        widgets = {
            'patient_name': forms.TextInput(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'units_required': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'urgency': forms.Select(attrs={'class': 'form-control'}),
            'hospital_name': forms.TextInput(attrs={'class': 'form-control'}),
            'hospital_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'required_by_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class BloodRequestUpdateForm(forms.ModelForm):
    """Form for admin to update blood request status"""
    class Meta:
        model = BloodRequest
        fields = ['status', 'rejection_reason', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
