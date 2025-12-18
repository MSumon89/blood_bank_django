from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('profile/create/', views.donor_profile_create, name='donor_profile_create'),
    path('profile/update/', views.donor_profile_update, name='donor_profile_update'),
    path('profile/', views.donor_profile_view, name='donor_profile_view'),
    path('donations/', views.donation_history_list, name='donation_history_list'),
    path('donations/create/', views.donation_create, name='donation_create'),
    path('search/', views.donor_search, name='donor_search'),
]
