from django.shortcuts import render, redirect, HttpResponse
from .forms import MyUserCreationForm, UserProfileUpdateForm, FriendSettingsUpdateForm
from .forms import MeetingCreationForm, MeetingCancelForm, CreateDisputeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from antivienas.database.models import CityOfService, User, Genders, FriendSetting, Order
import datetime as dt

#GLOBAL VARS
CITY_CHOICES = dict((value, key) for key, value in CityOfService.choices)
GENDERS = dict((value, key) for key, value in Genders.choices)
COLORS = dict((value, key) for key, value in User.InterestColorHexes.choices)
PERSONALITY_TYPES = dict((value, key) for key, value in User.PersonalityTypes.choices)
EDU_CHOICES = dict((value, key) for key, value in User.EducationChoices.choices)
MEETING_HOURS = dict((value, key) for key, value in Order.MeetingHours.choices)
ORDER_STATUSES = dict((value, key) for key, value in Order.OrderStatuses.choices)

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
               'personality_types': PERSONALITY_TYPES,
               'meeting_hours' : MEETING_HOURS}

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
def become_friend_action(request):
    
    FriendSetting.objects.get_or_create(friend=request.user)

    return redirect('profile', request.user.pk)

@login_required
def profile_update_action(request):
    if request.method == 'POST':
        post_data = request.POST.copy()

        if request.POST.get('city'):
            post_data['city'] = CITY_CHOICES[request.POST.get('city')]
        if request.POST.get('gender'):
            post_data['gender'] = GENDERS[request.POST.get('gender')]
        if request.POST.get('education'):
            post_data['education'] = EDU_CHOICES[request.POST.get('education')]
        if request.POST.get('personality_type'):
            post_data['personality_type'] = PERSONALITY_TYPES[request.POST.get('personality_type')]
        form = UserProfileUpdateForm(data=post_data, files=request.FILES, instance=request.user)
        
        if form.is_valid():
            user = form.save(commit=False)
            if request.POST.get('img_one'):
                user.save_with_img()
            else:
                user.save()
        else:
            print(form.errors.as_data)
    return redirect('profile', request.user.pk)

@login_required
def friend_settings_update_action(request):
    if request.method == 'POST':
        
        try:
            friend = FriendSetting.objects.get(friend=request.user)

            if friend:
                form = FriendSettingsUpdateForm(data=request.POST, instance=friend)
            
                if form.is_valid():
                    user = form.save(commit=False)
                    user.save()
                else:
                    print(form.errors.as_data)
        except:
            pass
    return redirect('profile', request.user.pk)

@login_required
def create_meeting_action(request):
    if request.method == 'POST':
        post_data = request.POST.copy()
        
        user_id = request.POST.get('user_id')
        user = User.objects.get(pk=user_id)
        
        try:
            friend_settings = FriendSetting.objects.get(friend=user)
        except:
            return redirect("index")
        
        if request.POST.get('meeting_hour'):
            post_data['meeting_hour'] = MEETING_HOURS[request.POST.get('meeting_hour')]
        
        if request.POST.get('no_of_hours'):
                price_in_form = int(request.POST.get('total_price'))
                price_in_db = int(request.POST.get('no_of_hours')) * friend_settings.price_per_hour

                if price_in_form != price_in_db:
                    messages.error(request, "PriceError: Price difference in form vs database")
                    redirect('profile', friend_settings.friend.pk)

                post_data['total_price'] = price_in_db

        if friend_settings.is_public and request.user != friend_settings.friend:
            post_data['user'] = request.user
            post_data['friend'] = friend_settings.friend
            form = MeetingCreationForm(post_data)

            if form.is_valid():
                meeting = form.save(commit=False)
                #allowed to create meeting 3 hours before
                time_now = dt.datetime.now() + dt.timedelta(hours=3)
                order_hours = meeting.meeting_hour.split(":")
                order_date = dt.datetime.combine(meeting.meeting_day,dt.time(int(order_hours[0]), int(order_hours[1])))
                if time_now > order_date:
                    messages.error(request, "TimeError: Minimum time to before meeting is 3 hours")
                    redirect('profile', friend_settings.friend.pk)
                else:
                    meeting.save()
                return redirect('meeting-page')
            else:
                print(form.errors.as_data)
                redirect('profile', friend_settings.friend.pk)
        
    return redirect("index")


@login_required
def meeting_page(request):
    """for managing user/friend meetings"""
    template = "pages/meeting-manager.html"
    context = {}
    try:
        friend = FriendSetting.objects.get(friend=request.user)
    except FriendSetting.DoesNotExist:
        active_orders = Order.objects.filter(Q(user=request.user) &
                                         (Q(order_status = Order.OrderStatuses.INITIATED) |
                                         Q(order_status = Order.OrderStatuses.CONFIRMED))
                                         )
    else:
        active_orders = Order.objects.filter((Q(friend=friend) | 
                                         Q(user=request.user)) &
                                         (Q(order_status = Order.OrderStatuses.INITIATED) |
                                         Q(order_status = Order.OrderStatuses.CONFIRMED))
                                         )
    
    # update meeting statuses with time
    time_now = dt.datetime.now()
    for order in active_orders:
        order_hours = order.meeting_hour.split(":")
        order_date = dt.datetime.combine(order.meeting_day,dt.time(int(order_hours[0]), int(order_hours[1])))
        if time_now > order_date and order.order_status == Order.OrderStatuses.CONFIRMED:
            order.order_status = Order.OrderStatuses.COMPLETE
            order.save()
        elif time_now > order_date and order.order_status == Order.OrderStatuses.INITIATED:
            order.order_status = Order.OrderStatuses.ABANDONED
            order.save()

    try:
        inactive_orders = Order.objects.filter((Q(friend=friend) | 
                                         Q(user=request.user)) &
                                         (Q(order_status = Order.OrderStatuses.COMPLETE) |
                                         Q(order_status = Order.OrderStatuses.DISPUTED) |
                                         Q(order_status = Order.OrderStatuses.CANCELLED)|
                                         Q(order_status = Order.OrderStatuses.ABANDONED))
                                         )
    except:
        inactive_orders = Order.objects.filter(Q(user=request.user) &
                                         (Q(order_status = Order.OrderStatuses.COMPLETE) |
                                         Q(order_status = Order.OrderStatuses.CANCELLED) |
                                         Q(order_status = Order.OrderStatuses.DISPUTED) |
                                         Q(order_status = Order.OrderStatuses.ABANDONED))
                                         )
        
    context['active_orders'] = active_orders.order_by("meeting_day")
    context['inactive_orders'] = inactive_orders.order_by("-meeting_day")
    
    return render(request, template, context)

@login_required
def delete_meeting_action(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=request.POST.get('pk'))
        except:
            return redirect("meeting-page")
        
        if order.order_status == Order.OrderStatuses.INITIATED and request.user == order.user:
            order.delete()
    
    return redirect("meeting-page")

@login_required
def confirm_meeting_action(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=request.POST.get('pk'))
        except:
            return redirect("meeting-page")
        
        if order.order_status == Order.OrderStatuses.INITIATED and request.user == order.friend.friend:
            order.order_status = Order.OrderStatuses.CONFIRMED
            order.save()
    
    return redirect("meeting-page")

@login_required
def cancel_meeting_action(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=request.POST.get('pk'))
        except:
            return redirect("meeting-page")
        
        post_data = request.POST.copy()

        if request.POST.get('cancel_reason'):
            post_data['cancel_reason'] = request.POST.get('cancel_reason')

        if order.order_status == Order.OrderStatuses.INITIATED and request.user == order.friend.friend:
            post_data['order_status'] = Order.OrderStatuses.CANCELLED
            form = MeetingCancelForm(data=post_data, instance=order)
            if form.is_valid:
                form.save()
                
        elif order.order_status == Order.OrderStatuses.COMPLETE and request.user == order.friend.friend:
            order.order_status = Order.OrderStatuses.DISPUTED
            order.save()
            post_data['friend_comment'] = request.POST.get("cancel_reason") if request.POST.get("cancel_reason") != None else ""
            post_data['order'] = order
            form = CreateDisputeForm(post_data)
            if form.is_valid():
                form.save()

        elif order.order_status == Order.OrderStatuses.COMPLETE and request.user == order.user:
            order.order_status = Order.OrderStatuses.DISPUTED
            order.save()
            post_data['user_comment'] = request.POST.get("cancel_reason") if request.POST.get("cancel_reason") != None else ""
            post_data['order'] = order
            form = CreateDisputeForm(post_data)
            if form.is_valid():
                form.save()

    return redirect("meeting-page")
