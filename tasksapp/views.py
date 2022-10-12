from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .models import Task
from .forms import TaskForm


def is_get(request):
    '''
    Returns True if the request method is GET.
    '''
    return request.method == 'GET'


def is_post(request):
    '''
    Returns True if the request method is POST.
    '''
    return request.method == 'POST'


def home(request):
    '''
    Renders the homepage.
    '''
    return render(request, 'tasksapp/home.html')


def sign_up_user(request):
    if is_get(request):
        return render(request, 'tasksapp/sign_up_user.html', {'form': UserCreationForm()})
    else:
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        passwords_match: bool = password1 == password2
        full_fields: bool = all((username, password1, password2))

        if passwords_match and full_fields and len(password1) >= 6:
            try:
                user = User.objects.create_user(
                    username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('current_tasks')
            except IntegrityError:
                return render(request, 'tasksapp/sign_up_user.html', {'error': 'The username is already taken. Please choose another one.', 'username': username})
        else:
            if not passwords_match:
                return render(request, 'tasksapp/sign_up_user.html', {'error': 'Passwords do not match.', 'username': username})
            if not full_fields:
                return render(request, 'tasksapp/sign_up_user.html', {'error': 'The fields must not be empty.'})
            if not len(password1) >= 6:
                return render(request, 'tasksapp/sign_up_user.html', {'error': 'Password must be equal or longer than 6 symbols.', 'username': username})


def log_in_user(request):
    if is_get(request):
        return render(request, 'tasksapp/log_in_user.html')
    else:
        username = request.POST['username']
        password = request.POST['password']

        full_fields: bool = all((username, password))

        user = authenticate(request, username=username, password=password)

        if not full_fields:
            return render(request, 'tasksapp/log_in_user.html', {'error': 'The fields must not be empty.', 'username': username})
        if user is None:
            return render(request, 'tasksapp/log_in_user.html', {'error': 'The user does not exist.', 'username': username})
        else:
            login(request, user)
            return redirect('current_tasks')


@login_required
def log_out_user(request):
    if is_post(request):
        logout(request)
        return redirect('home')


@login_required
def create_task(request):
    if is_get(request):
        return render(request, 'tasksapp/create_task.html', {'form': TaskForm()})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('current_tasks')
        except ValueError:
            return render(request, 'tasksapp/create_task.html', {'form': TaskForm(), 'error': 'Title\'s max length: 100. Memo\'s max length: 1000.'})


@login_required
def current_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed_time__isnull=True)
    return render(request, 'tasksapp/current_tasks.html', {'tasks': tasks})


@login_required
def completed_tasks(request):
    tasks = Task.objects.filter(user=request.user, completed_time__isnull=False).order_by('-completed_time')
    return render(request, 'tasksapp/completed_tasks.html', {'tasks': tasks})


@login_required
def task_page(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if is_get(request):
        form = TaskForm(instance=task)
        return render(request, 'tasksapp/task_page.html', {'task': task, 'form': form})
    else:
        try:
            form = TaskForm(request.POST, instance=task)
            form.save()
            if task.completed_time is None:
                return redirect('current_tasks')
            else:
                return redirect('completed_tasks')
        except ValueError:
            return render(request, 'tasksapp/task_page.html', {'task': task, 'form': form, 'error': 'Title\'s max length: 100. Memo\'s max length: 1000.'})


@login_required
def complete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if is_post(request):
        task.completed_time = timezone.now()
        task.save()
        return redirect('current_tasks')


@login_required
def delete_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if is_post(request):
        task.delete()
        if task.completed_time is None:
            return redirect('current_tasks')
        else:
            return redirect('completed_tasks')


@login_required
def redo_task(request, task_pk):
    task = get_object_or_404(Task, pk=task_pk, user=request.user)
    if is_post(request) and task.completed_time:
        task.completed_time = None
        task.save()
        return redirect('completed_tasks')