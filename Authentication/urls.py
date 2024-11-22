from django.urls import path
from . import views
from .views import ResetPasswordView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Role selection page (main entry point)
    path('select_role/', views.select_role, name='select_role'),
    path('test/', views.to_delete_after_dashboard_brige, name='to_delete_after_dashboard_brige'),

    # Home page (index.html)
    path('', views.home_page, name='home_page'),

    # School selection endpoint for redirecting to the appropriate subdomain
    path('select_school/', views.select_school, name='select_school'),

    # Registration paths for all user types
    path('register/<str:user_type>/', views.register_user, name='register_user'),

    # Login path
    path('login/', views.login_user, name='login'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('dashboard/school_admin/', views.school_dashboard, name='school_dashboard'),

    # Logout path
    path('logout/', views.logout_user, name='logout_user'),

    # Email activation path
    path('activate-user/<uidb64>/<token>/', views.activate_user, name='activate'),

    # Resend email validation request
    path('verify-email/<int:user_id>/', views.verify_email, name='verify_email'),
    path('resend-verification-email/<int:user_id>/', views.resend_verification_email, name='resend_verification_email'),

    # OTP Verification
    path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp'),


    # API endpoint to fetch school data
    path('api/schools/', views.get_schools, name='get_schools'),

    # Path for parent approval requests
    path('parent-approval/', views.parent_approval, name='parent_approval'),

    #Password reset
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='authentication/reset_password/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='authentication/reset_password/password_reset_complete.html'), name='password_reset_complete'),
]
