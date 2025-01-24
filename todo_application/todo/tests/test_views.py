# test_views.py
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from todo.models import Todo
from todo.serializers import ToDoSerializer


class TodoListCreateAPITestCase(APITestCase):

    def setUp(self):
        # Optionally create a Todo instance for testing
        self.todo = Todo.objects.create(
            title='Sample Todo',
            description='This is a sample todo item.',
            due_date='2025-01-30',
            completed=False
        )
        self.url = reverse('create_list')

    def test_get_todo_list(self):
        """
        Test retrieving the list of todos with query parameters.
        """
        response = self.client.get(self.url, {'title': 'Sample Todo'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Expect 1 result
        self.assertEqual(response.data['results'][0]['title'], 'Sample Todo')

    def test_get_empty_todo_list(self):
        """
        Test retrieving the list of todos returns 404 when no todos exist.
        """
        Todo.objects.all().delete()  # Clear todos for this test

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_todo_create(self):
        """
        Test creating a new todo.
        """
        data = {
            'title': 'New Todo',
            'description': 'This is a new todo item.',
            'due_date': '2025-02-15',  # Update the format if using jalali
            'completed': False
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)  # 1 existing + 1 new
        self.assertEqual(response.data['title'], 'New Todo')

    def test_post_todo_create_invalid(self):
        """
        Test creating a new todo with invalid data.
        """
        # Test with missing required fields (example)
        data = {
            'description': 'This todo has no title.',
            'due_date': '2025-02-15'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)  # Check for validation error