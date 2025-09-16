from django.urls import path
from . import views

urlpatterns = [
    path('', views.activity_list, name='activity_list'),
    path('create/', views.activity_create, name='activity_create'),
    path('update/<int:pk>/', views.activity_update, name='activity_update'),
    path('delete/<int:pk>/', views.activity_delete, name='activity_delete'),
]

