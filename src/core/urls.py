from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('todo/', views.TodoListView.as_view(), name='todo_list'),
    path('todo/new/', views.TodoCreateView.as_view(), name='todo_new'),
    path('todo/<int:pk>/', views.TodoDetailView.as_view(),
         name='todo_view'),
    path('todo/<int:pk>/edit/', views.TodoUpdateView.as_view(),
         name='todo_edit'),
    path('update-submit-todo',
         views.update_create_todo_form_with_complete_before,
         name='update-submit-todo'),
    path('complete-todo/<int:pk>/', views.complete_todo, name='complete-todo'),
    path('delete-todo/<int:pk>/', views.delete_todo, name='delete-todo'),
]
