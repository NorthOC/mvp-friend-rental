"""
URL configuration for antivienas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from antivienas.backend import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_page, name="index"),
    path('registruotis/', views.register_page, name="register"),
    path("prisijungti/", views.login_page, name="login"),
    path("atsijungti/", views.logout_action, name="logout"),
    path("profilis/<int:user_id>/", views.profile_page, name="profile"),
    path("profilis/<int:user_id>/atnaujinti", views.profile_update_action, name="profile-update"),
    path("susitikimai/", views.meeting_page, name="meeting-page")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)