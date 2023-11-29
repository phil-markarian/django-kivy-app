from django.urls import path
from . import views

urlpatterns = [
    path('', views.AllTasksView.as_view(), name='all_tasks'),
    path('create/', views.CreateTaskView.as_view(), name='create_task'),
]
