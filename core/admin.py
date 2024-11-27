from django.contrib import admin
from .models import User, Video, Comment, Rating

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_creator', 'is_staff']
    list_filter = ['is_creator', 'is_staff', 'is_active']
    search_fields = ['username', 'email']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'creator', 'uploaded_at']
    search_fields = ['title', 'creator__username']
    list_filter = ['uploaded_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'video', 'user', 'created_at']
    search_fields = ['video__title', 'user__username', 'text']
    list_filter = ['created_at']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'video', 'user', 'rating', 'created_at']
    search_fields = ['video__title', 'user__username']
    list_filter = ['rating', 'created_at']
