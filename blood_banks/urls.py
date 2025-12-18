from django.urls import path
from . import views

urlpatterns = [
    # Admin dashboard
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Blood banks
    path('blood-banks/', views.blood_bank_list, name='blood_bank_list'),
    path('blood-banks/create/', views.blood_bank_create, name='blood_bank_create'),
    path('blood-banks/<int:pk>/update/', views.blood_bank_update, name='blood_bank_update'),
    path('blood-banks/<int:pk>/delete/', views.blood_bank_delete, name='blood_bank_delete'),
    
    # Blood inventory
    path('inventory/', views.blood_inventory_list, name='blood_inventory_list'),
    path('inventory/create/', views.blood_inventory_create, name='blood_inventory_create'),
    path('inventory/<int:pk>/update/', views.blood_inventory_update, name='blood_inventory_update'),
    
    # Donors management (Admin)
    path('admin/donors/', views.donors_list, name='admin_donors_list'),
    
    # Donation approvals
    path('admin/donations/pending/', views.donation_approval_list, name='donation_approval_list'),
    path('admin/donations/<int:pk>/approve/', views.donation_approve, name='donation_approve'),
    path('admin/donations/<int:pk>/reject/', views.donation_reject, name='donation_reject'),
]
