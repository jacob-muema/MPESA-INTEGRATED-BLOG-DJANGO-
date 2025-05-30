from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
import json
from blog.models import Post, Category, Tag, Comment, UserProfile
from django.contrib.auth.models import User
from blog.forms import PostForm

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(is_admin)
def dashboard(request):
    # Calculate date ranges
    now = timezone.now()
    this_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Basic stats
    stats = {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(status='published').count(),
        'draft_posts': Post.objects.filter(status='draft').count(),
        'total_users': User.objects.count(),
        'total_comments': Comment.objects.count(),
        'total_views': sum(post.views for post in Post.objects.all()),
        'posts_this_month': Post.objects.filter(created_at__gte=this_month_start).count(),
        'users_this_month': User.objects.filter(date_joined__gte=this_month_start).count(),
        'comments_this_month': Comment.objects.filter(created_at__gte=this_month_start).count(),
        'views_this_month': sum(post.views for post in Post.objects.filter(created_at__gte=this_month_start)),
    }
    
    # Recent posts
    recent_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:5]
    
    # Recent comments
    recent_comments = Comment.objects.select_related('author', 'post').order_by('-created_at')[:5]
    
    # Chart data for posts over time (last 7 days)
    posts_chart_data = []
    posts_chart_labels = []
    for i in range(6, -1, -1):
        date = now - timedelta(days=i)
        posts_count = Post.objects.filter(
            created_at__date=date.date()
        ).count()
        posts_chart_data.append(posts_count)
        posts_chart_labels.append(date.strftime('%b %d'))
    
    # Category distribution
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).filter(post_count__gt=0)
    
    category_chart_labels = [cat.name for cat in categories]
    category_chart_data = [cat.post_count for cat in categories]
    
    # Pending comments count
    pending_comments_count = Comment.objects.filter(is_approved=False).count()
    
    context = {
        'stats': stats,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
        'posts_chart_labels': json.dumps(posts_chart_labels),
        'posts_chart_data': json.dumps(posts_chart_data),
        'category_chart_labels': json.dumps(category_chart_labels),
        'category_chart_data': json.dumps(category_chart_data),
        'pending_comments_count': pending_comments_count,
    }
    
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def posts_list(request):
    posts = Post.objects.select_related('author', 'category').order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter:
        posts = posts.filter(status=status_filter)
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        posts = posts.filter(category__slug=category_filter)
    
    # Pagination
    paginator = Paginator(posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories for filter dropdown
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'categories': categories,
    }
    
    return render(request, 'admin/posts_list.html', context)

@login_required
@user_passes_test(is_admin)
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Post created successfully!')
            return redirect('admin_dashboard:posts')
    else:
        form = PostForm()
    
    context = {
        'form': form,
        'action': 'Create',
    }
    
    return render(request, 'admin/post_form.html', context)

@login_required
@user_passes_test(is_admin)
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('admin_dashboard:posts')
    else:
        form = PostForm(instance=post)
    
    context = {
        'form': form,
        'post': post,
        'action': 'Edit',
    }
    
    return render(request, 'admin/post_form.html', context)

@login_required
@user_passes_test(is_admin)
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('admin_dashboard:posts')
    
    context = {
        'post': post,
    }
    
    return render(request, 'admin/confirm_delete.html', context)

@login_required
@user_passes_test(is_admin)
def comments_list(request):
    comments = Comment.objects.select_related('author', 'post').order_by('-created_at')
    
    # Filter by approval status
    status_filter = request.GET.get('status')
    if status_filter == 'pending':
        comments = comments.filter(is_approved=False)
    elif status_filter == 'approved':
        comments = comments.filter(is_approved=True)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        comments = comments.filter(
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(post__title__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(comments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'admin/comments_list.html', context)

@login_required
@user_passes_test(is_admin)
def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    messages.success(request, 'Comment approved successfully!')
    return redirect('admin_dashboard:comments')

@login_required
@user_passes_test(is_admin)
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, 'Comment deleted successfully!')
    return redirect('admin_dashboard:comments')

@login_required
@user_passes_test(is_admin)
def users_list(request):
    users = User.objects.select_related('profile').order_by('-date_joined')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Filter by user type
    user_type = request.GET.get('type')
    if user_type == 'admin':
        users = users.filter(is_staff=True)
    elif user_type == 'regular':
        users = users.filter(is_staff=False)
    
    # Pagination
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'user_type': user_type,
    }
    
    return render(request, 'admin/users_list.html', context)

@login_required
@user_passes_test(is_admin)
def categories_list(request):
    categories = Category.objects.annotate(
        post_count=Count('posts')
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    
    return render(request, 'admin/categories_list.html', context)

@login_required
@user_passes_test(is_admin)
def tags_list(request):
    tags = Tag.objects.annotate(
        post_count=Count('posts')
    ).order_by('name')
    
    context = {
        'tags': tags,
    }
    
    return render(request, 'admin/tags_list.html', context)

@login_required
@user_passes_test(is_admin)
def subscriptions_list(request):
    # This would be implemented when you have a subscription model
    # For now, we'll show a placeholder
    context = {
        'subscriptions': [],
    }
    
    return render(request, 'admin/subscriptions_list.html', context)

@login_required
@user_passes_test(is_admin)
def analytics(request):
    # Advanced analytics view
    context = {
        'analytics_data': {},
    }
    
    return render(request, 'admin/analytics.html', context)

@login_required
@user_passes_test(is_admin)
def settings(request):
    # Site settings view
    context = {
        'settings': {},
    }
    
    return render(request, 'admin/settings.html', context)
