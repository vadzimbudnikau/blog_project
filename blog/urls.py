from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.HomeView.as_view(), name='search'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/like_toggle/', views.LikeToggleView.as_view(), name='like_toggle'),
    path('accounts/register/', views.CustomRegisterView.as_view(), name='register'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
    path('accounts/profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_id>/comment/create/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]

