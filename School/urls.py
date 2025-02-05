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

    path('generate-pdf/', views.generate_pdf_view, name='generate_pdf'),
    path('get-subjects/', views.get_subjects, name='get_subjects'),
    path('get-grades/<str:subject>/', views.get_grades, name='get_grades'),
    path('get-standards/<str:subject>/<int:grade>/', views.get_standards, name='get_standards'),

    #GRADEBOOK FUNCTIONALITIES
    path('gradebook_list_view/', views.gradebook_list_view, name='get_gradebooks'),  # Render template to list gradebook entries
    path('create_gradebook/', views.create_gradebook_view, name='create_gradebook'),
    # Render template to create a gradebook entry
    path('gradebooks/<int:pk>/update/', views.update_gradebook_view, name='update_gradebook'),
    # Render template to update a gradebook entry
    path('gradebooks/<int:pk>/delete/', views.delete_gradebook_view, name='delete_gradebook'),
    # Render template to delete a gradebook entry
    path('gradebook_calculation/', views.gradebook_calculation, name='gradebook_calculation'),
    # Ajout du paramètre 'kind' dans l'URL
    path('available_link/<str:subject>/<str:grade>/<str:standard>/<str:kind>/', views.get_links, name='get_links'),



    #CLASSES FUNCTIONALITIES
    path('classes/', views.class_list_view, name='get_classes'),  # Render template to list classes
    path('classes/create/', views.create_class_view, name='create_class'),  # Render template to create a class
    path('classes/<int:pk>/update/', views.update_class_view, name='update_class'),  # Render template to update a class
    path('classes/<int:pk>/delete/', views.delete_class_view, name='delete_class'),  # Render template to delete a class

    #ASSIGMENTS FONCTIONNALITIES
    path('assignments/', views.assignment_list_view, name='get_assignments'),  # Render template to list assignments
    path('assignments/create/', views.create_assignment_view, name='create_assignment'),
    # Render template to create an assignment
    path('assignments/<int:pk>/update/', views.update_assignment_view, name='update_assignment'),
    # Render template to update an assignment
    path('assignments/<int:pk>/delete/', views.delete_assignment_view, name='delete_assignment'),
    # Render template to delete an assignment
]