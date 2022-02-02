from django.urls import path

from api import views

urlpatterns = [
    path("todos/", views.Todos.as_view()),
    path("todos/<int:pk>/", views.TodoDetails.as_view())
]
