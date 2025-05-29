from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Posts
    path('posts/', views.PostListCreateAPIView.as_view(), name='post_list_create'),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/comments/', views.PostCommentsAPIView.as_view(), name='post_comments'),
    
    # Categories and Tags
    path('categories/', views.CategoryListAPIView.as_view(), name='category_list'),
    path('tags/', views.TagListAPIView.as_view(), name='tag_list'),
    
    # User
    path('user/posts/', views.UserPostsAPIView.as_view(), name='user_posts'),
    path('user/profile/', views.UserProfileAPIView.as_view(), name='user_profile'),
    
    # Statistics
    path('stats/', views.api_stats, name='api_stats'),
    path('popular-posts/', views.popular_posts, name='popular_posts'),
    path('recent-posts/', views.recent_posts, name='recent_posts'),
]
