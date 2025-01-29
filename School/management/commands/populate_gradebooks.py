import random
from django.core.management.base import BaseCommand
from faker import Faker
from School.models import Class
from Authentication.models import Student
from School.models import Gradebook  # Assurez-vous d'importer votre modèle Gradebook

class Command(BaseCommand):
    help = 'Populate the Gradebook table with fake data based on existing classes and students'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Récupérer toutes les classes et étudiants existants dans la base de données
        classes = list(Class.objects.all())
        students = list(Student.objects.all())

        if not classes:
            self.stdout.write(self.style.WARNING('Aucune classe trouvée dans la base de données.'))
            return

        if not students:
            self.stdout.write(self.style.WARNING('Aucun étudiant trouvé dans la base de données.'))
            return

        for _ in range(30):  # Ajustez le nombre de grades à créer
            class_instance = random.choice(classes)  # Sélectionner une classe aléatoire
            student = random.choice(students)  # Sélectionner un étudiant aléatoire
            average = round(random.uniform(50, 100), 2)  # Générer une moyenne aléatoire

            # Créer des fichiers de feedback fictifs (remplacez par vos propres fichiers si nécessaire)
            exam_feedback = f"feedback/exam_feedback_{student.user.username}.txt"
            test_feedback = f"feedback/test_feedback_{student.user.username}.txt"
            homework_feedback = f"feedback/homework_feedback_{student.user.username}.txt"

            # Créer et enregistrer la nouvelle instance de Gradebook
            new_gradebook_entry = Gradebook.objects.create(
                class_instance=class_instance,
                student=student,
                average=average,
                exam_feedback=exam_feedback,
                test_feedback=test_feedback,
                homework_feedback=homework_feedback
            )

        self.stdout.write(self.style.SUCCESS('Gradebooks peuplés avec succès avec des données factices !'))