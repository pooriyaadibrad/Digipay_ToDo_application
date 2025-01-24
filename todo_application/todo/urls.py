from django.urls import path

from todo import views

urlpatterns = [
    path('create_list/', views.TodoListCreateApiView.as_view(), name='create_list'),
]
