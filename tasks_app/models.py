from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('INPROGRESS', 'InProgress'),
        ('COMPLETED', 'Completed'),
    )
    status = models.CharField(default="PENDING", choices=STATUS_CHOICES, max_length=20)
    completion_report = models.TextField()
    worked_hours = models.FloatField()


