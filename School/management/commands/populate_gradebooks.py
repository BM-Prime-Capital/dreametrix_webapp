import random
from django.core.management.base import BaseCommand
from faker import Faker
from School.models import Class
from Authentication.models import Student
from School.models import Gradebook


class Command(BaseCommand):
    help = 'Populate the Gradebook table with fake data based on existing classes and students'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Dictionnaire des sous-types possibles par type d'évaluation
        ASSESSMENT_SUBTYPES = {
            'EXAM': ['Midterm', 'Final', 'Practical'],
            'TEST': ['Unit 1', 'Unit 2', 'Quiz', 'Pop Quiz'],
            'HOMEWORK': ['Chapter 3', 'Project', 'Essay', 'Worksheet']
        }

        classes = list(Class.objects.all())
        students = list(Student.objects.all())

        if not classes:
            self.stdout.write(self.style.WARNING('Aucune classe trouvée dans la base de données.'))
            return

        if not students:
            self.stdout.write(self.style.WARNING('Aucun étudiant trouvé dans la base de données.'))
            return

        for _ in range(50):  # Augmenté le nombre pour mieux peupler les sous-types
            class_instance = random.choice(classes)
            student = random.choice(students)
            score = round(random.uniform(50, 100), 2)
            assessment_type = random.choice([choice[0] for choice in Gradebook.ASSESSMENT_TYPES])

            # Génération des données avec les nouveaux champs
            gradebook_data = {
                'class_instance': class_instance,
                'student': student,
                'assessment_type': assessment_type,
                'feedback_file': f"feedback/feedback_{student.user.username}_{random.randint(1, 100)}.txt",
                'score': score,
            }

            # Gestion du sous-type (70% de chance d'avoir un sous-type spécifique)
            if random.random() < 0.7 and ASSESSMENT_SUBTYPES.get(assessment_type):
                gradebook_data['subtype'] = random.choice(ASSESSMENT_SUBTYPES[assessment_type])

            # Gestion du voice note (20% de chance d'avoir un enregistrement)
            if random.random() < 0.2:
                gradebook_data['voice_note'] = f"voice_notes/note_{fake.uuid4()}.mp3"

            Gradebook.objects.create(**gradebook_data)

        self.stdout.write(self.style.SUCCESS(f'{Gradebook.objects.count()} entrées de Gradebook créées avec succès !'))