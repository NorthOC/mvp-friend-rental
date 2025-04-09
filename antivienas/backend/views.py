from django.shortcuts import render, redirect
from .forms import MyUserCreationForm, UserProfileUpdateForm, FriendSettingsUpdateForm
from .forms import MeetingCreationForm, MeetingCancelForm, CreateDisputeForm
from .forms import UserDescriptionUpdateForm, IdImgUploadForm
from .forms import UserImgUploadForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.files import File
from antivienas.database.models import CityOfService, User, Genders, FriendSetting, Order
from antivienas.database.models import InterestColorHexes, EducationChoices, MeetingHours, OrderStatuses, ProfileTypes
from antivienas.database.models import UserProfilePicture, VerifyIdPicture
import datetime as dt

#GLOBAL VARS
CITY_CHOICES = dict((value, key) for key, value in CityOfService.choices)
GENDERS = dict((value, key) for key, value in Genders.choices)
COLORS = dict((value, key) for key, value in InterestColorHexes.choices)
EDU_CHOICES = dict((value, key) for key, value in EducationChoices.choices)
MEETING_HOURS = dict((value, key) for key, value in MeetingHours.choices)
ORDER_STATUSES = dict((value, key) for key, value in OrderStatuses.choices)

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
        Q(friend__city__icontains=city) &
        Q(friend__gender__icontains=gender)
    )

    for query in search_query.split(" "):
        friends = friends.filter(Q(friend__first_name__icontains=query) | Q(friend__last_name__icontains=query))

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
            messages.error(request, 'Wrong password. Please try again.')

    return render(request, template)

def logout_action(request):
    """logout part"""
    logout(request)
    return redirect('index')


def profile_page(request, user_id):
    """viewing of a user/friend profile"""
    template = "pages/profile/profile.html"
    context = {}

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

    context['images'] = UserProfilePicture.objects.filter(user=user).order_by("-is_avatar","created")

    return render(request, template, context)

@login_required
def become_friend_action(request):
    #TODO: Make this proper
    request.user.profile_type = ProfileTypes.FRIEND
    FriendSetting.objects.get_or_create(friend=request.user)

    return redirect('profile', request.user.pk)

@login_required
def profile_update_action(request):
    template = "pages/profile/profile-update.html"
    context = {'colors':COLORS, 
               'cities': CITY_CHOICES, 
               'educations':EDU_CHOICES, 
               'genders':GENDERS,}
    
    if request.method == 'POST':
        post_data = request.POST.copy()

        if request.POST.get('city'):
            post_data['city'] = CITY_CHOICES[request.POST.get('city')]
        if request.POST.get('gender'):
            post_data['gender'] = GENDERS[request.POST.get('gender')]
        if request.POST.get('education'):
            post_data['education'] = EDU_CHOICES[request.POST.get('education')]
        form = UserProfileUpdateForm(data=post_data, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.pk)
        else:
            messages.error(request, form.errors.as_text)
    

    context['images'] = request.user.images.all().order_by("created")
    return render(request, template, context)

@login_required
def description_update_action(request):
    template = "pages/profile/description-update.html"
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        # regex for tel. \+370\s?\d{3}\s?\d{5}
        # email regex. \S*@\S*\s?
        # link regex. https?:\/\/\S+|www\.\S+|[a-zA-Z]{1,}\.[a-zA-Z]{2,}\/\S+

        form = UserDescriptionUpdateForm(data=post_data, instance=request.user)
        
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.pk)
        else:
            messages.error(request, form.errors.as_text)
    return render(request, template)

@login_required
def img_delete_action(request, img_id):
    if request.method == 'POST':
        if img_id >= 0 and img_id <= 3:
            try:
                request.user.images.all().order_by("created")[img_id].delete()
            except:
                pass

        context = {"images": request.user.images.all().order_by("created")}
        return render(request, "components/user-images.html", context=context)

@login_required
def img_upload_action(request):

    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['user'] = request.user

        form = UserImgUploadForm(data=post_data, files=request.FILES)
        
        if form.is_valid():
            image = form.save(commit=False)
            image.crop_and_save()
        else:
            messages.error(request, form.errors.as_text)
        
        context = {"images": request.user.images.all().order_by("created")}
        return render(request, "components/user-images.html", context=context)

@login_required
def select_avatar_action(request, img_id):
    if request.method == 'POST':
        UserProfilePicture.set_avatar(request.user, img_id)
    
        context = {"images": request.user.images.all().order_by("created")}
        return render(request, "components/user-images.html", context=context)

@login_required
def verify_id_page(request):
    template = "pages/profile/verify-id.html"
    context = {}

    if request.user.is_id_verified:
        return redirect('profile', request.user.pk)

    id_image = VerifyIdPicture.objects.filter(user=request.user).first()

    if request.method == 'POST':
        if (id_image and id_image.is_verified is False) or not id_image:
            post_data = request.POST.copy()
            post_data['user'] = request.user

            if id_image:
                form = IdImgUploadForm(instance=id_image,data=post_data, files=request.FILES)
            else:
                form = IdImgUploadForm(data=post_data, files=request.FILES)
            
            if form.is_valid():
                id_image = form.save()
            else:
                messages.error(request, form.errors.as_text)
    
    context['id_img'] = id_image
    return render(request, template, context)

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
                                         (Q(order_status = OrderStatuses.INITIATED) |
                                         Q(order_status = OrderStatuses.CONFIRMED))
                                         )
    else:
        active_orders = Order.objects.filter((Q(friend=friend) | 
                                         Q(user=request.user)) &
                                         (Q(order_status = OrderStatuses.INITIATED) |
                                         Q(order_status = OrderStatuses.CONFIRMED))
                                         )
    
    # update meeting statuses with time
    time_now = dt.datetime.now()
    for order in active_orders:
        order_hours = order.meeting_hour.split(":")
        order_date = dt.datetime.combine(order.meeting_day,dt.time(int(order_hours[0]), int(order_hours[1])))
        if time_now > order_date and order.order_status == OrderStatuses.CONFIRMED:
            order.order_status = OrderStatuses.COMPLETE
            order.save()
        elif time_now > order_date and order.order_status == OrderStatuses.INITIATED:
            order.order_status = OrderStatuses.ABANDONED
            order.save()

    try:
        inactive_orders = Order.objects.filter((Q(friend=friend) | 
                                         Q(user=request.user)) &
                                         (Q(order_status = OrderStatuses.COMPLETE) |
                                         Q(order_status = OrderStatuses.DISPUTED) |
                                         Q(order_status = OrderStatuses.CANCELLED)|
                                         Q(order_status = OrderStatuses.ABANDONED))
                                         )
    except:
        inactive_orders = Order.objects.filter(Q(user=request.user) &
                                         (Q(order_status = OrderStatuses.COMPLETE) |
                                         Q(order_status = OrderStatuses.CANCELLED) |
                                         Q(order_status = OrderStatuses.DISPUTED) |
                                         Q(order_status = OrderStatuses.ABANDONED))
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
        
        if order.order_status == OrderStatuses.INITIATED and request.user == order.user:
            order.delete()
    
    return redirect("meeting-page")

@login_required
def confirm_meeting_action(request):
    if request.method == "POST":
        try:
            order = Order.objects.get(pk=request.POST.get('pk'))
        except:
            return redirect("meeting-page")
        
        if order.order_status == OrderStatuses.INITIATED and request.user == order.friend.friend:
            order.order_status = OrderStatuses.CONFIRMED
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

        if order.order_status == OrderStatuses.INITIATED and request.user == order.friend.friend:
            post_data['order_status'] = OrderStatuses.CANCELLED
            form = MeetingCancelForm(data=post_data, instance=order)
            if form.is_valid:
                form.save()
                
        elif order.order_status == OrderStatuses.COMPLETE and request.user == order.friend.friend:
            order.order_status = OrderStatuses.DISPUTED
            order.save()
            post_data['friend_comment'] = request.POST.get("cancel_reason") if request.POST.get("cancel_reason") != None else ""
            post_data['order'] = order
            form = CreateDisputeForm(post_data)
            if form.is_valid():
                form.save()

        elif order.order_status == OrderStatuses.COMPLETE and request.user == order.user:
            order.order_status = OrderStatuses.DISPUTED
            order.save()
            post_data['user_comment'] = request.POST.get("cancel_reason") if request.POST.get("cancel_reason") != None else ""
            post_data['order'] = order
            form = CreateDisputeForm(post_data)
            if form.is_valid():
                form.save()

    return redirect("meeting-page")
