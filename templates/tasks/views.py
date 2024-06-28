from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from dashboard.models import Task
from .forms import TaskForm
from django.contrib.auth.models import User
from django.db.models import Q
import json


@login_required
def task_list(request):
    tasks = Task.objects.all()
    users = User.objects.all()
    query = request.GET.get('q')

    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) |
            Q(assigned_to__username=query) 
        )

    context = {
        'tasks': tasks,
        'users': users, 
    }
    return render(request, 'tasks/index.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)

    data = {
        'title': task.title,
        'description': task.description,
        'status': task.status,
        'priority': task.priority,
        'due_date': task.due_date.isoformat(),
        'assigned_to': task.assigned_to.username,
    }
    return JsonResponse(data)


@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()
    return render(request, 'tasks', {'form': form})


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/index.html', {'form': form})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


# @require_http_methods(['PATCH'])
def move_task(request, pk):
    task = get_object_or_404(Task, id=pk)

    if request.method == 'POST':
        updated_status_column = request.POST.get('new_status')

        print(updated_status_column)
        if updated_status_column == 'overdueColumn':
            task.status = 'Overdue'
        elif updated_status_column == 'completedColumn':
            task.status = 'Completed'
        elif updated_status_column == 'inProgressColumn':
            task.status = 'In Progress'
        else:
            pass

        task.save()

    return JsonResponse({'message': 'Task status updated successfully'})
