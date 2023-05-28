from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import *
import json 
from django.http import JsonResponse


def index(request):
    all_posts = NewPost.objects.all().order_by("-id")
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"all_posts": all_posts, "page_obj":page_obj}
    return render(request, "network/index.html", context)


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

        # Added by me
        # profession = request.POST.get("profession")
        # description = request.POST.get("description")

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

def create_post(request):
    if request.method == "GET":
        return render(request, "network/create_post.html")
    if request.method == "POST":
        content = request.POST.get("content")
        creator = User.objects.get(pk = request.user.id)
        new_post = NewPost(content = content, creator = creator)
        new_post.save()
        # return HttpResponse(f"{request.user.id}")
        return HttpResponseRedirect(reverse("index"))

def profile_page(request, name):
    if request.method == "GET":
        # Followers 
        user = User.objects.get(username = name)
        follow_objects_all = Follow.objects.filter(user_being_followed = user)
        follow_count = follow_objects_all.count() 

        # Following 
        following_objects_all = Follow.objects.filter(user_following = user)
        following_count = following_objects_all.count()

        # For active user 
        user_active = request.user 
        user_active_name = request.user.username
        user_active_posts = NewPost.objects.filter(creator= user_active).order_by('-id')
        
        # Check if user is a follower 
        follower = check_follower(name, user_active_name, user)
       
        # User posts object when link is clicked
        user_posts = NewPost.objects.filter(creator = user).order_by('-id')
        


        context = {"user_posts":user_posts, "name":name, "user_active":user_active, "user_clicked":user, "user_active_posts": user_active_posts, "follow_count":follow_count, "follow_objects_all":follow_objects_all, "follower":follower, "following_count":following_count}
        return render(request, "network/profile_page.html", context)
        return HttpResponse(f"{request.user.username}")

def check_follower(name, user_active_name, user):
    follow_objects_all = Follow.objects.filter(user_being_followed = user)
    active_user_object = User.objects.get(username = user_active_name)
    if active_user_object.username != name:
            
            for f in follow_objects_all:
                
                if f.user_following.username == active_user_object.username:
                    return True
                else:
                    return False
        

def test(request):
    # followers = User.objects.get(pk = 1).followers
    # user_id = request.user.id
    return render(request, "network/test.html")
    return HttpResponse(f"{followers}")

def follow(request, name):
    # User who pressed follow 
    user_active = request.user
    user_active_name= user_active.username

    # User being followed 
    user_being_followed = User.objects.get(username = name)

    follow_object = Follow(user_being_followed = user_being_followed, user_following = user_active)
    follow_object.save()
    user_being_followed.followers += 1
    return HttpResponseRedirect(reverse("profile_page", args = (name,)))


def unfollow(request, user_clicked, user_active):
    # follow_object = Follow.objects.get()
    user_clicked_object = User.objects.get(username = user_clicked)
    user_clicked_object_name = user_clicked_object.username
    user_active_object = User.objects.get(username = user_active)
    follow_object = Follow.objects.filter(user_being_followed = user_clicked_object, user_following = user_active_object)
    follow_object.delete()
    return HttpResponseRedirect(reverse("profile_page", args = (user_clicked_object_name,)))

def followers(request, user_clicked):
    user_clicked_object = User.objects.get(username = user_clicked)
    followers_objects = Follow.objects.filter(user_being_followed = user_clicked_object) 
    context = {"followers_objects":followers_objects}
    return render(request, "network/followers.html", context)

def following(request, user_clicked):
    user_clicked_object = User.objects.get(username = user_clicked)
    following_objects = Follow.objects.filter(user_following = user_clicked_object)
    context = {"following_objects":following_objects}
    return render(request, "network/following.html", context)

def following_page(request):
    user_active = request.user.username
    user_active_object = User.objects.get(username = user_active)
    follow_objects = Follow.objects.filter(user_following = user_active_object)
    
    posts = [] 
    for f in follow_objects:
        posts_all = NewPost.objects.filter(creator = f.user_being_followed).order_by("-id")
        posts.append(posts_all)
    context = {"posts":posts}
    return render(request, "network/following_posts.html", context)
    return HttpResponse(f"{user_active}")


def edit_post(request, post_id):
    data = json.loads(request.body)
    number = post_id
    post = NewPost.objects.get(pk  = post_id)
    post.content = data["content1"]
    post.save()
    content = post.content
    
    return JsonResponse({"message":"successfully received", "number": number, "content":content})

    
    