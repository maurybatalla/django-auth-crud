from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone

# con este decorador y tocando en settings impedimos que entre a un enlace si no esta logueado
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html',)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # registro el usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # esto automaticamente guarda la sesion del  usaurio en el navegador
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Usuario Ya existe',
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'No coinciden las contraseñas',
        })


@login_required
def tasks(request):
    # me va dar las tareas del usuario
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def tasks_completed(request):
    # me va dar las tareas del usuario
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def create_task(request):

    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:

        try:
            # le envio el form.py los datos y que el los guarde
            form = TaskForm(request.POST)
            # aca crea la tarea pero no la guarda
            new_task = form.save(commit=False)
            # para poder agregarle el usuario que siempre viene en el requeest por que django ya lo tiene global (belllo)
            new_task.user = request.user
            # le da guardar y chau ya se guardo
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Ingrese datos validos'
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # pero con esta funcion de django ya contempla si no existe y no explota
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        # task = Task.objects.get(pk=task_id) se puede hacer asi para obtener esa tarea
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            # pero con esta funcion de django ya contempla si no existe y no explota
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            # task = Task.objects.get(pk=task_id) se puede hacer asi para obtener esa tarea
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task': task, 'form': form, 'error': "Error al actualizar tarea"})


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.delete()
        return redirect('tasks')


@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password']
        )

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrectos',
            })
        else:
            login(request, user)
            return redirect('tasks')
