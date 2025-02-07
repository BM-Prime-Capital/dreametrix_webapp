from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import requests
import fitz
from io import BytesIO
import os
from django.conf import settings
import pandas as pd
import random
from openpyxl import load_workbook
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from .models import Class, Student, ChatHistory
import openai

import qrcode
from io import BytesIO


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

def ai_chat_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/ai_chat.html')

def reports_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/reports.html')

def seating_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/seating.html')

def teach_teacher_dashboard(request):
    return render(request, 'dashboard/teacher/teach.html')

# Récupérer la clé API depuis les paramètres
openai.api_key = settings.OPENAI_API_KEY  

def chatbot_view(request):
    return render(request, "chatbot/chat.html")

def chat_api(request):
    if request.method == "POST":
        user_message = request.POST.get("message")
        user = request.user if request.user.is_authenticated else None

        # Mise à jour de l'appel API pour correspondre à la nouvelle interface
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": user_message}]
        )
    

        # Récupérer la réponse du bot
        bot_response = response.choices[0].message.content
        
        # Enregistrer l'historique de chat pour les utilisateurs authentifiés
        #if user:
            #ChatHistory.objects.create(user=user, message=user_message, response=bot_response)

        return JsonResponse({"response": bot_response})



def filter_math_question(subject, number, grade, standard, kind):

    df = pd.read_excel("Digital library.xlsx")

    filtered_df = df.loc[
        (df["Subject"] == subject) &
        (df["Grade"] == grade) &
        (df["Standard"] == standard) &
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

def filter_lang_question(subject, number, grade, standard,  kind):
    df = pd.read_excel("Dreametrix excel.xlsx")

    filtered_df = df.loc[
        (df["Subject"] == subject) &
        (df["Grade"] == grade) &
        (df["Standard"] == standard) &
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


def generate_pdf(links: list | dict, selected_class: str, subject: str, grade: int, teacher_name: str):
    doc = fitz.open()

    # === Page 1 - Couverture ===
    cover = doc.new_page(width=595, height=842)

    # Configuration du texte
    text_params = {
        "fontname": "helv",
        "fontsize": 20,
        "color": (0, 0, 0)
    }

    # Titre principal (centré manuellement)
    cover.insert_text(
        point=(297, 200),  # Centre horizontal
        text=f"GRADE {grade} {subject.upper()}",
        **text_params
    )

    # Nom du professeur
    cover.insert_text(
        (297, 250),
        teacher_name,
        fontsize=14
    )

    # Titre du quiz
    cover.insert_text(
        (297, 300),
        "Muscle Memory Quiz 1",
        fontsize=16
    )

    # Lignes de saisie
    cover.insert_text((100, 650), "Name: -----------------------------", fontsize=12)
    cover.insert_text((100, 680), f"Class: {selected_class} ------------------------", fontsize=12)

    # === Page 2 - Vide ===
    doc.new_page(width=595, height=842)

    # === Pages de questions ===
    current_page = doc.new_page(width=595, height=842)
    x, y = 50, 50
    img_width = (595 - 100) // 2
    img_height = 350

    if isinstance(links, list):
        for i, link in enumerate(links):
            link = link.replace("dl=0", "raw=1")

            if i % 2 == 0 and i != 0:
                current_page = doc.new_page(width=595, height=842)
                y = 50

            try:
                response = requests.get(link)
                image = BytesIO(response.content)

                if i % 2 == 0:
                    rect = fitz.Rect(x, y, x + img_width, y + img_height)
                else:
                    rect = fitz.Rect(x + img_width + 10, y, 595 - x, y + img_height)
                    y += img_height + 20

                current_page.insert_image(rect, stream=image)

            except Exception as e:
                raise ValueError(e)

    else:
        for story, questions in links.items():
            story = story.replace("dl=0", "raw=1")

            try:
                story_page = doc.new_page(width=595, height=842)
                response = requests.get(story)
                image = BytesIO(response.content)
                story_page.insert_image(fitz.Rect(50, 50, 545, 792), stream=image)

                current_page = doc.new_page(width=595, height=842)
                y = 50

                for i, question in enumerate(questions):
                    question = question.replace("dl=0", "raw=1")

                    if i % 2 == 0 and i != 0:
                        current_page = doc.new_page(width=595, height=842)
                        y = 50

                    response = requests.get(question)
                    image = BytesIO(response.content)

                    if i % 2 == 0:
                        rect = fitz.Rect(x, y, x + img_width, y + img_height)
                    else:
                        rect = fitz.Rect(x + img_width + 10, y, 595 - x, y + img_height)
                        y += img_height + 20

                    current_page.insert_image(rect, stream=image)

            except Exception as e:
                raise ValueError(e)

    # QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=6,
        border=2,
    )
    qr.add_data(selected_class)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    qr_bytes = BytesIO()
    img.save(qr_bytes, format='PNG')
    qr_bytes.seek(0)

    for page in doc:
        page.insert_image(
            fitz.Rect(521, 768, 571, 818),
            stream=qr_bytes
        )
        qr_bytes.seek(0)

    doc.save("test.pdf")

def generate_pdf_view(request):
    if request.method == "POST":
        selected_class = request.POST.get('classes', '')
        if not selected_class:
            messages.error(request, "Veuillez sélectionner une classe.")
            return render(request, 'dashboard/teacher/digital_library.html')

        # Récupérer les informations du professeur
        teacher_name = request.user.get_full_name() or request.user.username
        subject = request.POST['subject']
        number = int(request.POST['number'])
        grade = int(request.POST['grade'])
        kind = request.POST['kind']
        standard = request.POST['standard']

        try:
            if subject == "Math":
                links = filter_math_question(subject, number, grade, standard,  kind)
            else:
                links = filter_lang_question(subject, number, grade, standard, kind)
            generate_pdf(
                links=links,
                selected_class=selected_class,
                subject=subject,
                grade=grade,
                teacher_name=teacher_name  # Nouveau paramètre
            )
            with open("test.pdf", "rb") as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="test_generated.pdf"'
                return response
        except ValueError as e:
            # Ajout d'un message en cas d'erreur
            messages.error(request, str(e))
            return render(request, 'dashboard/teacher/digital_library.html')

    return render(request, 'dashboard/teacher/digital_library.html')

def get_classes(request):
    classes = Class.objects.values('name', 'subject', 'grade')
    return JsonResponse({'classes': list(classes)})

def get_subjects(request):
    """df = pd.read_excel("Digital library.xlsx")"""
    # Nettoyer les espaces dans les sujets
    subjects = ["Math", "Language"]
    return JsonResponse({'subjects': subjects})

def get_grades(request, subject):
    # Sélectionner le bon fichier selon le sujet
    if subject == "Math":
        file_path = "Digital library.xlsx"
    else:  # Language
        file_path = "Dreametrix excel.xlsx"

    df = pd.read_excel(file_path)

    # Filtrer les grades pour le sujet sélectionné
    filtered_df = df[df["Subject"] == subject]
    grades = filtered_df["Grade"].unique().tolist()

    return JsonResponse({'grades': sorted(grades)})

# API to get standards based on subject, year, and grade
def get_standards(request, subject, grade):
    # Sélectionner le bon fichier Excel selon le sujet
    if subject == "Math":
        file_path = "Digital library.xlsx"
    else:  # Language
        file_path = "Dreametrix excel.xlsx"

    df = pd.read_excel(file_path)

    # Filtrer par subject et grade
    filtered_df = df[
        (df["Subject"] == subject) &
        (df["Grade"] == int(grade))
        ]

    # Récupérer les standards uniques
    standards = filtered_df["Standard"].unique().tolist()

    return JsonResponse({'standards': standards})

def get_links(request, subject, grade, standard, kind):
    # Déterminer le bon fichier Excel selon le sujet
    if subject == "Math":
        file_path = "Digital library.xlsx"
    else:  # Language
        file_path = "Dreametrix excel.xlsx"

    df = pd.read_excel(file_path)

    # Ajouter le filtre Standard
    base_filter = (
            (df["Subject"] == subject) &
            (df["Grade"] == int(grade)) &
            (df["Standard"] == standard) &
            (df["MC/OR"] == kind)
    )

    filtered_df = df.loc[base_filter]

    # Charger le classeur Excel pour accéder aux liens
    workbook = load_workbook(file_path)
    sheet = workbook.active

    available_links = []

    for index, row in filtered_df.iterrows():
        value = row["Link to item"]
        if pd.notna(value):
            # Récupérer le lien hypertexte
            cell = sheet.cell(row=index + 2, column=df.columns.get_loc("Link to item") + 1)
            link = cell.hyperlink.target if cell.hyperlink else None
            if link:
                available_links.append(link)

    return JsonResponse({'links': available_links})

def gradebook_calculation(request):
    return render(request, 'dashboard/teacher/calculations.html')



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
        student_ids = request.POST.getlist('students')

        if not name or not subject or not grade:
            return HttpResponseBadRequest("All fields are required.")

        try:
            new_class = Class.objects.create(name=name, subject=subject, grade=grade)
            # Add selected students to the class
            if student_ids:
                valid_student_ids = [int(sid) for sid in student_ids if sid.isdigit()]
                new_class.students.add(*valid_student_ids)

            return redirect('get_classes')
        except Exception as e:
            return HttpResponseBadRequest(f"An error occurred: {e}")
    else:
        # Get all students to display in the form
        students = Student.objects.all()
        return render(request, 'dashboard/teacher/add_new_item_classes.html', {'students': students})

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

from django.db.models import Count, Case, When, FloatField, F, Avg


def gradebook_list_view(request):
    # Agrégation par classe
    class_data = Gradebook.objects.values(
        'class_instance__name'
    ).annotate(
        total_students=Count('student', distinct=True),
        exam_count=Count(Case(When(assessment_type='EXAM', then=1))),
        test_count=Count(Case(When(assessment_type='TEST', then=1))),
        homework_count=Count(Case(When(assessment_type='HOMEWORK', then=1))),
        class_avg=Avg('score')
    ).order_by('class_instance__name')

    classes = Class.objects.all()

    return render(request, 'dashboard/teacher/gradebook.html', {
        'class_data': class_data,
        'classes': classes
    })

def get_classes(request):
    classes = Class.objects.values('name', 'subject', 'grade')
    return JsonResponse({'classes': list(classes)})

def create_gradebook_view(request):
    if request.method == 'POST':
        try:
            class_id = request.POST.get('class_instance')
            assessment_type = request.POST.get('assessment_type')
            feedback_file = request.FILES.get('feedback_image')

            # Récupérer tous les étudiants de la classe
            students = Student.objects.filter(class_students__id=class_id)
            if not students.exists():
                raise ValueError("No students found in this class")

            # Créer une entrée pour chaque étudiant
            for student in students:
                Gradebook.objects.create(
                    class_instance_id=class_id,
                    student=student,
                    assessment_type=assessment_type,
                    feedback_file=feedback_file,
                    score=0.0  # Valeur par défaut à mettre à jour plus tard
                )

            return redirect('get_gradebooks')

        except Exception as e:
            return render(request, 'dashboard/teacher/add_new_item.html', {
                'error': str(e)
            })

    return render(request, 'dashboard/teacher/add_new_item.html')

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

