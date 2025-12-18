from django.contrib import admin
from .models import DonorProfile, DonationHistory


@admin.register(DonorProfile)
class DonorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'blood_group', 'city', 'is_available', 'last_donation_date']
    list_filter = ['blood_group', 'is_available', 'city', 'gender']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Donor Details', {
            'fields': ('blood_group', 'date_of_birth', 'gender', 'is_available')
        }),
        ('Contact Information', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
        ('Medical Information', {
            'fields': ('medical_conditions', 'last_donation_date')
        }),
        ('Profile', {
            'fields': ('profile_photo',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DonationHistory)
class DonationHistoryAdmin(admin.ModelAdmin):
    list_display = ['donor', 'donation_date', 'units', 'blood_bank', 'status', 'approved_by']
    list_filter = ['status', 'donation_date', 'blood_bank']
    search_fields = ['donor__user__username', 'donor__user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor', 'blood_bank')
        }),
        ('Donation Details', {
            'fields': ('donation_date', 'units', 'notes')
        }),
        ('Status', {
            'fields': ('status', 'approved_by')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    list_filter = ['status', 'donation_date']
    search_fields = ['donor__user__username', 'donor__user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Donation Information', {
            'fields': ('donor', 'blood_bank', 'donation_date', 'units')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
