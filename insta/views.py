from django.shortcuts import render,redirect
from . forms import ImageUploadForm,ImageProfileForm,CommentForm
from .models import *
from django.contrib.auth.decorators import login_required
from vote.managers import  VotableManager
from django.contrib.auth.models import User
votes = VotableManager()

@login_required(login_url='/accounts/login/')
def home(request):
    images = Image.objects.all()
    
    
   
    
    return render(request, 'insta/index.html',{"images":images})

def image_upload(request):
    current_user = request.user
    if request.method == 'POST':
        form = ImageUploadForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('home')

    else:
        form = ImageUploadForm()
        return render(request,'insta/upload.html', {"form":form})
    
def profile_info(request):
    
    current_user=request.user
    profile_info = Profile.objects.filter(user=current_user).first()
    posts =  request.user.image_set.all()
    
    
    
    return render(request,'insta/profile.html',{"images":posts,"profile":profile_info,"current_user":current_user})
        
def profile_edit(request):
    current_user = request.user
    if request.method == 'POST':
        form = ImageProfileForm(request.POST,request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()
        return redirect('profile')

    else:
        form = ImageProfileForm()
        return render(request,'insta/edit.html',{"form":form})
    
def add_comment(request,id):

    current_user = request.user
    image = Image.get_single_photo(id=id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        print(form)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = current_user
            comment.image_id = id
            comment.save()
        return redirect('home')

    else:
        form = CommentForm()
        return render(request,'insta/new_comment.html',{"form":form,"image":image})  
    
def comments(request,id):
    comments = Comments.get_comments(id)
    number = len(comments   )
    
    return render(request,'insta/comments.html',{"comments":comments,"number":number})        

@login_required (login_url='/accounts/register/')          
def like_images(request,id):
    image =  Image.get_single_photo(id)
    user = request.user
    user_id = user.id
    
    if user.is_authenticated:
        uplike = image.votes.up(user_id)
        image.likes = image.votes.count()
        image.save()
        
    return redirect('home')
    
def search_user(request):
    
    if 'search_user' in request.GET and request.GET["search_user"]:

        search_term = request.GET.get("search_user")
        searched_user = User.objects.filter(username__icontains=search_term)
        message = f"{search_term}"  
        return render(request, 'insta/search_results.html', {"message": message, "users": searched_user})

    else:
        message = "You haven't searched for any term "
        return render(request, 'insta/search_results.html', {"message": message})
    
   
    
def unfollow(request, to_unfollow):
    if request.method == 'GET':
        user_profile2 = Profile.objects.get(pk=to_unfollow)
        unfollow_d = Follow.objects.filter(follower=request.user.profile, followed=user_profile2)
        unfollow_d.delete()
        return redirect('user_profile', user_profile2.user.username)


def follow(request, to_follow):
    if request.method == 'GET':
        user_profile3 = Profile.objects.get(pk=to_follow)
        follow_s = Follow(follower=request.user.profile, followed=user_profile3)
        follow_s.save()
        return redirect('user_profile', user_profile3.user.username)


def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    user_posts = user_prof.profile.posts.all()
    
    followers = Follow.objects.filter(followed=user_prof.profile)
    follow_status = None
    for follower in followers:
        if request.user.profile == follower.follower:
            follow_status = True
        else:
            follow_status = False
    params = {
        'user_prof': user_prof,
        'user_posts': user_posts,
        'followers': followers,
        'follow_status': follow_status
    }
    print(followers)
    return render(request, 'insta/user_profile.html', params)
    
