from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from dashboard.models import Task
from datetime import datetime


class TaskModelTest(TestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            status="In Progress",
            assigned_to=self.user,
            due_date=datetime.now()
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "Test Task")
        self.assertEqual(self.task.description, "This is a test task")
        self.assertEqual(self.task.status, "In Progress")
        self.assertIsInstance(self.task.due_date, datetime)
        self.assertEqual(self.task.assigned_to, self.user)
        self.assertEqual(Task.objects.count(), 1)  

    def test_task_string_representation(self):
        self.assertEqual(str(self.task), self.task.title)

    def test_update_task(self):
        # Update task details
        self.task.title = "Updated Test Task"
        self.task.status = "Completed"
        self.task.save()

        # Fetch the updated task from the database
        updated_task = Task.objects.get(id=self.task.id)

        # Assert the task details have been updated
        self.assertEqual(updated_task.title, "Updated Test Task")
        self.assertEqual(updated_task.status, "Completed")

    def test_delete_task(self):
        # Delete the task
        task_id = self.task.id
        self.task.delete()

        # Assert the task has been deleted from the database
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=task_id)


class DashboardViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_index_view_status_code(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_template(self):
        response = self.client.get(reverse('dashboard'))
        self.assertTemplateUsed(response, 'dashboard/index.html')

    def test_dashboard_view_context(self):
        response = self.client.get(reverse('dashboard'))
        self.assertIn('in_progress_tasks', response.context)
        self.assertIn('completed_tasks', response.context)
        self.assertIn('overdue_tasks', response.context)
        self.assertIn('users', response.context)


class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_view_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'authentication/login.html')

    def test_login_authentication(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('dashboard'))


class LogoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_logout_view(self):
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class MoveTaskViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            status="In Progress",
            assigned_to=self.user,
            due_date=datetime.now()
        )

    def test_move_task_view(self):
        response = self.client.post(reverse('move_task', args=[self.task.id]), {
            'new_status': 'completedColumn'
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.task.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.task.status, 'Completed')


class TaskViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # Create a task
        self.task = Task.objects.create(
            title="Test Task",
            description="This is a test task",
            status="In Progress",
            assigned_to=self.user,
            due_date=datetime.now()
        )

    def test_update_task_view(self):
        # Update task using view
        update_url = reverse('update_task', args=[self.task.id])
        response = self.client.post(update_url, {
            'title': "Updated Test Task",
            'description': "This is an updated test task",
            'status': "Completed",
            'assigned_to': self.user.id,
            'due_date': datetime.now()
        })

        # Assert the view redirects after update
        self.assertEqual(response.status_code, 200)

    def test_delete_task_view(self):
        # Delete task using the view
        delete_url = reverse('delete_task', args=[self.task.id])
        response = self.client.post(delete_url)

        # Assert the view redirects after delete
        self.assertEqual(response.status_code, 302)

        # Assert the task has been deleted from the database
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)
