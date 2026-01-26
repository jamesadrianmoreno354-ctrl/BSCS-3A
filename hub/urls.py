from django.urls import path
from . import views

app_name = 'hub'

urlpatterns = [
    path('', views.index, name='index'),
    path('portfolio/<int:pk>/', views.detail, name='detail'),
    path('data/portfolios.json', views.portfolios_json, name='portfolios_json'),
]
