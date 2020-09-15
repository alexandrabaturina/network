from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like

from datetime import datetime


def add_post(user, content, timestamp):
    new_post = Post (
        user = user,
        content = content,
        timestamp = timestamp,
    )
    new_post.save()

def index(request):
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


    # Show 10 post per page
    paginator = Paginator(posts, 10)
    current_page = request.GET.get('page')
    page_posts = paginator.get_page(current_page)

    # Select user's page_posts
    user_posts = ''
    if request.user.is_authenticated:
        user_posts = Post.objects.filter(user=request.user)
    return render(request, "network/index.html", {
        "page_posts": page_posts,
        "posted": posted,
        "user_posts": user_posts,
        "posts": posts,
        "current_user": request.user
    })


def new_post(request):
    empty_post = ''
    if request.method == "POST":
        if request.POST.get("post-button"):
            if request.POST.get("post-content"):
                content = request.POST.get("post-content")
                timestamp = datetime.now()
                add_post(request.user, content, timestamp)
                request.session['posted'] = "Your post was successfully saved."
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
    post = Post.objects.get(pk=post_id)
    data = json.loads(request.body.decode("utf-8"))
    post.content = data["edited_post"]
    post.save()
    return JsonResponse({"post_content": post.content})



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

def following(request):
    return render(request, "network/following.html")

def profile(request, username):
    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(user=user.id).order_by('-timestamp')

    return render(request, "network/profile.html", {
        "username": username,
        "user_posts": user_posts
    })
