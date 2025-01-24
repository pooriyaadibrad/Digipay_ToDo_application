from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from todo.models import Todo
import uuid


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
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Sample Todo')

    def test_get_empty_todo_list(self):
        """
        Test retrieving the list of todos returns 404 when no todos exist.
        """
        Todo.objects.all().delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_todo_create(self):
        """
        Test creating a new todo.
        """
        data = {
            'title': 'New Todo',
            'description': 'This is a new todo item.',
            'due_date': '2025-02-15',
            'completed': False
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.count(), 2)
        self.assertEqual(response.data['title'], 'New Todo')

    def test_post_todo_create_invalid(self):
        """
        Test creating a new todo with invalid data.
        """
        data = {
            'description': 'This todo has no title.',
            'due_date': '2025-02-15'
        }
        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)


class TodoDetailsAPITestCase(APITestCase):

    def setUp(self):
        # Create a sample Todo instance for testing
        self.todo_id = uuid.uuid4()
        self.todo = Todo.objects.create(
            id=self.todo_id,
            title='Sample Todo',
            description='This is a sample todo item.',
            due_date='2025-01-30',
            completed=False
        )
        self.url = reverse('update_delete_retrieve', kwargs={'pk': self.todo.id})

    def test_get_todo_detail(self):
        """
        Test retrieving the details of a specific todo.
        """
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.todo_id))
        self.assertEqual(response.data['title'], self.todo.title)

    def test_get_non_existent_todo_detail(self):
        """
        Test retrieving details for a todo that does not exist.
        """
        non_existent_url = reverse('update_delete_retrieve', kwargs={'pk': uuid.uuid4()})  # Generate a random UUID
        response = self.client.get(non_existent_url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_todo_update(self):
        """
        Test updating a specific todo.
        """
        updated_data = {
            'title': 'Updated Sample Todo',
            'description': 'This is the updated description.',
            'due_date': '2025-02-15',
            'completed': True
        }
        response = self.client.put(self.url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, updated_data['title'])
        self.assertTrue(self.todo.completed)

    def test_put_todo_update_invalid(self):
        """
        Test updating a todo with invalid data (example: missing required fields).
        """
        invalid_data = {
            'description': 'This todo has no title.',
            'due_date': '2025-02-15'
        }
        response = self.client.put(self.url, invalid_data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_delete_todo(self):
        """
        Test deleting a specific todo.
        """
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Check that the todo is indeed deleted
        self.assertFalse(Todo.objects.filter(id=self.todo_id).exists())

    def test_delete_non_existent_todo(self):
        """
        Test deleting a todo that does not exist.
        """
        non_existent_url = reverse('update_delete_retrieve', kwargs={'pk': uuid.uuid4()})
        response = self.client.delete(non_existent_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
