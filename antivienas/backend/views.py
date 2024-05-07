from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

def index(request):
    """returns the homepage"""
    template = "pages/index.html"
    return render(request, template)

def register(request):
    """registration of user"""
    pass

def login(request):
    """login part"""
    pass

def profile(request, user_id):
    """viewing of a user/friend profile"""
    pass

def meeting_manager(request):
    """for managing user/friend meetings"""
    template = "pages/meeting-manager.html"
    return render(request, template)