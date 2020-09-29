from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Following

from datetime import datetime

PER_PAGE = 10

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def add_post(user, content, timestamp):
    new_post = Post (
        user = user,
        content = content,
        timestamp = timestamp,
    )
    new_post.save()


def add_pagination(request, posts, amount):
    """Return amount of posts per page."""
    paginator = Paginator(posts, 10)
    current_page = request.GET.get('page')
    return paginator.get_page(current_page)


def index(request):
    """Render index template."""
    # Success alert about adding post
    posted = ''
    if request.session.has_key('posted'):
        posted = request.session.get('posted')
        del request.session['posted']

    posts =  Post.objects.all().order_by('-timestamp')
    for post in posts:
        post.is_liked = False
        for likes in post.liked_posts.all():
            if likes.user == request.user:
                post.is_liked = True
                break

    page_posts = add_pagination(request, posts, PER_PAGE)
    show_pagination = posts.count() // PER_PAGE > 0

    # Select user's page_posts
    user_posts = ''
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(user=request.user)
    return render(request, "network/index.html", {
        "page_posts": page_posts,
        "posted": posted,
        "user_posts": user_posts,
        "posts": posts,
        "current_user": request.user,
        "show_pagination": show_pagination
    })


def new_post(request):
    """Add new post."""
    empty_post = ''
    if request.method == "POST":
        if request.POST.get("post-button"):
            if request.POST.get("post-content"):
                content = request.POST.get("post-content")
                timestamp = datetime.now()
                add_post(request.user, content, timestamp)
                request.session['posted'] = "Your post was successfully added."
                return HttpResponseRedirect(reverse("index"))
            else:
                empty_post = "You are trying to submit an empty post. Please enter the content of your post."
    return render(request, "network/new_post.html", {
        "user": request.user,
        "empty_post": empty_post
    })


@csrf_exempt
# @login_required
def like_post(request, post_id):
    """Like/dislike post #post_id."""
    post = Post.objects.get(pk=post_id)
    data = json.loads(request.body.decode("utf-8"))
    command = data["command"]
    if command == "like":
        Like.objects.create(user=request.user, liked_post=post)
        button_text = "Unlike"
    elif command == "unlike":
        like_obj = Like.objects.get(user=request.user, liked_post=post)
        like_obj.delete()
        button_text = "Like"
    post.save()
    # Count Likes
    likes_count = Like.objects.filter(liked_post=post_id).count()
    return JsonResponse({'likes': likes_count, 'button_text': button_text})


@csrf_exempt
def edit_post(request, post_id):
    """Edit post #post_id."""
    post = Post.objects.get(pk=post_id)
    data = json.loads(request.body.decode("utf-8"))
    post.content = data["edited_post"]
    post.save()
    return JsonResponse({"post_content": post.content})


@csrf_exempt
def follow_user(request, username):
    """Follow user with username username."""
    data = json.loads(request.body.decode("utf-8"))
    following = User.objects.get(username=username)
    Following.objects.create(user=request.user, following=following)
    followers = Following.objects.filter(following=following).count()
    return JsonResponse({"button_text": "Unfollow", "followers": followers})


@csrf_exempt
def unfollow_user(request, username):
    """Unfollow user with username username."""
    data = json.loads(request.body.decode("utf-8"))
    following = User.objects.get(username=username)
    following_obj = Following.objects.get(user=request.user, following=following)
    following_obj.delete()
    followers = Following.objects.filter(following=following).count()
    return JsonResponse({"button_text": "Follow", "followers": followers})


def following(request):
    """Render following template."""
    following_users = Following.objects.filter(user=request.user).values('following')
    posts = Post.objects.filter(user__in=following_users).order_by('-timestamp')
    following_exists = following_users.count() > 0
    posts_exist = posts.count() > 0

    for post in posts:
        post.is_liked = False
        for likes in post.liked_posts.all():
            if likes.user == request.user:
                post.is_liked = True
                break

    page_posts = add_pagination(request, posts, PER_PAGE)
    show_pagination = posts.count() // PER_PAGE > 0

    return render(request, "network/following.html", {
        "posts": posts,
        "page_posts": page_posts,
        "show_pagination": show_pagination,
        "following_exists": following_exists,
        "posts_exist": posts_exist
    })


def profile(request, username):
    """Render profile of user with username username."""
    follower = request.user
    user = User.objects.get(username=username)
    show_follow_button = (follower != user)
    to_follow = not Following.objects.filter(user=follower, following=user).exists()
    user_posts = Post.objects.filter(user=user.id).order_by('-timestamp')

    for post in user_posts:
        post.is_liked = False
        for likes in post.liked_posts.all():
            if likes.user == request.user:
                post.is_liked = True
                break

    following = Following.objects.filter(user=user.id).count()
    followers = Following.objects.filter(following=user.id).count()

    page_posts = add_pagination(request, user_posts, PER_PAGE)
    show_pagination = user_posts.count() // PER_PAGE > 0

    return render(request, "network/profile.html", {
        "username": user.username,
        "date_joined": user.date_joined,
        "last_login": user.last_login,
        "user_posts": user_posts,
        "page_posts": page_posts,
        "following": following,
        "followers": followers,
        "to_follow": to_follow,
        "show_follow_button": show_follow_button,
        "current_user": request.user
    })
