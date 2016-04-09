from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

# Prat
from django.contrib.auth.models import User
from prat.models import UserProfile, Task

def index(request):
    context = {
        "user": request.user,
        "tasks": ["1", "2", "3"]
    }

    if request.user.is_authenticated():
        return render(request, 'index.html', context)
    else:
        return render(request, 'welcome.html', context)

@login_required
def viewProfile(request, username = None):

    if username:
        user = User.objects.filter(username = username).first()
    else:
        user = request.user
    
    context = {
        'user': user,
        'profile': user.profile
    }

    if request.user.username == username or not username:
        return render(request, 'myprofile.html', context)
    return render(request, 'profile.html', context)
