# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string
from django.templatetags.static import static



class User(AbstractUser):
    is_email_verified = models.BooleanField(default=False)

    # Attributs spécifiques à l'école
    school_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=8, unique=True, null=True, blank=True)  # Le code unique pour chaque utilisateur
    photo = models.ImageField(upload_to='photo/',blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    subdomain = models.CharField(max_length=100, unique=True, null=True, blank=True)

    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('school_admin', 'School Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='student')

    # OTP Code for email verification
    otp_code = models.IntegerField(null=True, blank=True)

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return static('img/woman.jpg')

    def save(self, *args, **kwargs):
        # Génère un code unique de 8 chiffres si ce n'est pas encore défini
        if not self.code:
            self.code = ''.join(random.choices(string.digits, k=8))  # Générer un code unique de 8 chiffres
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.user_type})"


# Modèle pour Student avec clé étrangère vers un User de type School Admin
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    school = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'school_admin'})  # Lié à un User de type 'school_admin'

    def __str__(self):
        return self.user.username



# Modèle pour Teacher avec clé étrangère vers un User de type School Admin
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    school = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'school_admin'})  # Lié à un User de type 'school_admin'

    def __str__(self):
        return self.user.username


class Parent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='parent_profile')
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    is_approved = models.BooleanField(default=False)  # Validation par l'élève

    def __str__(self):
        return f"{self.user.username} (Parent of {self.student.user.username})"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message[:50]}"