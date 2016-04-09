from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

def index(request):
    context = {
        "user": request.user,
        "tasks": ["1", "2", "3"]
    }

    if request.user.is_authenticated():
        return render(request, 'index.html', context)
    else:
        return render(request, 'welcome.html', context)
