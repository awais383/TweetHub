from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm, userRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.exceptions import PermissionDenied



# Create your views here.
def index(request):
  return render(request, 'tweet/index.html')


def tweet_list(request):
   tweets= Tweet.objects.all().order_by('-created_at')
   return render (request, 'tweet/tweet_list.html', {'tweets': tweets})


@login_required
def tweet_create(request):
   if request.method== "POST":
      form= TweetForm(request.POST, request.FILES)
      if form.is_valid():
          tweet= form.save(commit=False)
          tweet.user= request.user
          tweet.save()
          return redirect('tweet_list') 
   else:
         form= TweetForm()
   return render(request, 'tweet/tweet_form.html', {'form': form})
   

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id, user=request.user)

    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        form = TweetForm(instance=tweet)

    return render(request, 'tweet/tweet_form.html', {'form': form})


@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    if tweet.user != request.user:
        raise PermissionDenied("You are not allowed to delete this tweet.")

    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')

    return render(request, 'tweet/tweet_delete.html', {'tweet': tweet})


def register_user(request):
    if request.method == 'POST':
        form = userRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=True)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            auth_login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('tweet_list')
    else:
        form = userRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


from .forms import LoginForm  # import your custom form


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('tweet_list')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



def loged_out_user(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('tweet_list') 
