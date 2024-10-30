from django.urls import path
from . import views

urlpatterns = [
    path('currency_converter/', views.currencyx, name='currency_converter'),
    path('calculate_bmi/', views.calculate_bmi, name='calculate_bmi'),
    path('result/<str:bmi>/<str:category>/', views.bmi_result, name='bmi_result'),
]