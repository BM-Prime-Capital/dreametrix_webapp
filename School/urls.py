from django.urls import path
from . import views

urlpatterns = [
    #SCHOOL DASHBOARD
    path('home_school_dashboard/', views.home_school_dashboard, name='home_school_dashboard'),
    path('teachers_school_dashboard/', views.teachers_school_dashboard, name='teachers_school_dashboard'),
    path('parents_school_dashboard/', views.parents_school_dashboard, name='parents_school_dashboard'),
    path('students_school_dashboard/', views.students_school_dashboard, name='students_school_dashboard'),
    path('communicate_school_dashboard/', views.communicate_school_dashboard, name='communicate_school_dashboard'),
    path('school_dashboard/', views.school_dashboard, name='school_dashboard'),

    #TEACHER DASHBOARD
    path('home_teacher_dashboard/', views.home_teacher_dashboard, name='home_teacher_dashboard'),
    path('assignments_teacher_dashboard/', views.assignments_teacher_dashboard, name='assignments_teacher_dashboard'),
    path('attendance_teacher_dashboard/', views.attendance_teacher_dashboard, name='attendance_teacher_dashboard'),
    path('character_teacher_dashboard/', views.character_teacher_dashboard, name='character_teacher_dashboard'),
    path('communicate_teacher_dashboard/', views.communicate_teacher_dashboard, name='communicate_teacher_dashboard'),
    path('gradebook_teacher_dashboard/', views.gradebook_teacher_dashboard, name='gradebook_teacher_dashboard'),
    path('polis_teacher_dashboard/', views.polis_teacher_dashboard, name='polis_teacher_dashboard'),
    path('reports_teacher_dashboard/', views.reports_teacher_dashboard, name='reports_teacher_dashboard'),
    path('seating_teacher_dashboard/', views.seating_teacher_dashboard, name='seating_teacher_dashboard'),
    path('teach_teacher_dashboard/', views.teach_teacher_dashboard, name='teach_teacher_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),


    #STUDENT DASHBOARD
    path('class_student_dashboard/', views.class_student_dashboard, name='class_student_dashboard'),
    path('assignments_student_dashboard/', views.assignments_student_dashboard, name='assignments_student_dashboard'),
    path('gradebook_student_dashboard/', views.gradebook_student_dashboard, name='gradebook_student_dashboard'),
    path('attendance_student_dashboard/', views.attendance_student_dashboard, name='attendance_student_dashboard'),
    path('character_student_dashboard/', views.character_student_dashboard, name='character_student_dashboard'),
    path('communicate_student_dashboard/', views.communicate_student_dashboard, name='communicate_student_dashboard'),
    path('library_student_dashboard/', views.library_student_dashboard, name='library_student_dashboard'),
    path('reward_student_dashboard/', views.reward_student_dashboard, name='reward_student_dashboard'),
    path('tutor_student_dashboard/', views.tutor_student_dashboard, name='tutor_student_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),

    #PARENT DASHBOARD
    path('class_parent_dashboard/', views.class_parent_dashboard, name='class_parent_dashboard'),
    path('assignments_parent_dashboard/', views.assignments_parent_dashboard, name='assignments_parent_dashboard'),
    path('gradebook_parent_dashboard/', views.gradebook_parent_dashboard, name='gradebook_parent_dashboard'),
    path('attendance_parent_dashboard/', views.attendance_parent_dashboard, name='attendance_parent_dashboard'),
    path('communicate_parent_dashboard/', views.communicate_parent_dashboard, name='communicate_parent_dashboard'),
    path('library_parent_dashboard/', views.library_parent_dashboard, name='library_parent_dashboard'),
    path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),


    # Generate digital library
    path('generate_pdf/', views.generate_pdf_view, name='generate_pdf'),
    path('api/subjects/', views.get_subjects, name='get_subjects'),
    path('api/years/<str:subject>/', views.get_years, name='get_years'),
    path('api/grades/<str:subject>/<int:year>/', views.get_grades, name='get_grades'),
]
