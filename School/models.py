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

    # Champs existants conservés
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assessment_type = models.CharField(max_length=10, choices=ASSESSMENT_TYPES)
    feedback_file = models.FileField(upload_to='feedback/')
    score = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True)

    # Nouveaux champs avec valeurs par défaut et migration sécurisée
    subtype = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        default='GENERAL',  # Valeur par défaut pour les nouvelles entrées
        help_text="Sous-type d'évaluation (ex: 'Unit 1', 'Quiz 2')"
    )

    voice_note = models.FileField(
        upload_to='voice_notes/',
        null=True,
        blank=True,
        verbose_name="Commentaire audio"
    )

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

class School_class_students(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='school_class_students')  # Added related_name
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)  # Clé étrangère vers Student

    def __str__(self):
        return f"Classe: {self.class_id.name}, Élève: {self.student_id.user.first_name} {self.student_id.user.last_name}"

