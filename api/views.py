from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Q

from blog.models import Post, Category, Tag, Comment, UserProfile
from .serializers import (
    PostListSerializer, PostDetailSerializer, PostCreateUpdateSerializer,
    CategorySerializer, TagSerializer, CommentSerializer, CommentCreateSerializer,
    UserProfileSerializer, UserSerializer
)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
        
        # Search
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(content__icontains=search) |
                Q(tags__name__icontains=search)
            ).distinct()
        
        # Category filter
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Tag filter
        tag = self.request.query_params.get('tag', None)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Author filter
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        
        return queryset.order_by('-created_at')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostListSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer

    def get_object(self):
        obj = super().get_object()
        if self.request.method == 'GET':
            obj.increment_views()
        return obj

    def perform_update(self, serializer):
        # Only allow author to update their own posts
        if self.get_object().author != self.request.user:
            raise permissions.PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        # Only allow author to delete their own posts
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You can only delete your own posts.")
        instance.delete()

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class PostCommentsAPIView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=post_slug)
        return post.comments.filter(is_approved=True, parent=None).select_related('author')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        post_slug = self.kwargs['slug']
        post = get_object_or_404(Post, slug=post_slug)
        serializer.save(author=self.request.user, post=post)

class UserPostsAPIView(generics.ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')

class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_stats(request):
    """Get basic blog statistics"""
    stats = {
        'total_posts': Post.objects.filter(status='published').count(),
        'total_categories': Category.objects.count(),
        'total_tags': Tag.objects.count(),
        'total_comments': Comment.objects.filter(is_approved=True).count(),
        'total_users': User.objects.count(),
    }
    return Response(stats)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_posts(request):
    """Get most popular posts by views"""
    posts = Post.objects.filter(status='published').order_by('-views')[:5]
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def recent_posts(request):
    """Get most recent posts"""
    posts = Post.objects.filter(status='published').order_by('-created_at')[:5]
    serializer = PostListSerializer(posts, many=True)
    return Response(serializer.data)
