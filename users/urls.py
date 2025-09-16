from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.user_list, name='user_list'),
    path('create/', views.user_create, name='user_create'),
    path('update/<int:pk>/', views.user_update, name='user_update'),
    path('delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('toggle-active/<int:pk>/', views.user_toggle_active, name='user_toggle_active'),
    path('profile/', views.profile, name='profile'),
]