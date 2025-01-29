import random
from django.core.management.base import BaseCommand
from faker import Faker
from School.models import Class  # Assurez-vous d'importer votre modèle Classe
from Authentication.models import Student

class Command(BaseCommand):
    help = 'Populate the Class table with fake data, including existing students'

    def handle(self, *args, **kwargs):
        fake = Faker()
        subjects = ['Math', 'Science', 'History', 'English', 'Art']

        # Récupérer tous les étudiants existants dans la base de données
        students = list(Student.objects.all())

        if not students:
            self.stdout.write(self.style.WARNING('Aucun étudiant trouvé dans la base de données.'))
            return

        for _ in range(10):  # Ajustez la plage pour le nombre de classes que vous souhaitez
            name = fake.word().capitalize()  # Générer un nom de classe aléatoire
            subject = random.choice(subjects)  # Sélectionner un sujet aléatoire
            grade = random.randint(1, 12)  # Sélectionner un grade aléatoire entre 1 et 12

            # Sélectionner un étudiant aléatoire à associer à cette classe
            selected_student = random.choice(students)  # Utiliser un nom différent

            # Créer et enregistrer la nouvelle instance de classe
            new_class = Class.objects.create(name=name, subject=subject, grade=grade)
            new_class.students.add(selected_student)  # Assurez-vous que la relation est bien configurée

        self.stdout.write(
            self.style.SUCCESS('Classes peuplées avec succès avec des données factices et des étudiants existants !'))