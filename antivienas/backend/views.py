from django.shortcuts import render, redirect, HttpResponse
from .forms import MyUserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from antivienas.database.models import CityOfService, User, Genders

#GLOBAL VARS
CITY_CHOICES = CityOfService.choices
GENDERS = Genders.choices


# Create your views here.

def index_page(request):
    """returns the homepage"""
    template = "pages/index.html"
    context = {'cities': CITY_CHOICES, 'genders': GENDERS}

    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    city = request.GET.get('city') if request.GET.get('city') != None else ''
    gender = request.GET.get('gender') if request.GET.get('gender') != None else ''

    users = User.objects.filter(
        Q(first_name__icontains=search_query) |
        Q(city__icontains=city) |
        Q(gender__icontains=gender)
    )
    return render(request, template, context)

def register_page(request):
    """registration of user"""

    if request.user.is_authenticated:
        return redirect('index')
    
    template = "pages/register.html"
    form = MyUserCreationForm()

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['password1'] = post_data['password']
        post_data['password2'] = post_data['password']

        form = MyUserCreationForm(post_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('index')
        else:
            print("REGISTER ERROR")
            print(form.errors.as_text)

    return render(request, template, {'form': form, 'cities': CITY_CHOICES})

def login_page(request):
    """login part"""
    template = "pages/login.html"

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, template)

def logout_action(request):
    """logout part"""
    logout(request)
    return redirect('index')

def profile_page(request, user_id):
    """viewing of a user/friend profile"""
    template = "pages/profile.html"
    context = {"user_id": user_id}
    return render(request, template, context)

def meeting_page(request):
    """for managing user/friend meetings"""
    template = "pages/meeting-manager.html"
    return render(request, template)