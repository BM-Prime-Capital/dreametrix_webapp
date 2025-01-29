from django.db import models

from Authentication.models import Student


# Create your models here.
class Class(models.Model):
    name = models.CharField(max_length=100)  # Ex: Class 5 - Math
    subject = models.CharField(max_length=100)
    grade = models.IntegerField()
    students = models.ManyToManyField(Student, related_name='classes')

    def __str__(self):
        return f"{self.name} - {self.subject} (Grade {self.grade})"


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


class Gradebook(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    average = models.FloatField()
    exam_feedback = models.FileField(upload_to='feedback/')
    test_feedback = models.FileField(upload_to='feedback/')
    homework_feedback = models.FileField(upload_to='feedback/')

    def __str__(self):
        return f"Gradebook entry for {self.student.user.username} in {self.class_instance.name}"
