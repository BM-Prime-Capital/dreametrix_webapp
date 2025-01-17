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

import fitz  # PyMuPDF
import requests
from io import BytesIO
from PIL import Image
from django.shortcuts import render
import pandas as pd
from django.http import HttpResponse


def digital_library(request):
    # Charger le fichier Excel
    url = "https://www.dropbox.com/scl/fi/d5bqz20hsdsmuya85dl3b/Digital-library.xlsx?rlkey=hb1d0kqbnqesbhbleqb5r3r2c&e=1&dl=1"
    data = pd.read_excel(url)

    # Extraire les valeurs uniques pour les dropdowns
    context = {
        'years': data['Year'].unique().tolist(),
        'subjects': data['Subject'].unique().tolist(),
        'grades': data['Grade'].unique().tolist(),
        'question_numbers': data['Question Number'].unique().tolist(),
        'mc_ors': data['MC/OR'].unique().tolist(),
        'standards': data['Standard'].unique().tolist(),
        'point_values': data['Point Value'].unique().tolist(),
        'key_s': data['Key'].unique().tolist(),
        'link_to_items': data['Link to item'].unique().tolist(),
    }
    return render(request, 'dashboard/teacher/digital_library.html', context)


def resolve_redirect_url(url):
    """
    Résout les redirections d'une URL pour obtenir l'URL finale.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            return response.url
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la résolution de l'URL: {e}")
    return None


def generate_pdf(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        year = request.POST['year']
        subject = request.POST['subject']
        grade = request.POST['grade']
        question_number = request.POST['question_number']
        mc_or = request.POST['mc_or']
        standardd = request.POST['standardd']
        point_value = request.POST['point_value']
        ke_y = request.POST['ke_y']
        link_to_item = request.POST['link_to_item']

        # Vérifier et résoudre l'URL
        resolved_link = resolve_redirect_url(link_to_item)
        if not resolved_link:
            return HttpResponse("Erreur : L'URL de l'image n'est pas valide.", status=400)

        # Créer un document PDF
        doc = fitz.open()

        # Ajouter une page au PDF
        page = doc.new_page()

        # Ajouter les détails de l'examen
        text_x, text_y = 72, 750
        page.insert_text((text_x, text_y), f"Titre de l'examen : Examen Final", fontsize=14)
        page.insert_text((text_x, text_y - 20), f"Année : {year}", fontsize=12)
        page.insert_text((text_x, text_y - 40), f"Matière : {subject}", fontsize=12)
        page.insert_text((text_x, text_y - 60), f"Niveau : {grade}", fontsize=12)

        try:
            # Télécharger l'image
            response = requests.get(resolved_link)
            response.raise_for_status()

            # Ajouter l'image au PDF sans extraire le texte
            img_rect = fitz.Rect(72, 300, 300, 500)
            pixmap = fitz.Pixmap(BytesIO(response.content))  # Utilisation correcte de Pixmap
            page.insert_image(img_rect, pixmap=pixmap)

        except Exception as e:
            print(f"Erreur lors de l'insertion de l'image : {e}")
            page.insert_text((text_x, 300), "Erreur lors du chargement de l'image.", fontsize=12)

        # Sauvegarder le PDF dans un flux
        pdf_data = BytesIO()
        doc.save(pdf_data)
        doc.close()
        pdf_data.seek(0)

        # Retourner le PDF comme réponse
        response = HttpResponse(pdf_data, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="exercise_{year}_{subject}.pdf"'
        return response







