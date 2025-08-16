from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from .models import Recipe, UserEmail
from .forms import RecipeForm, UsernameChangeForm
import base64
from django.core.files.base import ContentFile


def home(request):
    return render(request, 'home.html')


def recipes(request):
    query = request.GET.get('q', '')
    if query:
        all_recipes = Recipe.objects.filter(title__icontains=query)
    else:
        all_recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': all_recipes})


def post(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            if request.user.is_authenticated:
                recipe.author = request.user.username
                recipe.created_by = request.user
            recipe.save()
            return render(request, 'post.html', {'form': RecipeForm(), 'success': True})
    else:
        form = RecipeForm()
    return render(request, 'post.html', {'form': form})


def profile(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You need to login first to view your profile.')
        return render(request, 'profile.html', {'show_login_message': True})
    user = request.user
    username_form = None
    num_recipes = Recipe.objects.filter(created_by=user).count()
    if request.method == 'POST':
        username_form = UsernameChangeForm(request.POST, instance=user)
        if username_form.is_valid():
            username_form.save()
            messages.success(request, 'Username updated successfully!')
            return redirect('profile')
    else:
        username_form = UsernameChangeForm(instance=user)
    return render(request, 'profile.html', {'username_form': username_form, 'num_recipes': num_recipes})


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if email already exists
        if UserEmail.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')
        
        try:
            # Create user with email as username (Django requires unique usernames)
            # We'll use email as both username and email
            user = User.objects.create_user(
                username=email,  # Use email as username
                email=email,
                password=password
            )
            
            # Create UserEmail record
            UserEmail.objects.create(user=user, email=email)
            
            # Log the user in
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
            
        except IntegrityError:
            messages.error(request, 'An account with this email already exists')
            return render(request, 'register.html')
        except Exception as e:
            messages.error(request, 'An error occurred while creating your account')
            return render(request, 'register.html')
    
    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        try:
            # Find user by email
            user_email = UserEmail.objects.get(email=email)
            user = user_email.user
            
            # Authenticate using username (which is the email)
            authenticated_user = authenticate(request, username=user.username, password=password)
            
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
        except UserEmail.DoesNotExist:
            messages.error(request, 'No account found with this email')
        except Exception as e:
            messages.error(request, 'An error occurred during login')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')