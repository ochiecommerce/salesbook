from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact_list, name='contact_list'),
    path('add_contact/',views.add_contact, name='add_contact'),
    path('register/',views.register, name='register'),
    path('<int:contact_id>/', views.contact_detail, name='contact_detail'),
    path('<int:contact_id>/add_interaction/', views.add_interaction, name='add_interaction'),
]
