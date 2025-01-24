from django.test import TestCase
from todo.models import Todo
import jdatetime


class TodoModelTest(TestCase):

    def setUp(self):
        """
        Create a Todo instance for testing.
        """
        self.todo = Todo.objects.create(
            title='Test Todo',
            description='This is a test todo item.',
            due_date=jdatetime.date(2025, 1, 30),
        )

    def test_todo_creation(self):
        """
        Test that the Todo instance is created correctly.
        """
        self.assertEqual(self.todo.title, 'Test Todo')
        self.assertEqual(self.todo.description, 'This is a test todo item.')
        self.assertEqual(self.todo.due_date, jdatetime.date(2025, 1, 30))
        self.assertFalse(self.todo.completed)

    def test_string_representation(self):
        """
        Test the string representation of the Todo instance.
        """
        self.assertEqual(str(self.todo), 'Test Todo')

    def test_todo_completed_default(self):
        """
        Test that a new Todo instance is not completed by default.
        """
        new_todo = Todo.objects.create(
            title='New Todo',
            description='Another test todo item.',
            due_date=jdatetime.date(2025, 2, 15)
        )
        self.assertFalse(new_todo.completed)

    def test_todo_update(self):
        """
        Test that the Todo instance can be updated.
        """
        self.todo.title = 'Updated Test Todo'
        self.todo.completed = True
        self.todo.save()
        self.assertTrue(Todo.objects.get(id=self.todo.id).completed)
        self.assertEqual(self.todo.title, 'Updated Test Todo')

    def test_due_date_field(self):
        """
        Test the due date field to ensure it accepts valid dates.
        """
        self.assertIsInstance(self.todo.due_date, jdatetime.date)

    def test_deletion_todo(self):
        self.todo.delete()
        self.assertEqual(Todo.objects.count(), 0)
