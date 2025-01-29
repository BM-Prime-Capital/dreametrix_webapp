# serializers.py
from rest_framework import serializers
from .models import Class
from .models import Assignment
from .models import Gradebook

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'assignment_type', 'average_score', 'general_feedback']


class GradebookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gradebook
        fields = ['id', 'student_name', 'assignment_title', 'score', 'feedback']