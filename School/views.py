from django.shortcuts import render, redirect
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
def home_teacher_dashboard(request):
   return render(request, 'dashboard/teacher/home.html')

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


def filter_question(subject, year, number, grade, kind, standard):
    # Construct the absolute path to the Excel file
    excel_file_path = os.path.join(settings.BASE_DIR, "Digital library.xlsx")

    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_file_path)

    # Filter the DataFrame based on the provided parameters
    filtered_df = df.loc[
        (df["Year"] == year) &
        (df["Subject"] == subject) &
        (df["Grade"] == grade) &
        (df["MC/OR"] == kind) &
        (df["Standard"] == standard)  # Added Standard filter
    ]

    # Load the workbook for hyperlink extraction
    workbook = load_workbook(excel_file_path)
    sheet = workbook.active

    links = []
    column = df.columns.get_loc("Link to item")

    try:
        q = random.sample(list(filtered_df.index), number)
    except ValueError:
        raise ValueError("Not enough questions to generate test")

    for ele in q:
        cell = sheet.cell(ele + 2, column + 1)
        link = cell.hyperlink.target
        links.append(link)

    return links


# Fonction pour générer le PDF
def generate_pdf(links):
    doc = fitz.open()
    pdf = doc.new_page(width=595, height=842)  # taille A4
    x, y = 24, 24  # coordonnées initiales
    margin = 5  # marge

    for link in links:
        link = link.replace("dl=0", "raw=1")

        try:
            response = requests.get(link)
            image = BytesIO(response.content)

            if y + 228 > 842 - 24:
                pdf = doc.new_page(width=595, height=842)
                x, y = 24, 24

            pdf.insert_image(fitz.Rect(x, y, x + 228, y + 228), stream=image)
            y += 228 + margin

        except Exception as e:
            raise ValueError(e)
    doc.save("test_generated_today.pdf")


# Vue pour générer le PDF
from django.contrib import messages

def generate_pdf_view(request):
    if request.method == "POST":
        subject = request.POST['subject']
        year = int(request.POST['year'])
        number = int(request.POST['number'])
        grade = int(request.POST['grade'])
        kind = request.POST['kind']
        standard = request.POST['standard']  # Nouveau champ ajouté pour Standard

        try:
            links = filter_question(subject, year, number, grade, kind, standard)
            generate_pdf(links)

            with open("test_generated_today.pdf", "rb") as pdf:
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
    df = pd.read_excel("Digital library.xlsx")
    # Nettoyer les espaces dans les sujets
    subjects = df['Subject'].str.strip().unique().tolist()
    return JsonResponse({'subjects': subjects})


def get_years(request, subject):
    df = pd.read_excel("Digital library.xlsx")

    # Nettoyer le sujet pour enlever les espaces
    subject = subject.strip()

    # Vérifiez si le sujet existe dans le DataFrame
    if subject in df['Subject'].values:
        years = df[df['Subject'].str.strip() == subject]['Year'].unique().tolist()
    else:
        years = []

    return JsonResponse({'years': years})

# API pour obtenir les niveaux en fonction du sujet et de l'année
def get_grades(request, subject, year):
    df = pd.read_excel("Digital library.xlsx")

    # Nettoyer le sujet et l'année pour enlever les espaces
    subject = subject.strip()
    year = str(year).strip()

    print("All unique years:", df['Year'].unique())
    print("All unique grades:", df['Grade'].unique())

    grades = df[(df['Subject'].str.strip() == subject) & (df['Year'].astype(str) == year)]['Grade'].unique().tolist()
    return JsonResponse({'grades': grades})

# API to get standards based on subject, year, and grade
def get_standards(request, subject, year, grade):
    df = pd.read_excel("Digital library.xlsx")

    # Clean the input parameters to remove spaces
    subject = subject.strip()
    year = str(year).strip()
    grade = str(grade).strip()

    standards = df[
        (df['Subject'].str.strip() == subject) &
        (df['Year'].astype(str) == year) &
        (df['Grade'].astype(str) == grade)
    ]['Standard'].unique().tolist()

    return JsonResponse({'standards': standards})


