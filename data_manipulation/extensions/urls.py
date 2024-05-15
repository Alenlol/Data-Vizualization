from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('files/', views.FileChoose.as_view(), name='files'),
    path('files/<slug:pk>/', views.ChartUpdate.as_view(), name='files_by')
]
