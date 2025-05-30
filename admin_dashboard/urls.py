from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Posts management
    path('posts/', views.posts_list, name='posts'),
    path('posts/create/', views.create_post, name='create_post'),
    path('posts/<slug:slug>/edit/', views.edit_post, name='edit_post'),
    path('posts/<slug:slug>/delete/', views.delete_post, name='delete_post'),
    
    # Comments management
    path('comments/', views.comments_list, name='comments'),
    path('comments/<int:comment_id>/approve/', views.approve_comment, name='approve_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    
    # User management
    path('users/', views.users_list, name='users'),
    
    # Content organization
    path('categories/', views.categories_list, name='categories'),
    path('tags/', views.tags_list, name='tags'),
    
    # Business features
    path('subscriptions/', views.subscriptions_list, name='subscriptions'),
    path('analytics/', views.analytics, name='analytics'),
    
    # System
    path('settings/', views.settings, name='settings'),
]
