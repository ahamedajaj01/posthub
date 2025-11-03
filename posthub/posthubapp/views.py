from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .forms import RegistrationForm, PostForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def homepage(request):
    print("User authenticated?", request.user.is_authenticated)  # debu
    if  request.user.is_authenticated:
        return redirect('view_post')
    else:
        posts = Post.objects.all().order_by('-created_at')
        return render(request, 'posthubapp/index.html', {'posts': posts})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Registration successful! You can now log in.")
            return redirect('login_view')
        else:
            messages.error(request,"Please correct the error below.")
            print("Form errors:", form.errors)
            return render(request, 'posthubapp/register.html', {'form':form})
    else:
        form = RegistrationForm()
        return render(request,'posthubapp/register.html',{'form':form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            #  try to find user
            try:
                user = User.objects.get(email=email)
            except Exception as e:
                messages.error(request,  f"{e} No account found with this email.")
                return render(request, 'posthubapp/login_view.html', {'form': form})
            user = authenticate(request, username = user.username, password = password)
            if user is not None:
                login(request,user)
                messages.success(request,f"Welcome back, {user.username}!")
                return redirect('view_post')
            else:
                messages.error(request,"Invalid credentials")
                return redirect('login_view')
    else:
        form = LoginForm()  
        return render(request,'posthubapp/login_view.html',{'form':form})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('view_post')
        else:
             messages.error(request, "Please correct the errors below.")
             return render(request, 'posthubapp/create_post.html',{'form':form})
    else:
        form = PostForm()
        return render(request,'posthubapp/create_post.html',{'form':form})
    
@login_required
def view_post(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'posthubapp/view_post.html',{'posts':posts})

def explore_post(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request,"posthubapp/explore_post.html",{"posts":posts})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('login_view')

@login_required
def edit_post(request,post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        messages.error(request, "You are not allowed to edit this post.")
        return redirect('view_post')
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully.")
            return redirect("view_post")
    else:
        form = PostForm(instance=post)
    return render(request,"posthubapp/edit_post.html",{"form":form})

@login_required
def delete_post(request,post_id):
    post = get_object_or_404(Post, id = post_id)

    if request.user != post.author:
        messages.error(request, "You are not allowed to delete this post.")
        return redirect('view_post')

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect('view_post')  # your user’s post list view

    return render(request, 'posthubapp/delete_post.html', {'post': post})
