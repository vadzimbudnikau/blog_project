from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, ListView, DetailView
from .models import Post, Comment, UserProfile, Like, Category, Tag
from .forms import CommentForm, CommentUpdateForm, PostForm, PostUpdateForm, UserUpdateForm


class HomeView(ListView):
    """Display a list of all posts on the home page."""
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 3
    ordering = '-published_date'

    def get_queryset(self):
        search_query = self.request.GET.get('query')
        queryset = super().get_queryset()
        category_slug = self.request.GET.get('category')
        tag_slug = self.request.GET.get('tag')

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(content__icontains=search_query))

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        if tag_slug:
            queryset = queryset.filter(tag__slug=tag_slug)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        for post in context['posts']:
            post.total_likes = post.like_set.count()
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    """Display the details of a specific post."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """
        Add additional context data to the view.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Updated context data.
        """
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        liked = Like.objects.filter(user=self.request.user, post=post).exists()
        comments = post.comments.all().order_by('created_date')
        context['liked'] = liked
        context['total_likes'] = post.like_set.count()
        context['comments'] = comments
        return context


class LikeToggleView(LoginRequiredMixin, View):
    """Toggle the like status of a post."""

    def post(self, request, pk):
        """
        Handle POST request to toggle the like status of a post.

        Args:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key of the post.

        Returns:
            HttpResponseRedirect: Redirects to the post detail page.
        """
        post = get_object_or_404(Post, pk=pk)
        liked = False

        if Like.objects.filter(user=request.user, post=post).exists():
            Like.objects.filter(user=request.user, post=post).delete()
        else:
            Like.objects.create(user=request.user, post=post)
            liked = True
            total_likes = post.likes.count()

        return redirect('post_detail', pk=pk)


class CustomRegisterView(CreateView):
    """Handle user registration."""
    form_class = UserCreationForm
    template_name = 'blog/registration.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.save()
        login(self.request, user)
        return response


class CustomLoginView(LoginView):
    """Handle user login."""
    template_name = 'blog/login.html'


class CustomLogoutView(LogoutView):
    """Handle user logout."""
    template_name = 'blog/logout.html'
    next_page = '/accounts/login/'


class ProfileView(LoginRequiredMixin, TemplateView):
    """Display the user profile."""
    template_name = 'blog/profile.html'


class PostCreateView(CreateView):
    """Handle creation of a new post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_create.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(UpdateView):
    """Handle updating an existing post."""
    model = Post
    form_class = PostUpdateForm
    template_name = 'blog/post_update.html'
    success_url = reverse_lazy('home')


class PostDeleteView(DeleteView):
    """Handle deletion of an existing post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')


class CommentCreateView(CreateView):
    """Handle creation of a new comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_id']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.kwargs['post_id']])


class CommentUpdateView(UpdateView):
    """Handle updating an existing comment."""
    model = Comment
    form_class = CommentUpdateForm
    template_name = 'blog/comment_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.post_id])


class CommentDeleteView(DeleteView):
    """Handle deletion of an existing comment."""
    model = Comment
    template_name = 'blog/comment_delete.html'

    def get_success_url(self):
        return reverse('post_detail', args=[self.object.post_id])


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Handle updating the user profile."""
    model = UserProfile
    form_class = UserUpdateForm
    template_name = 'blog/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return user_profile

    def form_valid(self, form):
        """Handle uploaded profile picture."""
        profile_picture = form.cleaned_data['profile_picture']
        if profile_picture:
            self.request.user.userprofile.profile_picture = profile_picture
            self.request.user.userprofile.save()

        messages.success(self.request, 'Profile successfully updated.')
        return super().form_valid(form)
