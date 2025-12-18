from django.contrib import admin
from .models import BloodBank, BloodInventory


class BloodInventoryInline(admin.TabularInline):
    model = BloodInventory
    extra = 1


@admin.register(BloodBank)
class BloodBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'phone_number', 'email', 'is_active']
    list_filter = ['is_active', 'city']
    search_fields = ['name', 'city', 'email']
    inlines = [BloodInventoryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'zip_code')
        }),
    )


@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ['blood_bank', 'blood_group', 'units_available', 'last_updated']
    list_filter = ['blood_group', 'blood_bank']
    search_fields = ['blood_bank__name']
