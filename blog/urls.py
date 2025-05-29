from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path('tag/<slug:slug>/', views.tag_posts, name='tag_posts'),
    path('my-posts/', views.user_posts, name='user_posts'),
    path('profile/', views.profile, name='profile'),
    path('subscribe/', views.subscription_plans, name='subscription_plans'),
    path('subscribe/process/', views.process_subscription, name='process_subscription'),
    path('api/mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('api/mpesa/status/', views.check_payment_status, name='check_payment_status'),
]
