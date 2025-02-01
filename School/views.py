from django.shortcuts import redirect
from django.contrib import messages




#SCHOOL_DASHBOARD
def home_school_dashboard(request):
   return render(request, 'dashboard/school/home.html')

def school_dashboard(request):
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'school': request.user.school_name,
        'photo': request.user.photo,
        'role': 'School Leader/Principal'  # Replace with actual role if available
    }
    return render(request, 'dashboard/school/school_dashboard.html', context)

def teachers_school_dashboard(request):

    return render(request, 'dashboard/school/teachers.html')

def parents_school_dashboard(request):
    return render(request, 'dashboard/school/parents.html')

def students_school_dashboard(request):
    return render(request, 'dashboard/school/students.html')

def communicate_school_dashboard(request):
    return render(request, 'dashboard/school/communicate.html')




#STUDENT_DASHBOARD
def class_student_dashboard(request):
   return render(request, 'dashboard/student/class.html')

def student_dashboard(request):
    context = {
        'username': request.user.username,
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email,
        'photo': request.user.photo,
    }
    return render(request, 'dashboard/student/student_dashboard.html', context)

def assignments_student_dashboard(request):
   return render(request, 'dashboard/student/assignments.html')

def gradebook_student_dashboard(request):
   return render(request, 'dashboard/student/gradebook.html')

def attendance_student_dashboard(request):
   return render(request, 'dashboard/student/attendance.html')

def character_student_dashboard(request):
   return render(request, 'dashboard/student/character.html')

def communicate_student_dashboard(request):
    return render(request, 'dashboard/student/communicate.html')

def library_student_dashboard(request):
    return render(request, 'dashboard/student/library.html')

def reward_student_dashboard(request):
    return render(request, 'dashboard/student/reward.html')

def tutor_student_dashboard(request):
    return render(request, 'dashboard/student/tutor.html')



#PARENT_DASHBOARD
def class_parent_dashboard(request):
   return render(request, 'dashboard/parent/class.html')

def parent_dashboard(request):
    context = {
        'username': request.user.username,
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email,
        'photo': request.user.photo,
    }
    return render(request, 'dashboard/parent/parent_dashboard.html', context)

def assignments_parent_dashboard(request):
   return render(request, 'dashboard/parent/assignments.html')

def gradebook_parent_dashboard(request):
   return render(request, 'dashboard/parent/gradebook.html')

def attendance_parent_dashboard(request):
   return render(request, 'dashboard/parent/attendance.html')

def communicate_parent_dashboard(request):
    return render(request, 'dashboard/parent/communicate.html')

def library_parent_dashboard(request):
    return render(request, 'dashboard/parent/library.html')



#TEACHER_DASHBOARD

def update_profile_photo(request):
    if request.method == "POST":
        user = request.user
        profile_photo = request.FILES.get('profile_picture')  # Récupérer le fichier sélectionné

        if profile_photo:
            user.photo = profile_photo
            user.save()  # Enregistrer la mise à jour
            messages.success(request, "Profile picture updated successfully!")
        else:
            messages.error(request, "Please select a valid image.")

        # Rediriger ou recharger la page en fonction du type d'utilisateur
        return redirect('teacher_dashboard')

    return render(request, 'dashboard/teacher/teacher_dashboard.html')

def teacher_dashboard(request):

    if request.method == "POST":
        user = request.user
        profile_photo = request.FILES.get('profile_picture')  # Récupérer le fichier sélectionné

        if profile_photo:
            user.photo = profile_photo
            user.save()  # Enregistrer la mise à jour
            messages.success(request, "Profile picture updated successfully!")
            context = {
                'username': request.user.username,
                'firstname': request.user.first_name,
                'lastname': request.user.last_name,
                'email': request.user.email,
                'role_user': request.user.user_type,
                'school': request.user.school_name,
                'photo': request.user.photo,
            }
            # Rediriger ou recharger la page en fonction du type d'utilisateur
            return render(request, 'dashboard/teacher/teacher_dashboard.html', context)
        else:
            messages.error(request, "Please select a valid image.")


    context = {
        'username': request.user.username,
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email,
        'role_user': request.user.user_type,
        'school': request.user.school_name,
        'photo': request.user.photo,
    }
    return render(request, 'dashboard/teacher/teacher_dashboard.html',context)


def assignments_teacher_dashboard(request):
   return render(request, 'dashboard/teacher/assignments.html')

def attendance_teacher_dashboard(request):
   return render(request, 'dashboard/teacher/attendance.html')

def character_teacher_dashboard(request):
   return render(request, 'dashboard/teacher/character.html')

def communicate_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/communicate.html')

def gradebook_teacher_dashboard(request):
   return render(request, 'dashboard/teacher/gradebook.html')

def polis_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/polis.html')

def reports_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/reports.html')

def seating_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/seating.html')

def teach_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/teach.html')


from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import pandas as pd
import random
import requests
import fitz
from io import BytesIO
from openpyxl import load_workbook


# Fonction pour filtrer les questions
import os
from django.conf import settings
import pandas as pd
import random
from openpyxl import load_workbook
# Vue pour générer le PDF
from django.contrib import messages


def filter_math_question(subject, year, number, grade, kind):

    df = pd.read_excel("Digital library.xlsx")

    filtered_df = df.loc[
        (df["Year"] == year) &
        (df["Subject"] == subject) &
        (df["Grade"] == grade) &
        (df["MC/OR"] == kind)
    ]

    workbook = load_workbook("Digital library.xlsx")
    sheet = workbook.active

    links = []

    column = df.columns.get_loc("Link to item")
    try:
        q = random.sample(list(filtered_df.index), number)
    except ValueError:
        raise ValueError("Not enough questions to generate test")

    for ele in q:
        cell = sheet.cell(ele+2, column+1)
        link = cell.hyperlink.target
        links.append(link)
    return links


def filter_lang_question(year, number, grade, kind):
    df = pd.read_excel("Dreametrix excel.xlsx")

    filtered_df = df.loc[
        (df["Year"] == year) &
        (df["Grade"] == grade) &
        (df["MC/OR"] == kind)
        ]

    workbook = load_workbook("Dreametrix excel.xlsx")
    sheet = workbook.active


    story_column = df.columns.get_loc("Story")
    stories = random.sample(list(filtered_df.index), number)


    story_links = {}

    def _get_question(story):
        res = []
        value = filtered_df.loc[story, "Story"]
        rows = filtered_df.index[filtered_df["Link to item"] == value].tolist()
        for row in rows:
            cell = sheet.cell(row+2, story_column+2)
            link = cell.hyperlink.target
            res.append(link)
        return res

    for story in stories:
        q = tuple(_get_question(story))

        cell = sheet.cell(story+2, story_column+1)
        link = cell.hyperlink.target
        story_links[link] = q

    return story_links


def generate_pdf(links: list | dict):

    doc = fitz.open()
    pdf = doc.new_page(width=595, height=842) # size of an A4 sheet (595, 842)
    x, y = 24, 24 # x and y initial coordinate
    margin = 5 # margin

    if isinstance(links, list):

        for link in links:
            link = link.replace("dl=0", "raw=1")

            try:
                response = requests.get(link)
                image = BytesIO(response.content)

                if y+228 > 842-24:
                    pdf = doc.new_page(width=595, height=842)
                    x, y = 24, 24

                pdf.insert_image(fitz.Rect(x, y, x+228, y+228), stream=image)
                y += 228+margin

            except Exception as e:
                raise ValueError(e)
    else:
        for story, questions in links.items():
            story = story.replace("dl=0", "raw=1")

            try:
                response = requests.get(story)
                image = BytesIO(response.content)

                pdf.insert_image(fitz.Rect(x, y, x+500, y+750), stream=image)
                pdf = doc.new_page(width=595, height=842)

                for question in questions:
                    question = question.replace("dl=0", "raw=1")

                    response = requests.get(question)
                    image = BytesIO(response.content)

                    if y + 350 > 842 - 24:
                        pdf = doc.new_page(width=595, height=842)
                        x, y = 24, 24

                    pdf.insert_image(fitz.Rect(x, y, x + 350, y + 350), stream=image)
                    y += 350 + margin

            except Exception as e:
                raise ValueError(e)

    doc.save("test.pdf")


def generate_pdf_view(request):
    if request.method == "POST":
        subject = request.POST['subject']
        year = int(request.POST['year'])
        number = int(request.POST['number'])
        grade = int(request.POST['grade'])
        kind = request.POST['kind']
        standard = request.POST['standard']  # Nouveau champ ajouté pour Standard

        try:
            if subject == "Math":
                links = filter_math_question(subject, year, number, grade, kind)
            else:
                links = filter_lang_question(year, number, grade, kind)
            generate_pdf(links)
            with open("test.pdf", "rb") as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="test_generated.pdf"'
                return response
        except ValueError as e:
            # Ajout d'un message en cas d'erreur
            messages.error(request, str(e))
            return render(request, 'dashboard/teacher/digital_library.html')

    return render(request, 'dashboard/teacher/digital_library.html')



# API pour obtenir les sujets
def get_subjects(request):
    """df = pd.read_excel("Digital library.xlsx")"""
    # Nettoyer les espaces dans les sujets
    subjects = ["Math", "Language"]
    return JsonResponse({'subjects': subjects})


def get_years(request, subject):
    df = pd.read_excel("Digital library.xlsx")

    years = df["Year"].unique().tolist()
    print(f" Content: {years}")

    return JsonResponse({'years': years})

# API pour obtenir les niveaux en fonction du sujet et de l'année
def get_grades(request, subject, year):
    df = pd.read_excel("Digital library.xlsx")

    grades = df["Grade"].unique().tolist()
    return JsonResponse({'grades': grades})

# API to get standards based on subject, year, and grade
def get_standards(request, subject, year, grade):
    df = pd.read_excel("Digital library.xlsx")
    standards = df["Standard"].unique().tolist()
    return JsonResponse({'standards': standards})

def gradebook_calculation(request):
    return render(request, 'dashboard/teacher/calculations.html')


from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import Class, Student

def class_list_view(request):
    """Affiche la liste des classes, avec option de filtrage."""
    classes = Class.objects.all()  # Récupérer toutes les classes

    # Récupérer les filtres de la requête
    class_filter = request.GET.get('class')
    subject_filter = request.GET.get('subject')
    grade_filter = request.GET.get('grade')

    if class_filter:
        classes = classes.filter(name=class_filter)
    if subject_filter:
        classes = classes.filter(subject=subject_filter)
    if grade_filter:
        classes = classes.filter(grade=grade_filter)

    # Récupérer les listes uniques pour les filtres
    unique_classes = Class.objects.values_list('name', flat=True).distinct()
    unique_subjects = Class.objects.values_list('subject', flat=True).distinct()
    unique_grades = Class.objects.values_list('grade', flat=True).distinct()

    return render(request, 'dashboard/teacher/home.html', {
        'classes': classes,
        'unique_classes': unique_classes,
        'unique_subjects': unique_subjects,
        'unique_grades': unique_grades,
    })

def create_class_view(request):
    """Handle the creation of a new class."""
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        grade = request.POST.get('grade')

        # Validate inputs
        if not name or not subject or not grade:
            return HttpResponseBadRequest("All fields are required.")

        try:
            # Create the new class
            new_class = Class.objects.create(name=name, subject=subject, grade=grade)

            return redirect('get_classes')  # Redirect to the class list after creation
        except Student.DoesNotExist:
            return HttpResponseBadRequest("Student not found.")
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {e}")

    return render(request, 'dashboard/teacher/add_new_item_classes.html')

def update_class_view(request, pk):
    """Handle the update of an existing class."""
    class_instance = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_instance.name = request.POST.get('name')
        class_instance.subject = request.POST.get('subject')
        class_instance.grade = request.POST.get('grade')
        class_instance.save()
        return redirect('get_classes')  # Redirect to the class list after updating

    return render(request, 'classes/update_class.html', {'class_instance': class_instance})

def delete_class_view(request, pk):
    """Handle the deletion of a class."""
    class_instance = get_object_or_404(Class, pk=pk)
    if request.method == 'POST':
        class_instance.delete()
        return redirect('get_classes')  # Redirect to the class list after deletion

    return render(request, 'dashboard/teacher/add_new_item_classes.html', {'class_instance': class_instance})



from django.shortcuts import render, redirect, get_object_or_404
from .models import Assignment
from .serializers import AssignmentSerializer

def assignment_list_view(request):
    """Render the template to list all assignments."""
    assignments = Assignment.objects.all()
    return render(request, 'assignments/assignment_list.html', {'assignments': assignments})

def create_assignment_view(request):
    """Handle the creation of a new assignment."""
    if request.method == 'POST':
        title = request.POST.get('title')
        assignment_type = request.POST.get('assignment_type')
        average_score = request.POST.get('average_score')
        general_feedback = request.POST.get('general_feedback') == 'on'
        new_assignment = Assignment.objects.create(
            title=title,
            assignment_type=assignment_type,
            average_score=average_score,
            general_feedback=general_feedback
        )
        return redirect('get_assignments')  # Redirect to the assignment list after creation

    return render(request, 'assignments/create_assignment.html')

def update_assignment_view(request, pk):
    """Handle the update of an existing assignment."""
    assignment_instance = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment_instance.title = request.POST.get('title')
        assignment_instance.assignment_type = request.POST.get('assignment_type')
        assignment_instance.average_score = request.POST.get('average_score')
        assignment_instance.general_feedback = request.POST.get('general_feedback') == 'on'
        assignment_instance.save()
        return redirect('get_assignments')  # Redirect to the assignment list after updating

    return render(request, 'assignments/update_assignment.html', {'assignment_instance': assignment_instance})

def delete_assignment_view(request, pk):
    """Handle the deletion of an assignment."""
    assignment_instance = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment_instance.delete()
        return redirect('get_assignments')  # Redirect to the assignment list after deletion

    return render(request, 'assignments/delete_assignment.html', {'assignment_instance': assignment_instance})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Gradebook
from .models import Student
from .serializers import GradebookSerializer

def gradebook_list_view(request):
    """Render the template to list all gradebook entries."""
    gradebooks = Gradebook.objects.all()
    classes = Class.objects.all()  # Récupérer toutes les classes
    return render(request, 'dashboard/teacher/gradebook.html', {'gradebooks': gradebooks, 'classes': classes})

def create_gradebook_view(request):
    """Handle the creation of a new gradebook entry."""
    if request.method == 'POST':
        class_instance_id = request.POST.get('class_instance')  # ID de la classe
        student_id = request.POST.get('student')  # ID de l'élève
        average = request.POST.get('average')  # Note moyenne
        exam_feedback = request.FILES.get('exam_feedback')  # Fichier de feedback d'examen
        test_feedback = request.FILES.get('test_feedback')  # Fichier de feedback de test
        homework_feedback = request.FILES.get('homework_feedback')  # Fichier de feedback de devoir

        class_instance = Class.objects.get(id=class_instance_id)
        student = Student.objects.get(id=student_id)

        new_gradebook = Gradebook.objects.create(
            class_instance=class_instance,
            student=student,
            average=average,
            exam_feedback=exam_feedback,
            test_feedback=test_feedback,
            homework_feedback=homework_feedback
        )

        return redirect('get_gradebooks')  # Redirection vers la liste des gradebooks après la création

    # Récupérer tous les étudiants et classes
    studentss = Student.objects.all()
    classes = Class.objects.all()

    if not studentss:
        print("Aucun étudiant trouvé.")
    else:
        print(f"Étudiants trouvés : {[student.user.username for student in studentss]}")  #

    return render(request, 'dashboard/teacher/add_new_item.html', {
        'students': studentss,
        'classes': classes,  # Si vous avez besoin de sélectionner une classe
    })

def update_gradebook_view(request, pk):
    """Handle the update of an existing gradebook entry."""
    gradebook_instance = get_object_or_404(Gradebook, pk=pk)
    if request.method == 'POST':
        gradebook_instance.student_name = request.POST.get('student_name')
        gradebook_instance.assignment_title = request.POST.get('assignment_title')
        gradebook_instance.score = request.POST.get('score')
        gradebook_instance.feedback = request.POST.get('feedback')
        gradebook_instance.save()
        return redirect('get_gradebooks')  # Redirect to the gradebook list after updating

    return render(request, 'dashboard/teacher/gradebook.html', {'gradebook_instance': gradebook_instance})

def delete_gradebook_view(request, pk):
    """Handle the deletion of a gradebook entry."""
    gradebook_instance = get_object_or_404(Gradebook, pk=pk)
    if request.method == 'POST':
        gradebook_instance.delete()
        return redirect('get_gradebooks')  # Redirect to the gradebook list after deletion

    return render(request, 'dashboard/teacher/gradebook.html', {'gradebook_instance': gradebook_instance})

