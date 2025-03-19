from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_size/<int:size_id>/', views.add_size, name='add_size'),
    path('remove_size/<int:size_id>/', views.remove_size, name='remove_size'),
]