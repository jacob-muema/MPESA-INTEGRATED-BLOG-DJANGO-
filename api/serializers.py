from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag, Comment, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count', 'created_at']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()

class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count', 'created_at']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()

class PostListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'excerpt', 'category', 'tags',
            'featured_image', 'status', 'created_at', 'updated_at', 
            'published_at', 'views', 'comment_count'
        ]

    def get_comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'content', 'excerpt', 
            'category', 'tags', 'featured_image', 'status', 'created_at', 
            'updated_at', 'published_at', 'views', 'comments'
        ]

    def get_comments(self, obj):
        comments = obj.comments.filter(is_approved=True, parent=None)
        return CommentSerializer(comments, many=True).data

class PostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'category', 'tags', 
            'featured_image', 'status'
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(**validated_data)
        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        instance.tags.set(tags)
        return instance

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'author', 'content', 'created_at', 'updated_at', 
            'is_approved', 'replies'
        ]

    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        return []

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'parent']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user', 'bio', 'avatar', 'website', 'twitter', 
            'github', 'linkedin', 'created_at'
        ]
