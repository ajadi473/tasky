from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from dashboard.models import Task
from .forms import TaskForm
from django.contrib.auth.models import User


# @login_required
def task_list(request):
    tasks = Task.objects.all()
    users = User.objects.all() 
    
    context = {
        'tasks': tasks,
        'users': users, 
    }
    return render(request, 'tasks/index.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


# @login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('/welcome/tasks')
    else:
        form = TaskForm()
    return render(request, '/welcome/tasks', {'form': form})


# @login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})


# @login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})
