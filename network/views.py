from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post

from datetime import datetime


def add_post(user, content, timestamp):
    new_post = Post (
        user = user,
        content = content,
        timestamp = timestamp,
    )
    new_post.save()

def index(request):
    posted = ''
    if request.session.has_key('posted'):
        posted = request.session.get('posted')
        del request.session['posted']

    posts =  Post.objects.all()
    # Show 10 post per page
    paginator = Paginator(posts, 10)
    current_page = request.GET.get('page')
    page_posts = paginator.get_page(current_page)
    return render(request, "network/index.html", {
        "page_posts": page_posts,
        "posted": posted
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
