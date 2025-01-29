import random
from django.core.management.base import BaseCommand
from faker import Faker
from School.models import Class
from Authentication.models import Student
from School.models import Assignment  # Assurez-vous d'importer votre modèle Assignment

class Command(BaseCommand):
    help = 'Populate the Assignment table with fake data based on existing classes'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Récupérer toutes les classes existantes dans la base de données
        classes = list(Class.objects.all())
        students = list(Student.objects.all())

        if not classes:
            self.stdout.write(self.style.WARNING('Aucune classe trouvée dans la base de données.'))
            return

        if not students:
            self.stdout.write(self.style.WARNING('Aucun étudiant trouvé dans la base de données.'))
            return

        assignment_types = [Assignment.HOMEWORK, Assignment.TEST, Assignment.EXAM]

        for _ in range(20):  # Ajustez le nombre d'assignements à créer
            class_instance = random.choice(classes)  # Sélectionner une classe aléatoire
            assignment_type = random.choice(assignment_types)  # Sélectionner un type d'assignement aléatoire
            average_score = round(random.uniform(50, 100), 2)  # Générer un score moyen aléatoire
            general_feedback = random.choice([True, False])  # Feedback général aléatoire
            specific_feedback_count = random.randint(0, 5)  # Nombre de feedbacks spécifiques aléatoires

            # Créer et enregistrer la nouvelle instance d'assignement
            new_assignment = Assignment.objects.create(
                class_instance=class_instance,
                assignment_type=assignment_type,
                average_score=average_score,
                general_feedback=general_feedback,
                specific_feedback_count=specific_feedback_count
            )

            # Associer des étudiants à cet assignement
            selected_students = random.sample(students, k=random.randint(1, min(5, len(students))))  # Sélectionner entre 1 et 5 étudiants
            new_assignment.students.set(selected_students)  # Associer les étudiants à l'assignement

        self.stdout.write(self.style.SUCCESS('Assignments peuplés avec succès avec des données factices !'))