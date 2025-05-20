from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='created_tasks')
    due_date = models.DateField()
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('INPROGRESS', 'InProgress'),
        ('COMPLETED', 'Completed'),
    )
    status = models.CharField(default="PENDING", choices=STATUS_CHOICES, max_length=20)
    completion_report = models.TextField(blank=True, null=True)
    worked_hours = models.FloatField(blank=True, null=True)


class Admin(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_users')
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_assigned')