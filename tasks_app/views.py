from rest_framework.views import APIView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import Tasks
from .serializers import TaskSerializer, AdminSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth import login
from .models import Admin

def is_admin(user):
    return user.is_staff and not user.is_superuser

def is_superadmin(user):
    return user.is_superuser

class IsAdminOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    from django.contrib.auth.models import User

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        due_date = request.POST.get("due_date")
        assigned_to_id = request.POST.get("assigned_to")

        if title and description and due_date and assigned_to_id:
            assigned_to = User.objects.get(id=assigned_to_id)
            Tasks.objects.create(
                title=title,
                description=description,
                due_date=due_date,
                assigned_to=assigned_to,
                created_by=request.user,
            )
            return redirect('admin_dashboard')

    tasks = Tasks.objects.filter(created_by=request.user)
    completed_tasks = tasks.filter(status='COMPLETED')
    users = User.objects.filter(is_staff=False, is_superuser=False)

    return render(request, 'admin_dashboard.html', {
        'tasks': tasks,
        'completed_tasks': completed_tasks,
        'users': users
    })

@login_required
@user_passes_test(is_superadmin)
def superadmin_dashboard(request):
    tasks = Tasks.objects.all()
    return render(request, 'superadmin_dashboard.html', {'tasks': tasks})

class TasksViewSet(viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Tasks.objects.all()
        elif user.is_staff:
            return Tasks.objects.filter(created_by=user)
        else:
            return Tasks.objects.filter(assigned_to=user)

class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('superadmin_dashboard')
        elif user.is_staff:
            return reverse_lazy('admin_dashboard')
        else:
            raise Exception("Admin panel access only for admins")

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.save()
        return user

class RegisterPage(FormView):
    template_name = 'registration/register.html'
    form_class = CustomUserCreationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class AdminView(generics.ListCreateAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class TaskListView(generics.ListAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSuperAdmin]

class AdminTaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tasks.objects.all()
        return Tasks.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TaskReportsView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAdminOrSuperAdmin]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tasks.objects.filter(status='COMPLETED')
        return Tasks.objects.filter(status='COMPLETED', created_by=self.request.user)


class CompleteTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            task = Tasks.objects.get(pk=pk, assigned_to=request.user)
        except Tasks.DoesNotExist:
            return Response({'error': 'Task not found'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(status='COMPLETED')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)