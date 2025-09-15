from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.user_list, name='list'),
    path('create/', views.user_create, name='create'),
    path('<int:pk>/edit/', views.user_update, name='edit'),
    path('<int:pk>/delete/', views.user_delete, name='delete'),
]


