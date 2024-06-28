from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = 'trouble_app'  # Define app_name for namespace resolution

urlpatterns = [
    path('', views.index, name='index'),  # Homepage or index view
    path('register/', views.register_view, name='register'),  # User registration view
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Login view
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # Logout view
    path('accounts/', include('django.contrib.auth.urls')),  # Includes Django's built-in authentication URLs
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard view
    path('issue/', views.issue_list, name='issue_list'),  # List of issues view
    path('create_issue/', views.create_issue, name='create_issue'),  # Create issue view
    path('issue/<int:issue_id>/', views.issue_detail, name='issue_detail'),  # Issue detail view
    path('issue/<int:issue_id>/edit/', views.issue_edit, name='issue_edit'),  # Edit issue view
    path('issues/<int:issue_id>/delete/', views.create_confirm_delete, name='create_confirm_delete'),
]
