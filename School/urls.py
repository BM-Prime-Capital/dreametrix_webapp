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

    #STUDENT DASHBOARD
    path('home_student_dashboard/', views.home_student_dashboard, name='home_student_dashboard'),
    path('assignments_student_dashboard/', views.assignments_student_dashboard, name='assignments_student_dashboard'),
    path('gradebook_student_dashboard/', views.gradebook_student_dashboard, name='gradebook_student_dashboard'),
    path('attendance_student_dashboard/', views.attendance_student_dashboard, name='attendance_student_dashboard'),
    path('character_student_dashboard/', views.character_student_dashboard, name='character_student_dashboard'),
    path('seating_student_dashboard/', views.seating_student_dashboard, name='seating_student_dashboard'),
    path('communicate_student_dashboard/', views.communicate_student_dashboard, name='communicate_student_dashboard'),
    path('reports_student_dashboard/', views.reports_student_dashboard, name='reports_student_dashboard'),
    path('teach_student_dashboard/', views.teach_student_dashboard, name='teach_student_dashboard'),
    path('polis_student_dashboard/', views.polis_student_dashboard, name='polis_student_dashboard'),

    #PARENT DASHBOARD
]
