from django.urls import path
from . import views

urlpatterns = [
    # Role selection page (main entry point)
    path('select_role/', views.select_role, name='select_role'),

    # Home page (index.html)
    path('', views.home_page, name='home_page'),

    # School selection endpoint for redirecting to the appropriate subdomain
    path('select_school/', views.select_school, name='select_school'),

    # Registration paths for all user types
    path('register/<str:user_type>/', views.register_user, name='register_user'),

    # Login path
    path('login/', views.login_user, name='login'),

    # Logout path
    path('logout/', views.logout_user, name='logout_user'),

    # Email activation path
    path('activate-user/<uidb64>/<token>/', views.activate_user, name='activate'),

    # Resend email validation request
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
    path('resend-verification-email/<int:user_id>/', views.resend_verification_email, name='resend_verification_email'),

    # API endpoint to fetch school data
    path('api/schools/', views.get_schools, name='get_schools'),

    # Path for parent approval requests
    path('parent-approval/', views.parent_approval, name='parent_approval'),
]
