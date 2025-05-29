from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from datetime import datetime
from .models import Post, Category, Tag, Comment, UserProfile
from .forms import CommentForm, UserProfileForm
from .mpesa import MpesaClient

logger = logging.getLogger(__name__)

def is_admin(user):
    return user.is_staff or user.is_superuser

def home(request):
    # Get breaking news
    breaking_news = Post.objects.filter(status='published', is_breaking=True).order_by('-created_at')[:3]
    
    # Get featured post
    featured_post = Post.objects.filter(status='published', is_featured=True).first()
    
    # Get latest posts
    posts = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    # Exclude featured post from regular posts
    if featured_post:
        posts = posts.exclude(id=featured_post.id)
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Sidebar data
    categories = Category.objects.annotate(post_count=Count('posts')).filter(post_count__gt=0)
    popular_posts = Post.objects.filter(status='published').order_by('-views')[:5]
    recent_posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    
    context = {
        'breaking_news': breaking_news,
        'featured_post': featured_post,
        'page_obj': page_obj,
        'categories': categories,
        'popular_posts': popular_posts,
        'recent_posts': recent_posts,
        'search_query': search_query,
    }
    return render(request, 'blog/home.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    post.increment_views()
    
    comments = post.comments.filter(is_approved=True, parent=None).select_related('author')
    comment_form = CommentForm()
    
    # Related posts
    related_posts = Post.objects.filter(
        category=post.category, 
        status='published'
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        content = data.get('content')
        parent_id = data.get('parent_id')
    else:
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id')
    
    if content:
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent_id=parent_id if parent_id else None
        )
        
        if request.content_type == 'application/json':
            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'author': comment.author.username,
                    'content': comment.content,
                    'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p'),
                }
            })
        else:
            messages.success(request, 'Comment added successfully!')
    
    return redirect('blog:post_detail', slug=slug)

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'blog/category_posts.html', context)

def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'tag': tag,
        'page_obj': page_obj,
    }
    return render(request, 'blog/tag_posts.html', context)

@login_required
def profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('blog:profile')
    else:
        form = UserProfileForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'blog/profile.html', context)

# Admin-only views
@user_passes_test(is_admin)
def admin_dashboard(request):
    stats = {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(status='published').count(),
        'draft_posts': Post.objects.filter(status='draft').count(),
        'total_comments': Comment.objects.count(),
        'total_categories': Category.objects.count(),
    }
    
    recent_posts = Post.objects.order_by('-created_at')[:5]
    recent_comments = Comment.objects.order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_posts': recent_posts,
        'recent_comments': recent_comments,
    }
    return render(request, 'blog/admin_dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def create_post(request):
    """Admin-only view to create posts"""
    if request.method == 'POST':
        # Handle form submission - redirect to admin for now
        messages.info(request, 'Please use the Django admin to create posts.')
        return redirect('/admin/blog/post/add/')
    else:
        # Redirect to admin
        return redirect('/admin/blog/post/add/')

@login_required
@user_passes_test(is_admin)
def edit_post(request, slug):
    """Admin-only view to edit posts"""
    post = get_object_or_404(Post, slug=slug)
    messages.info(request, 'Please use the Django admin to edit posts.')
    return redirect(f'/admin/blog/post/{post.id}/change/')

@login_required
@user_passes_test(is_admin)
def delete_post(request, slug):
    """Admin-only view to delete posts"""
    post = get_object_or_404(Post, slug=slug)
    messages.info(request, 'Please use the Django admin to delete posts.')
    return redirect(f'/admin/blog/post/{post.id}/delete/')

@login_required
def user_posts(request):
    """View user's own posts (read-only for non-admin users)"""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'blog/user_posts.html', context)

@login_required
def subscription_plans(request):
    """Display subscription plans"""
    context = {
        'plans': [
            {
                'name': 'Basic',
                'price': 150,
                'features': [
                    'Access to all articles',
                    'Weekly newsletter',
                    'Basic tech insights',
                    'Community access'
                ]
            },
            {
                'name': 'Premium',
                'price': 250,
                'features': [
                    'Everything in Basic',
                    'Exclusive premium content',
                    'Daily tech briefings',
                    'Priority support',
                    'Early access to articles',
                    'Ad-free experience'
                ]
            }
        ]
    }
    return render(request, 'blog/subscription_plans.html', context)

@login_required
@require_POST
def process_subscription(request):
    """Process M-Pesa subscription payment"""
    plan_type = request.POST.get('plan_type')
    phone_number = request.POST.get('phone_number')
    
    # Validate phone number
    if not phone_number:
        messages.error(request, 'Please provide a valid phone number')
        return redirect('blog:subscription_plans')
    
    # Clean phone number - ensure it starts with 254
    phone_number = phone_number.strip()
    if phone_number.startswith('0'):
        phone_number = '254' + phone_number[1:]
    elif not phone_number.startswith('254'):
        phone_number = '254' + phone_number
    
    # Set amount based on plan
    if plan_type == 'Premium':
        amount = 250
    else:  # Basic plan
        amount = 150
    
    # Generate a unique reference
    account_reference = f"TechPulse-{request.user.id}-{int(datetime.now().timestamp())}"
    transaction_desc = f"TechPulse {plan_type} Subscription"
    
    try:
        # Initialize M-Pesa client
        mpesa_client = MpesaClient()
        
        # Log the request
        logger.info(f"Initiating STK push for user {request.user.username}, plan: {plan_type}, phone: {phone_number}")
        
        # Make the STK push request
        response = mpesa_client.stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=account_reference,
            transaction_desc=transaction_desc
        )
        
        # Check if request was successful
        if 'ResponseCode' in response and response['ResponseCode'] == '0':
            # Store transaction details in session for status checking
            request.session['checkout_request_id'] = response['CheckoutRequestID']
            request.session['subscription_plan'] = plan_type
            
            messages.success(
                request, 
                f"Payment request sent to {phone_number}. Please check your phone and enter your M-Pesa PIN to complete the transaction."
            )
            
            # Log success
            logger.info(f"STK push initiated successfully for {request.user.username}: {response['CheckoutRequestID']}")
        else:
            # Handle error
            error_message = response.get('errorMessage', 'Unknown error')
            messages.error(request, f"Payment request failed: {error_message}")
            
            # Log error
            logger.error(f"STK push failed for {request.user.username}: {response}")
    
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        logger.exception(f"Exception in process_subscription: {str(e)}")
    
    return redirect('blog:subscription_plans')

@csrf_exempt
@require_POST
def mpesa_callback(request):
    """Handle M-Pesa callback"""
    try:
        # Parse the JSON data from the request
        data = json.loads(request.body)
        logger.info(f"M-Pesa callback received: {data}")
        
        # Extract the relevant information
        result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        checkout_request_id = data.get('Body', {}).get('stkCallback', {}).get('CheckoutRequestID')
        
        if result_code == 0:
            # Payment was successful
            # Extract payment details
            metadata = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])
            
            # Process payment details
            payment_details = {}
            for item in metadata:
                if item.get('Name') == 'Amount':
                    payment_details['amount'] = item.get('Value')
                elif item.get('Name') == 'MpesaReceiptNumber':
                    payment_details['receipt_number'] = item.get('Value')
                elif item.get('Name') == 'PhoneNumber':
                    payment_details['phone_number'] = item.get('Value')
            
            # TODO: Update user subscription status in the database
            logger.info(f"Successful payment: {payment_details}")
            
            # Return success response
            return JsonResponse({
                'status': 'success',
                'message': 'Payment processed successfully'
            })
        else:
            # Payment failed
            result_desc = data.get('Body', {}).get('stkCallback', {}).get('ResultDesc', 'Unknown error')
            logger.warning(f"Payment failed: {result_desc}")
            
            # Return error response
            return JsonResponse({
                'status': 'error',
                'message': result_desc
            })
    
    except Exception as e:
        logger.exception(f"Error processing M-Pesa callback: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required
def check_payment_status(request):
    """Check the status of an STK push payment"""
    checkout_request_id = request.session.get('checkout_request_id')
    
    if not checkout_request_id:
        return JsonResponse({
            'status': 'error',
            'message': 'No pending transaction found'
        })
    
    try:
        mpesa_client = MpesaClient()
        response = mpesa_client.check_transaction_status(checkout_request_id)
        
        return JsonResponse({
            'status': 'success',
            'data': response
        })
    
    except Exception as e:
        logger.exception(f"Error checking payment status: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)
