from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from Authentication.models import Student

# Get the custom user model
User = get_user_model()  

# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=100)  # Ex: Class 5 - Math
    subject = models.CharField(max_length=100)
    grade = models.IntegerField()
    students = models.ManyToManyField(Student, related_name='classes')

    def __str__(self):
        return f"{self.name} - {self.subject} (Grade {self.grade})"

class Gradebook(models.Model):
    ASSESSMENT_TYPES = (
        ('EXAM', 'Exam'),
        ('TEST', 'Test'),
        ('HOMEWORK', 'Homework'),
    )

    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=10, choices=ASSESSMENT_TYPES)
    feedback_file = models.FileField(upload_to='feedback/')
    score = models.FloatField()  # À utiliser plus tard pour le calcul de la moyenne
    date_added = models.DateTimeField(auto_now_add=True)

class Assignment(models.Model):
    HOMEWORK = 'HW'
    TEST = 'TEST'
    EXAM = 'EXAM'
    ASSIGNMENT_TYPES = [
        (HOMEWORK, 'Homework'),
        (TEST, 'Test'),
        (EXAM, 'Exam'),
    ]

    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    assignment_type = models.CharField(max_length=10, choices=ASSIGNMENT_TYPES)
    average_score = models.FloatField()
    general_feedback = models.BooleanField(default=False)
    specific_feedback_count = models.IntegerField(default=0)
    students = models.ManyToManyField(Student, related_name='assignments')

    def __str__(self):
        return f"{self.assignment_type} for {self.class_instance.name}"

class ChatHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonyme'}: {self.message[:50]}"

