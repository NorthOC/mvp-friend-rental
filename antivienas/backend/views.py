from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

def index(request):
    """returns the homepage"""
    template = "pages/index.html"
    return render(request, template)

def register(request):
    """registration of user"""
    template = "pages/register.html"
    return render(request, template)

def login(request):
    """login part"""
    template = "pages/login.html"
    return render(request, template)

def profile(request, user_id):
    """viewing of a user/friend profile"""
    template = "pages/profile.html"
    context = {"user_id": user_id}
    return render(request, template, context)

def meeting_manager(request):
    """for managing user/friend meetings"""
    template = "pages/meeting-manager.html"
    return render(request, template)