from django.contrib import admin
from .models import BloodRequest


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ['patient_name', 'blood_group', 'units_required', 'urgency', 'status', 'requested_date', 'required_by_date']
    list_filter = ['status', 'urgency', 'blood_group', 'requested_date']
    search_fields = ['patient_name', 'hospital_name', 'requester__username', 'requester__email']
    readonly_fields = ['requested_date', 'approved_date']
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('requester', 'patient_name', 'blood_group', 'units_required', 'urgency')
        }),
        ('Hospital Information', {
            'fields': ('hospital_name', 'hospital_address', 'city', 'contact_number')
        }),
        ('Request Details', {
            'fields': ('reason', 'required_by_date', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'approved_date', 'rejection_reason')
        }),
        ('Timestamps', {
            'fields': ('requested_date',),
            'classes': ('collapse',)
        }),
    )
