from django.urls import path, include
from .views import (TasksViewSet, admin_dashboard, superadmin_dashboard,
                    RoleBasedLoginView, RegisterPage, UserDetailView, AdminView,
                    TaskListView, UserListCreateView, AdminTaskListView,
                    TaskReportsView, CompleteTaskView)
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LogoutView

router = DefaultRouter()
router.register(r'tasks', TasksViewSet, basename='task')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('admin-panel/', admin_dashboard,name='admin_dashboard'),
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),

    path('superadmin/users/', UserListCreateView.as_view(), name='user-list'),
    path('superadmin/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('superadmin/assign-user/', AdminView.as_view(), name='assign-user'),
    path('tasks/<int:pk>/complete/', CompleteTaskView.as_view(), name='task-complete'),
    path('admin/tasks/', AdminTaskListView.as_view(), name='admin_task_list'),
    path('admin/reports/', TaskReportsView.as_view(), name='admin_task_reports')
    path('superadmin/tasks/', TaskListView.as_view(), name='task-list'),

]