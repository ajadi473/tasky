from django.shortcuts import render
from dashboard.models import Task
from django.contrib.auth.models import User


def index(request):
    # Fetch tasks categorized by status
    in_progress_tasks = Task.objects.filter(status='In Progress')
    count_in_progress = in_progress_tasks.count()
    completed_tasks = Task.objects.filter(status='Completed')
    count_completed = completed_tasks.count()
    overdue_tasks = Task.objects.filter(status='Overdue')
    count_overdue = overdue_tasks.count()
    all_tasks = Task.objects.all()
    users = User.objects.all()

    context = {
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'all_tasks': all_tasks,
        'in_progress_counter': count_in_progress,
        'completed_counter': count_completed,
        'overdue_counter': count_overdue,
        'users': users,
    }
    return render(request, 'dashboard/index.html', context)