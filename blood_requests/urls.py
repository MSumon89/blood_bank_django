from django.urls import path
from . import views

urlpatterns = [
    path('', views.blood_request_list, name='blood_request_list'),
    path('create/', views.blood_request_create, name='blood_request_create'),
    path('<int:pk>/', views.blood_request_detail, name='blood_request_detail'),
    path('<int:pk>/update/', views.blood_request_update, name='blood_request_update'),
    path('<int:pk>/delete/', views.blood_request_delete, name='blood_request_delete'),
]
