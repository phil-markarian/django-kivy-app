from django.urls import path
from . import views
from .views import AllTasksView, CreateTaskView, StoreItemList, StoreItemDetail

urlpatterns = [
    path('all_tasks', views.AllTasksView.as_view(), name='all_tasks'),
    path('create', views.CreateTaskView.as_view(), name='create_task'),
    path('store', StoreItemList.as_view(), name='store-list'),
    path('store/<int:pk>', StoreItemDetail.as_view(), name='store-detail'),
]
