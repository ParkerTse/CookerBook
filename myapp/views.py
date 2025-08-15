from django.contrib.auth.models import User
def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'register.html')
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
from django.shortcuts import render
from .models import Recipe

def home(request):
    return render(request, 'home.html')

# Create your views here.
def recipes(request):
    query = request.GET.get('q', '')
    if query:
        all_recipes = Recipe.objects.filter(title__icontains=query)
    else:
        all_recipes = Recipe.objects.all()
    return render(request, 'recipes.html', {'recipes': all_recipes})

from .forms import RecipeForm

def post(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'post.html', {'form': RecipeForm(), 'success': True})
    else:
        form = RecipeForm()
    return render(request, 'post.html', {'form': form})

def profile(request):
    return render(request, 'profile.html')
	

