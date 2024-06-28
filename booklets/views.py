
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .forms import BookletForm, CustomUserCreationForm
from .models import Booklet
from django.contrib.auth.models import User


def redirect_to_home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_home')
        else:
            return redirect('user_home')
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('user_home')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_home')
        else:
            return redirect('user_home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_staff:
                return redirect('admin_home')
            else:
                return redirect('user_home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def admin_home(request):
    booklets = Booklet.objects.filter(uploaded_by=request.user)
    return render(request, 'admin_home.html', {'booklets': booklets})

@login_required
def user_home(request):
    booklets = Booklet.objects.all()
    return render(request, 'user_home.html', {'booklets': booklets})


@user_passes_test(lambda u: u.is_superuser)
def add_booklet(request):
    if request.method == 'POST':
        form = BookletForm(request.POST, request.FILES)
        if form.is_valid():
            booklet = form.save(commit=False)
            booklet.uploaded_by = request.user
            booklet.save()
            return redirect('admin_home')
    else:
        form = BookletForm()
    return render(request, 'add_booklet.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_booklet(request, booklet_id):
    booklet = Booklet.objects.get(id=booklet_id)
    booklet.delete()
    return redirect('admin_home')

def logout_view(request):
    logout(request)
    return redirect('login')
