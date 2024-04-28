from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('charts/', views.chart, name='files'),
    path('charts/<slug:pk>/', views.ChartUpdate.as_view(), name='chart_by')
]
