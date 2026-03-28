from django.urls import path
from . import views

app_name = 'grimoire'

urlpatterns = [
    path('plant_list/', views.plant_list, name='plant_list'),
    path('plant/<slug:slug>/', views.plant_detail, name='plant_detail'),
    path('property/<slug:slug>/', views.property_detail, name='property'),
    path('random/', views.random_plant, name='random_plant'),
]
