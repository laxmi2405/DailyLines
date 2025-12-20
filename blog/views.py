from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Post, Category
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden

# HOME PAGE
def home(request):
    query = request.GET.get("q", "")

    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        ).order_by('-created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    categories = Category.objects.all()

    return render(request, "blog/home.html", {
        "posts": posts,
        "categories": categories
    })


# CATEGORY FILTER
def category_filter(request, category_id):
    posts = Post.objects.filter(category_id=category_id).order_by('-created_at')
    categories = Category.objects.all()
    return render(request, 'blog/home.html', {
        'posts': posts,
        'categories': categories
    })


# ADD POST
@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)   # hold before saving
            post.author = request.user       # assign logged user
            post.save()                      # now save
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})


# POST DETAILS + COMMENTS
def post_details(request, id):
    post = get_object_or_404(Post, id=id)
    comments = post.comments.all().order_by('-created_at')

    liked = False
    if request.user.is_authenticated:
        liked = post.likes.filter(user=request.user).exists()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect('post_details', id=post.id)
    else:
        form = CommentForm()

    return render(request, 'blog/post_details.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'liked': liked   # << send to template
    })


# SIGNUP USER
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'blog/signup.html', {'form': form})

@login_required
def edit_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Prevent editing others' posts
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_details', id=post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/edit_post.html', {'form': form})

@login_required
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)

    # Prevent deleting others' posts
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'blog/confirm_delete.html', {'post': post})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'blog/my_posts.html', {'posts': posts})

from .models import Like

@login_required
def toggle_like(request, id):
    post = get_object_or_404(Post, id=id)

    # check if already liked
    like = Like.objects.filter(user=request.user, post=post)

    if like.exists():
        like.delete()  # unlike
    else:
        Like.objects.create(user=request.user, post=post)  # like

    return redirect('post_details', id=id)

