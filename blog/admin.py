from django.contrib import admin
from .models import Post, Comment, UserProfile, Like, Category, Tag

admin.AdminSite.site_header = 'Администрация'
admin.AdminSite.site_title = 'Добро пожаловать'
admin.AdminSite.index_title = 'Добро пожаловать'
admin.AdminSite.empty_value_display = '-пусто-'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'published_date', 'author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'content', 'created_date']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_picture', 'description', 'contact_info']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'post']

