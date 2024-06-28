from django.shortcuts import render
from dashboard.models import Task
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    # Fetch tasks categorized by status
    in_progress_tasks = Task.objects.filter(status='In Progress')
    completed_tasks = Task.objects.filter(status='Completed')
    overdue_tasks = Task.objects.filter(status='Overdue')
    users = User.objects.all()

    query = request.GET.get('query', None)
    if query:
        in_progress_tasks = in_progress_tasks.filter(title__icontains=query)
        completed_tasks = completed_tasks.filter(title__icontains=query)
        overdue_tasks = overdue_tasks.filter(title__icontains=query)
        
    # priority = request.GET.get('priority', None)
    # if priority:
    #     in_progress_tasks = in_progress_tasks.order_by(priority)
    #     completed_tasks = completed_tasks.order_by(priority)
    #     overdue_tasks = overdue_tasks.order_by(priority)
    
    due_date = request.GET.get('due_date', None)
    print(due_date)
    if due_date:
        # Parse due_date from string to datetime object
        due_date = datetime.strptime(due_date, '%Y-%m-%d').date()

        in_progress_tasks = in_progress_tasks.filter(due_date__date=due_date)
        completed_tasks = completed_tasks.filter(due_date__date=due_date)
        overdue_tasks = overdue_tasks.filter(due_date__date=due_date)

    category = request.GET.get('category', None)
    if category:
        in_progress_tasks = in_progress_tasks.filter(category__icontains=category)
        completed_tasks = completed_tasks.filter(category__icontains=category)
        overdue_tasks = overdue_tasks.filter(category__icontains=category)

    # Count tasks in each category
    count_in_progress = in_progress_tasks.count()
    count_completed = completed_tasks.count()
    count_overdue = overdue_tasks.count()

    context = {
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'in_progress_counter': count_in_progress,
        'completed_counter': count_completed,
        'overdue_counter': count_overdue,
        'users': users,
        'query': query,
        'category': category,
        'due_date': due_date
    }
    return render(request, 'dashboard/index.html', context)


def search_tasks(request):
    query = request.GET.get('query', '')
    in_progress_tasks = Task.objects.filter(status='In Progress',
                                            title__icontains=query)
    completed_tasks = Task.objects.filter(status='Completed',
                                          title__icontains=query)
    overdue_tasks = Task.objects.filter(status='Overdue',
                                        title__icontains=query)

    context = {
        'in_progress_html': render(request,
                                   'dashboard/index.html',
                                   {'tasks': in_progress_tasks}),
        'completed_html': render(request,
                                 'dashboard/index.html',
                                 {'tasks': completed_tasks}),
        'overdue_html': render(request,
                               'dashboard/index.html',
                               {'tasks': overdue_tasks}),
    }
    return JsonResponse(context)

