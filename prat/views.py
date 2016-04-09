from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

# Prat Models
from django.contrib.auth.models import User
from prat.models import UserProfile, Task

# Prat Forms
from prat.forms import EditProfileForm

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

@login_required
def editProfile(request):
    if request.method == 'GET':
        form = EditProfileForm()
        context = {
            'form': form,
        }

        return render(request, 'edit_profile.html', context)
    elif request.method ==  'POST':
        form = EditProfileForm(request.POST, request.FILES)
        user = request.user
        profile = user.profile

        if form.is_valid():
            if form.cleaned_data['first_name']:
                profile.first_name = form.cleaned_data['first_name']
            if form.cleaned_data['last_name']:
                profile.last_name = form.cleaned_data['last_name']
            if form.cleaned_data['birthday']:
                profile.birthday = form.cleaned_data['birthday']
            if form.cleaned_data['gender']:
                profile.gender = form.cleaned_data['gender']
            if form['avatar'].value():
                profile.avatar = form['avatar'].value()
            if form.cleaned_data['email']:
                user.email = form.cleaned_data['email']
                user.save()
            profile.save()
        else:
            context = {'form': form}
            return render(request, 'edit_profile.html', context)
        return redirect('viewProfile')
