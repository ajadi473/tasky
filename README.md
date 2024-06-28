# Tasky - Task Management Dashboard

Tasky is a task management dashboard built with Django, using Tailwind CSS , Jquery and Bootstrap for the frontend. It allows users to manage tasks, filter and sort them based on priority, due date, and category, and provides user authentication. A use case is Jira board for task managemebt.

## Features

- Task management with statuses: In Progress, Completed, Overdue
- AJAX-based search functionality
- Task filtering and sorting by priority, due date, and category
- User authentication (login, logout)
- Responsive design using Tailwind CSS and Bootstrap

## Prerequisites

- Python 3.x
- Django 3.x

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/ajadi473/tasky.git

cd tasky

### 2. Create virtualenv

python -m venv venv
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Migrate Database

python3 manage.py migrate

Default users: username: admin / password: admin12345

### 5. Collect files

python3 manage.py collectstatic

### 6. Start development server

python3 manage.py runserver


### 7. To run tests

python3 manage.py test
