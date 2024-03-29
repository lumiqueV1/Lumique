from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Photos, Vote
from .models import UserProfile
from .forms import LoginForm, RegistrationForm, PhotoSubmissionForm # Import the forms defined in forms.py
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import Photos
from .forms import PhotoSubmissionForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import logging
from ipware import get_client_ip


def home(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Filter photos for authenticated users
        photos = Photos.objects.filter(user__user=request.user)
    else:
        # For non-authenticated users, display all photos
        photos = Photos.objects.all()

    return render(request, 'Beautyswipe_v1/home.html', {'photos': photos})

def login_view(request):
    if request.method == 'POST':
        # If the request method is POST, process the login form
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # If the user is authenticated, log in and redirect to the home page
                login(request, user)
                return redirect('Beautyswipe_v1:home')
    else:
        # If the request method is GET, display the login form
        form = LoginForm()

    # Render the login page with the login form
    return render(request, 'Beautyswipe_v1/login.html', {'form': form})

def logout_view(request):
    # Log out the user and redirect to the home page
    logout(request)
    return redirect('Beautyswipe_v1:ranked_photos')

def register_view(request):
    if request.method == 'POST':
        # If the request method is POST, process the registration form
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # If the registration is successful, log in the user and redirect to the home page
            login(request, user)
            return redirect('Beautyswipe_v1:home')
    else:
        # If the request method is GET, display the registration form
        form = RegistrationForm()

    # Render the registration page with the registration form
    return render(request, 'Beautyswipe_v1/register.html', {'form': form })


def user_profile(request, user_id):
    user_profile = get_object_or_404(UserProfile, user__id=user_id)
    return render(request, 'Beautyswipe_v1/user_profile.html', {'user_profile': user_profile})


def submit_photo(request):
    if request.method == 'POST':
        form = PhotoSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            return redirect('Beautyswipe_v1:ranked_photos')
    else:
        form = PhotoSubmissionForm()

    return render(request, 'Beautyswipe_v1/submit_photo.html', {'form': form})



logger = logging.getLogger(__name__)

def vote(request, photo_id):
    try:
        photo = get_object_or_404(Photos, pk=photo_id)

        # Use get_client_ip to retrieve client's IP address
        client_ip, _ = get_client_ip(request)

        # Check if the user has already voted for this photo
        if not Vote.objects.filter(photo=photo, voter_ip=client_ip).exists():
            # Create a new Vote instance associated with the user's IP address
            Vote.objects.create(photo=photo, voter_ip=client_ip)

            # Increment the count by 1 for each vote
            photo.increment_count()

            # Return the updated count as a JSON response
            return JsonResponse({'count': photo.get_votes_count()})

        # If the user has already voted, return an error
        return JsonResponse({'error': 'Voting failed - User has already voted'}, status=400)

    except Exception as e:
        # Log any exceptions for further analysis
        logger.exception(f"Error processing upvote request: {str(e)}")
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    finally:
        # Log request details
        logger.info(f"Received upvote request for photo_id {photo_id}. Client IP: {client_ip}")


def about(request):
    # Get the top 20 users with the highest votes
    top_users = UserProfile.objects.annotate(total_votes=Count('photos__vote')).order_by('-total_votes')[:20]

    return render(request, 'Beautyswipe_v1/about.html', {'top_users': top_users})

def ranked_photos(request):
    # Retrieve all photos from the database
    photos = Photos.objects.all()

    # Calculate beauty rank for each photo based on the number of votes
    for photo in photos:
        photo.votes_count = photo.vote_set.count()

    # Order photos by beauty rank in descending order
    ranked_photos = sorted(photos, key=lambda x: x.votes_count, reverse=True)

    # Render the ranked photos page
    return render(request, 'Beautyswipe_v1/photos.html', {'ranked_photos': ranked_photos})


def ranking(request):
    # Annotate the UserProfiles with the count of related Photos votes
    top_users = UserProfile.objects.annotate(total_votes=Count('photos__vote')).order_by('-total_votes')[:20]

    return render(request, 'Beautyswipe_v1/ranking.html', {'top_users': top_users})


def landing_page(request):
    return render(request, 'Beautyswipe_v1/main.html')
