from django.urls import path
from . import views

urlpatterns = [
    path('home_school_dashboard/', views.home_school_dashboard, name='home_school_dashboard'),
    path('teachers_school_dashboard/', views.teachers_school_dashboard, name='teachers_school_dashboard'),
    path('parents_school_dashboard/', views.parents_school_dashboard, name='parents_school_dashboard'),
    path('students_school_dashboard/', views.students_school_dashboard, name='students_school_dashboard'),
    path('communicate_school_dashboard/', views.communicate_school_dashboard, name='communicate_school_dashboard'),
    path('school_dashboard/', views.school_dashboard, name='school_dashboard'),
]
