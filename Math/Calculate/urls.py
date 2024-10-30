from django.urls import path
from . import views

urlpatterns = [
    path('calculate_bmi/', views.calculate_bmi, name='calculate_bmi'),
    path('result/<str:bmi>/<str:category>/', views.bmi_result, name='bmi_result'),
]