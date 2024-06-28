"""
URL configuration for trouble_tracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from trouble_app import views  # Assuming your views are in the trouble_app application


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's authentication URLs
    path('', include('trouble_app.urls')),
    path('', views.index, name='index'),
    path('issues/', views.issue_list, name='issue_list'),
    path('register/', views.register_view, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.my_view, name='profile'),  # Example profile view
    path('issues/<int:issue_id>/', views.issue_detail, name='issue_detail'),  # Example detail view with dynamic URL
    path('create_issue/', views.create_issue, name='create_issue'),  # Create issue view
    path('issues/<int:issue_id>/delete/', views.create_confirm_delete, name='create_confirm_delete'),

    
]   

