from rest_framework import serializers
from .models import Tasks
from django.contrib.auth.models import User
from .models import Admin

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = '__all__'

    def validate(self, data):
        if data.get('status') == 'COMPLETED':
            if not data.get('completion_report'):
                raise serializers.ValidationError(
                    "Completion report is required when marking as completed.")
            if data.get('worked_hours') is None:
                raise serializers.ValidationError(
                    "Worked hours must be specified when marking as completed.")
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
