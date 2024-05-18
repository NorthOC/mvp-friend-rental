from django.shortcuts import render, redirect, HttpResponse
from .forms import MyUserCreationForm, UserProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from antivienas.database.models import CityOfService, User, Genders, FriendSetting
import os

#GLOBAL VARS
CITY_CHOICES = dict((value, key) for key, value in CityOfService.choices)
GENDERS = dict((value, key) for key, value in Genders.choices)
COLORS = dict((value, key) for key, value in User.InterestColorHexes.choices)
PERSONALITY_TYPES = dict((value, key) for key, value in User.PersonalityTypes.choices)
EDU_CHOICES = dict((value, key) for key, value in User.EducationChoices.choices)

# Create your views here.

def index_page(request):
    """returns the homepage"""
    template = "pages/index.html"
    context = {'cities': CITY_CHOICES, 'genders': GENDERS}

    search_query = request.GET.get('q') if request.GET.get('q') != None else ''
    city = request.GET.get('city') if request.GET.get('city') != None else ''
    if city:
        city = CITY_CHOICES[city]
    gender = request.GET.get('gender') if request.GET.get('gender') != None else ''
    if gender:
        gender = GENDERS[gender]
    sort_by = request.GET.get('filter-by') if request.GET.get('filter-by') != None else ''
    context['search_query'] = search_query
    context['city'] = city
    context['gender'] = gender
    context['sort_by'] = sort_by

    friends = FriendSetting.objects.filter(
        Q(is_public=True) &
        Q(friend__first_name__icontains=search_query) &
        Q(friend__city__icontains=city) &
        Q(friend__gender__icontains=gender)
    )
    if friends:
        match sort_by:
            case 'age_up':
                friends = friends.order_by('-friend__birthday')
            case 'age_down':
                friends = friends.order_by('friend__birthday')
            case _:
                pass

    context['friends'] = friends

    return render(request, template, context)

def register_page(request):
    """registration of user"""

    if request.user.is_authenticated:
        return redirect('index')
    
    template = "pages/register.html"
    form = MyUserCreationForm()

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['username'] = post_data['email']
        post_data['password1'] = post_data['password']
        post_data['password2'] = post_data['password']
        post_data['city'] = CITY_CHOICES[post_data['city']]
        post_data['gender'] = GENDERS[post_data['gender']]



        form = MyUserCreationForm(post_data)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email.lower()
            user.email = user.email.lower()
            try:
                user.save()
            except:
                print("REGISTER ERROR")
                print("Nice try apple pie")
            else:
                login(request, user)
                return redirect('index')
        else:
            print("REGISTER ERROR")
            print(form.errors.as_text)

    return render(request, template, {'form': form, 'cities': CITY_CHOICES, 'genders': GENDERS})

def login_page(request):
    """login part"""
    template = "pages/login.html"

    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

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
    context = {'colors':COLORS, 
               'cities': CITY_CHOICES, 
               'educations':EDU_CHOICES, 
               'genders':GENDERS,
               'personality_types': PERSONALITY_TYPES}

    try:
        user = User.objects.get(pk=user_id)
        context["user"] = user
    except:
        return redirect("index")
    
    if user.gender == Genders.VYRAS:
        context['text_ending'] = "as"
    else:
        context['text_ending'] = "ė"
    
    try:
        friend_params = FriendSetting.objects.get(friend=user)
        context["friend_params"] = friend_params
    except:
        pass

    return render(request, template, context)

@login_required
def profile_update_action(request, user_id):
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['city'] = CITY_CHOICES[request.POST.get('city')]
        post_data['gender'] = GENDERS[request.POST.get('gender')]
        post_data['education'] = EDU_CHOICES[request.POST.get('education')]
        post_data['personality_type'] = PERSONALITY_TYPES[request.POST.get('personality_type')]
        form = UserProfileUpdateForm(data=post_data, files=request.FILES, instance=request.user)
        
        if form.is_valid():
            print(request.user.img_one.path)
            print(User._meta.get_field('img_one').get_default())
            user = form.save(commit=False)
            user.save()
        else:
            print(form.errors.as_data)
    return redirect('profile', request.user.pk)

def meeting_page(request):
    """for managing user/friend meetings"""
    template = "pages/meeting-manager.html"
    return render(request, template)