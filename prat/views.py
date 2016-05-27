from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

# Prat Models
from django.contrib.auth.models import User
from prat.models import (UserProfile, Task, Category, UserTaskActivity,
    Ong, UserGroup)

# Prat Forms
from prat.forms import (EditProfileForm, UserRegisterForm, CreateTaskForm,
    EditTaskForm, CreateGroupForm)

def index(request):
    if request.user.is_authenticated():
        user_tasks = request.user.tasks.all()
        context = {
            "user": request.user,
            "tasks": user_tasks,
            "completed_tasks": filter(lambda task: task.completed(), user_tasks),
            "overdue_tasks": filter(lambda task: task.overdue(), user_tasks)
        }
        return render(request, 'index.html', context)
    else:
        context = {}
        return render(request, 'welcome.html', context)

def register(request):
    if request.method == 'GET':
        form = UserRegisterForm()
        context = {'form': form}
        return render(request, 'register.html', context)
    elif request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.save()

            user_auth = authenticate(username=username, password=password)
            if user_auth is None:
                return redirect('login')
            else:
                login(request, user_auth)
                profile = UserProfile.objects.create(user=user)
                profile.save()
                return redirect('viewProfile', username=username)
        else:
            context = {'form': form}
            return render(request, 'register.html', context)

@login_required
def view_profile(request, username = None):
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
def edit_profile(request):
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
            if form.cleaned_data['username']:
                user.username = form.cleaned_data['username']
                user.save()
            profile.save()
        else:
            context = {'form': form}
            return render(request, 'edit_profile.html', context)
        return redirect('viewProfile')

@login_required
def view_task(request, pk):
    if request.method == 'GET':
        task = Task.objects.get(pk = pk)
        if task.owner == request.user:
            context = {
                'task': task,
                'activity_length': range(task.activity_length())
            }
            return render(request, 'task_details.html', context)
        else:
            return redirect('index')

@login_required
def edit_task(request, pk):
    task = Task.objects.get(pk = pk)
    if task.owner != request.user:
        return redirect('index')

    if request.method == 'GET':
        form = EditTaskForm()
        context = {
            'form': form,
        }
        return render(request, 'edit_task.html', context)
    elif request.method ==  'POST':
        form = EditTaskForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['name']:
                task.name = form.cleaned_data['name']
            if form.cleaned_data['category']:
                task_pk = form.cleaned_data['category']
                task.category = Category.objects.get(pk = task_pk)
            if form.cleaned_data['ong']:
                ong_pk = form.cleaned_data['ong']
                task.ong = Ong.objects.get(pk = ong_pk)
            task.save()
        else:
            context = {'form': form}
            return render(request, 'edit_task.html', context)
        return redirect('viewTask', pk=pk)

@login_required
def delete_task(request, pk):
    task = Task.objects.get(pk=pk)

    if task.owner != request.user:
        return redirect('index')

    task.delete()
    return redirect('index')

@login_required
def restart_task(request, pk):
    task = Task.objects.get(pk=pk)

    if task.owner != request.user:
        return redirect('index')

    activities = UserTaskActivity.objects.filter(task=task).filter(user=request.user).delete()
    return redirect('index')

@login_required
def create_task(request):
    if request.method == 'GET':
        form = CreateTaskForm()
        context = {
            'form': form,
        }
        return render(request, 'create_task.html', context)
    elif request.method == 'POST':
        form = CreateTaskForm(request.POST)
        user = request.user

        if form.is_valid():
            if form.cleaned_data['name']:
                name = form.cleaned_data['name']
            if form.cleaned_data['category']:
                category = form.cleaned_data['category']
            if form.cleaned_data['ong']:
                ong = form.cleaned_data['ong']
            task = Task.objects.create(name = name, category = category,
                                       owner = user, ong = ong)
            task.save()
        else:
            context = {'form': form}
            return render(request, 'create_task.html', context)
        return redirect('index')

@login_required
def complete_task(request, pk):
    if request.method == 'GET':
        task = Task.objects.get(pk = pk)
        if task.owner == request.user and task.completed() is False:
            user = request.user
            profile = user.profile

            # Calculate points & experience gained
            points = task.points_reward * (1 + task.activity_length() * task.points_multiplier)
            experience = task.experience_reward * (1 + task.activity_length() * task.experience_multiplier)

            profile.points = profile.points + points
            profile.giveExperience(experience)
            profile.save()

            # Update task statistics
            task.points_total = task.points_total + points
            task.experience_total = task.experience_total + experience
            task.sessions_total = task.sessions_total + 1
            if (task.activity_length() + 1) > task.sessions_record:
                task.sessions_record = task.activity_length() + 1
            task.save()

            # Create UserTaskActivity
            activity = UserTaskActivity.objects.create(task=task, user=user)
            activity.experience_gained = experience
            activity.points_gained = points
            activity.save()

            context = {
                'task': task,
                'experience': experience,
                'points': points
            }
            return render(request, 'task_reward.html', context)
        else:
            return redirect('index')

def view_ongs(request):
    ong_list = Ong.objects.all()
    context = {'ong_list': ong_list}
    return render(request, 'all_ongs.html', context)

def ong_details(request, pk):
    ong = Ong.objects.get(pk=pk)
    context = {'ong': ong}
    return render(request, 'ong_details.html', context)

@login_required
def view_groups(request):
    if request.user.is_authenticated():
        group_users = UserGroup.objects.all()
        context = {'group_users': group_users}

    return render(request, 'groups.html', context)

@login_required
def create_group(request):
    if request.method == 'GET':
        form = CreateGroupForm()
        context = {
            'form': form,
        }
        return render(request, 'create_group.html', context)
    elif request.method == 'POST':
        form = CreateGroupForm(request.POST)
        user = request.user

        if form.is_valid():
            if form.cleaned_data['name']:
                name = form.cleaned_data['name']
            if form.cleaned_data['description']:
                description = form.cleaned_data['description']
            if form.cleaned_data['task']:
                task = form.cleaned_data['task']

            group = UserGroup.objects.create(name=name, description=description,
                                             task=task)
            group.users.clear()
            group.users.add(user)
            group.save()
        else:
            context = {'form': form}
            return render(request, 'create_group.html', context)
        return redirect('viewGroups')
