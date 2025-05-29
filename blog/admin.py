from django.contrib import admin
from .models import Category, Tag, Post, Comment, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_featured', 'is_breaking', 'created_at', 'views']
    list_filter = ['status', 'category', 'is_featured', 'is_breaking', 'created_at', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    list_editable = ['status', 'is_featured', 'is_breaking']
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('Content', {
            'fields': ('content', 'excerpt', 'featured_image_url')
        }),
        ('Settings', {
            'fields': ('status', 'is_featured', 'is_breaking', 'read_time')
        }),
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author__username', 'content']
    list_editable = ['is_approved']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'website', 'created_at']
    search_fields = ['user__username', 'bio']
