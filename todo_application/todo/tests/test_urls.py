# test_todo_urls.py
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from todo.views import TodoListCreateApiView, TodoDetailsApiView

class TodoUrlsTestCase(SimpleTestCase):

    def test_create_list_url_resolves(self):
        """
        Test the 'create_list/' URL routes to the TodoListCreateApiView.
        """
        url = reverse('create_list')
        self.assertEqual(resolve(url).func.view_class, TodoListCreateApiView)

    def test_update_delete_retrieve_url_resolves(self):
        """
        Test the 'update_delete_retrieve/<pk>' URL routes to the TodoDetailsApiView.
        """
        url = reverse('update_delete_retrieve', kwargs={'pk': 'test'})
        self.assertEqual(resolve(url).func.view_class, TodoDetailsApiView)