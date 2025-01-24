from django.urls import path

from todo import views

urlpatterns = [
    path('create_list/', views.TodoListCreateApiView.as_view(), name='create_list'),
    path('update_delete_retrieve/<str:pk>',views.TodoDetailsApiView.as_view(), name='update_delete_retrieve')
]
