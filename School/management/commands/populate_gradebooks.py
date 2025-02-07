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

        for _ in range(30):  # Ajustez le nombre de notes à créer
            class_instance = random.choice(classes)  # Sélectionner une classe aléatoire
            student = random.choice(students)  # Sélectionner un étudiant aléatoire
            score = round(random.uniform(50, 100), 2)  # Générer un score aléatoire

            # Créer des fichiers de feedback fictifs
            feedback_file = f"feedback/feedback_{student.user.username}_{random.randint(1, 100)}.txt"

            # Créer et enregistrer la nouvelle instance de Gradebook
            new_gradebook_entry = Gradebook.objects.create(
                class_instance=class_instance,
                student=student,
                assessment_type=random.choice([choice[0] for choice in Gradebook.ASSESSMENT_TYPES]),  # Sélectionner un type d'évaluation aléatoire
                feedback_file=feedback_file,
                score=score
            )

        self.stdout.write(self.style.SUCCESS('Gradebooks peuplés avec succès avec des données factices !'))