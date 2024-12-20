from django.urls import path
from . import views

urlpatterns = [
    path('calculator/', views.calculate, name='calculator'),
    path('currency_converter/', views.currency_convert, name='currency_converter'),
    path('calculate_bmi/', views.calculate_bmi, name='calculate_bmi'),
    path('result/<str:bmi>/<str:category>/', views.bmi_result, name='bmi_result'),
]