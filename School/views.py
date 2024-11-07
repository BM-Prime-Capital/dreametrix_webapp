from django.shortcuts import render

def home_school_dashboard(request):
   return render(request, 'dashboard/school/home.html')

def school_dashboard(request):
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'school': request.user.school_name,
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