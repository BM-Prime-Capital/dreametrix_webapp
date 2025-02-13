from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .models import User, Student, Teacher, Parent, Notification
from .utils import generate_token
import threading
from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token  # Import for generating CSRF token
from django.views.decorators.cache import never_cache
#RESET PASSWORD IMPORTS
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMultiAlternatives
from .utils import get_image_url_or_base64
from random import randint
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError

# Added by Henock
import logging


# Configuration du logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.ERROR, format='%(asctime)s %(levelname)s %(message)s')


# ================= Helper Functions =================

# Thread class for sending emails asynchronously
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# def register_user(request, user_type):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         photo = request.FILES.get('profile_picture')
#         # Check if the email is already taken
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "An account with this email already exists.")
#             return render(request, 'authentication/register.html', {'user_type': user_type})

#         # Check if the username is already taken
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "An account with this username already exists.")
#             return render(request, 'authentication/register.html', {'user_type': user_type})

#         # Registration for school admins
#         if user_type == 'school_admin':
#             school_name = request.POST.get('school_name')
#             address = request.POST.get('address')

#             try:
#                 # Create a user account for the school admin
#                 user = User.objects.create_user(
#                     username=username,
#                     email=email,
#                     password=password,
#                     user_type='school_admin'
#                 )
#                 # Add school-specific details
#                 user.school_name = school_name
#                 user.address = address
#                 user.save()

#                 # Send activation email
#                 send_activation_email(user, request)
#                 return redirect('verify_email', user.id)

#             except IntegrityError:
#                 messages.error(request, "An error occurred while creating the account.")
#                 return render(request, 'authentication/register.html', {'user_type': user_type})

#         # Registration for students and teachers
#         elif user_type in ['student', 'teacher']:
#             school_code = request.POST.get('school_code')
#             school_admin = User.objects.filter(code=school_code, user_type='school_admin').first()

#             if not school_admin:
#                 messages.error(request, "The school code is invalid.")
#                 return render(request, 'authentication/register.html', {'user_type': user_type})

#             try:
#                 user = User.objects.create_user(
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     username=username,
#                     email=email,
#                     password=password,
#                     user_type=user_type
#                 )

#                 # Link the user to the school admin through the respective profile
#                 if user_type == 'student':
#                     Student.objects.create(user=user, school=school_admin)
#                 elif user_type == 'teacher':
#                     Teacher.objects.create(user=user, school=school_admin)

#                 # Send activation email
#                 send_activation_email(user, request)
#                 return redirect('verify_email', user.id)

#             except IntegrityError:
#                 messages.error(request, "An error occurred while creating the account.")
#                 return render(request, 'authentication/register.html', {'user_type': user_type})

#         # Registration for parents
#         elif user_type == 'parent':
#             student_code = request.POST.get('student_code')
#             student = Student.objects.filter(user__code=student_code).first()

#             if not student:
#                 messages.error(request, "The student code is invalid.")
#                 return render(request, 'authentication/register.html', {'user_type': user_type})

#             try:
#                 user = User.objects.create_user(
#                     first_name=request.POST.get('first_name'),
#                     last_name=request.POST.get('last_name'),
#                     username=username,
#                     email=email,
#                     password=password,
#                     user_type='parent'
#                 )

#                 # Link the parent to the specified student
#                 Parent.objects.create(user=user, student=student)

#                 send_activation_email(user, request)
#                 return redirect('verify_email', user.id)

#             except IntegrityError:
#                 messages.error(request, "An error occurred while creating the account.")
#                 return render(request, 'authentication/register.html', {'user_type': user_type})

#     return render(request, 'authentication/register.html', {'user_type': user_type})


# Henock

def register_user(request, user_type='school_admin'):  # Valeur par défaut ajoutée
    # Une validation added au début de la fonction
    if user_type != 'school_admin' and not request.user.is_authenticated:
        return redirect('login')

    if user_type != 'school_admin' and not request.user.is_school_admin:
        messages.error(request, "Unauthorized access")
        return redirect('login')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        photo = request.FILES.get('profile_picture')

        try:
            # Vérification si l'email existe déjà
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return render(request, 'authentication/register.html', {'user_type': user_type})

            # Vérification si le nom d'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                messages.error(request, "An account with this username already exists.")
                return render(request, 'authentication/register.html', {'user_type': user_type})

            if user_type == 'school_admin':
                school_name = request.POST.get('school_name')
                address = request.POST.get('address')

                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    user_type='school_admin'
                )
                user.school_name = school_name
                user.address = address
                user.save()

                send_activation_email(user, request)
                return redirect('verify_email', user.id)

            elif user_type in ['student', 'teacher']:
                school_code = request.POST.get('school_code')
                school_admin = User.objects.filter(code=school_code, user_type='school_admin').first()

                if not school_admin:
                    messages.error(request, "The school code is invalid.")
                    return render(request, 'authentication/register.html', {'user_type': user_type})

                user = User.objects.create_user(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    username=username,
                    email=email,
                    password=password,
                    user_type=user_type
                )

                if user_type == 'student':
                    Student.objects.create(user=user, school=school_admin)
                elif user_type == 'teacher':
                    Teacher.objects.create(user=user, school=school_admin)

                send_activation_email(user, request)
                return redirect('verify_email', user.id)

            elif user_type == 'parent':
                student_code = request.POST.get('student_code')
                student = Student.objects.filter(user__code=student_code).first()

                if not student:
                    messages.error(request, "The student code is invalid.")
                    return render(request, 'authentication/register.html', {'user_type': user_type})

                user = User.objects.create_user(
                    first_name=request.POST.get('first_name'),
                    last_name=request.POST.get('last_name'),
                    username=username,
                    email=email,
                    password=password,
                    user_type='parent'
                )

                Parent.objects.create(user=user, student=student)
                send_activation_email(user, request)
                return redirect('verify_email', user.id)

        except IntegrityError as e:
            logger.error(f"IntegrityError while registering {user_type}: {str(e)}", exc_info=True)
            messages.error(request, "An error occurred while creating the account.")
        except Exception as e:
            logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
            messages.error(request, "An unexpected error occurred. Please try again later.")

    return render(request, 'authentication/register.html', {'user_type': user_type})


# ================= Authentication (Login/Logout) =================
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

@never_cache
def login_user(request):
    """Login view that handles authentication for all user types, including school admins."""
    user_type = request.GET.get('user_type', 'student')  # Default to 'student' if no type is provided

    # Generate a CSRF token if it's missing
    if not request.session.get('csrf_token'):
        get_token(request)

    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # Can be either username or email
        password = request.POST.get('password')

        # Check if the identifier is an email or username
        if '@' in identifier:
            try:
                users = User.objects.filter(email=identifier)

                if not users.exists():
                    messages.error(request, 'Invalid email or password')
                    return render(request, 'authentication/login.html', {'user_type': user_type})

                if users.count() > 1:
                    messages.error(request, 'Multiple accounts found with this email. Please contact support.')
                    return render(request, 'authentication/login.html', {'user_type': user_type})

                username = users.first().username

                # Authenticate using the username
                user = authenticate(request, username=username, password=password)

            except User.MultipleObjectsReturned:
                messages.error(request, 'Multiple accounts found with this email. Please contact support.')
                return render(request, 'authentication/login.html', {'user_type': user_type})

        else:
            # Assume identifier is a username
            user = authenticate(request, username=identifier, password=password)

        if user is not None:
            login(request, user)
            # Redirection selon le type d'utilisateur
            if user.user_type == 'school_admin':
                return redirect('school_dashboard')
            elif user.user_type == 'teacher':
                return redirect('teacher_dashboard')
            elif user.user_type == 'student':
                return redirect('student_dashboard')
            elif user.user_type == 'parent':
                return redirect('parent_dashboard')
        else:
            messages.error(request, 'Invalid credentials')

    return render(request, 'authentication/login.html', {'user_type': user_type})

@login_required
def student_dashboard(request):
    context = {
        'username': request.user.username,
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email,
    }
    return render(request, 'dashboard/student/student_dashboard.html', context)

@login_required
def teacher_dashboard(request):
    context = {
        'username': request.user.username,
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email,
    }
    return render(request, 'dashboard/teacher/teacher_dashboard.html', context)

@login_required
def parent_dashboard(request):
    context = {
        'username': request.user.username,
        'firstname': request.user.first_name,
        'lastname': request.user.last_name,
        'email': request.user.email,
    }
    return render(request, 'dashboard/parent/parent_dashboard.html', context)

@login_required
def school_dashboard(request):
    # Pass user data to the template
    context = {
        'username': request.user.username,
        'email': request.user.email,
        'school': request.user.school_name,
        'role': 'School Leader/Principal'  # Replace with actual role if available
    }
    return render(request, 'dashboard/school/school_dashboard.html', context)

def logout_user(request):
    """ View for logging out users """
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect(reverse('login'))


# ================= Role Selection =================
def select_role(request):
    """ View to display role selection screen for Teachers, Students, and Parents """
    return render(request, 'authentication/select_role.html')

def home_page(request):
    """ View to display role selection screen for Teachers, Students, and Parents """
    return render(request, 'index.html')

def to_delete_after_dashboard_brige(request):
    """ View to display role selection screen for Teachers, Students, and Parents """
    return render(request, 'dashboard/school/school_dashboard.html')

# ================= Email Activation =================

# Fonction d'envoi de l'email d'activation
def send_activation_email(user, request):
    """
        Generate a 4-digit OTP, save it to the user, and send the activation email.
        """
    # Generate OTP
    otp = randint(1000, 9999)
    user.otp_code = otp
    user.save()  # Save OTP to the database

    # Send Activation Email
    current_site = request.get_host()
    email_subject = 'Activate your DreaMetrix account'
    logo_path = 'img/logo.png'  # Path relative to STATIC_ROOT or STATIC_URL

    # Get dynamic image URL or Base64
    logo_url_or_base64 = get_image_url_or_base64(logo_path, request)

    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user),
        'logo_url_or_base64': logo_url_or_base64,
        'otp_code': user.otp_code,  # Pass the saved OTP to the template
    })

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )
    email.content_subtype = "html"
    try:
        email.send()
        logger.info(f"✅ Email envoyé avec succès à {user.email}")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi de l'email :", e)

    # email.send()

def activate_user(request, uidb64, token):
    """ View for activating user accounts via email and redirecting to OTP validation. """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and generate_token.check_token(user, token):
        # Redirect the user to the OTP verification page
        return redirect('verify_otp', user_id=user.id)

    messages.error(request, 'Activation link is invalid or has expired.')
    return render(request, 'authentication/activate-failed.html')

def resend_verification_email(request, user_id):
    user = User.objects.get(pk=user_id)
    if user.is_email_verified:
        messages.info(request, 'Votre email a déjà été vérifié. Vous pouvez maintenant vous connecter.')
        return redirect('login')  # Redirection vers la page de login ou autre

    send_activation_email(user, request)
    messages.success(request, 'A new verification email has been sent.')
    return redirect('verify_email', user.id)

def verify_email(request, user_id):
    """ Page to wait for email verification with a countdown """
    try:
        user = User.objects.get(pk=user_id, is_email_verified=False)
    except User.DoesNotExist:
        return redirect('login')  # Redirect if the user is already verified

    expiration_time = now() + timedelta(minutes=5)

    return render(request, 'authentication/verify_email.html', {
        'user': user,
        'expiration_time': expiration_time,
    })

#Verify otp
def verify_otp(request, user_id):
    """ View for OTP validation """
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        messages.error(request, "Invalid request.")
        return redirect('register')

    if request.method == 'POST':
        otp_input = request.POST.get('otp')  # Get the combined OTP from the hidden input
        if str(user.otp_code) == otp_input:
            user.is_email_verified = True
            user.save()
            messages.success(request, "Your account has been successfully verified!")
            return redirect('login')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'authentication/verify_otp.html', {'user': user})

def send_app_notification_to_student(student_user, parent_user):
    """ Fonction pour envoyer une notification dans l'application """
    Notification.objects.create(
        user=student_user,
        message=f"User {parent_user.first_name} {parent_user.last_name} has registered as your parent. Please approve or reject this request."
    )

def parent_approval(request):
    """ Vue où l'élève voit et gère les demandes de validation parent-enfant """
    student = request.user.student_profile  # Récupère l'étudiant connecté
    parent_requests = Parent.objects.filter(student=student, is_approved=False)  # Récupère les demandes non approuvées

    if request.method == 'POST':
        parent_id = request.POST.get('parent_id')
        action = request.POST.get('action')

        parent = Parent.objects.get(id=parent_id)

        if action == 'approve':
            parent.is_approved = True
            parent.save()
            messages.success(request, 'Parent-child relationship approved.')
        elif action == 'reject':
            parent.delete()
            messages.success(request, 'Parent-child relationship rejected.')

        return redirect('parent_approval')

    return render(request, 'student/parent_approval.html', {'parent_requests': parent_requests})

def select_school(request):
    """Redirects user to the selected school's subdomain and renders the select_role template"""

    # In development mode, render the role selection page
    if settings.DEBUG:
        return render(request, 'authentication/select_role.html')

    # In production, redirect and render the select_role template for the subdomain
    else:
        return render(request, 'authentication/select_role.html')

def get_schools(request):
    """API endpoint to get the list of schools with verified emails"""
    # Filtrer les schools_admin dont l'email est vérifié
    schools = User.objects.filter(user_type='school_admin', is_email_verified=True).values('school_name', 'code', 'subdomain')
    return JsonResponse(list(schools), safe=False)

#RESET PASSWORD
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authentication/reset_password/password_reset.html'
    email_template_name = 'authentication/reset_password/reset_password_email.html'
    #subject_template_name = 'authentication/reset_password/test.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please ensure you've entered the correct address and check your spam folder."
    success_url = reverse_lazy('login')
    success_message = (
        "We've emailed you instructions for setting your password, if an account exists with the email you entered."
        " You should receive them shortly. If you don't receive an email, please check your spam folder."
    )

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Custom send_mail method to use HTML email.
        """
        # Generate subject and body
        subject = render_to_string(subject_template_name, context).strip()
        body_text = render_to_string(email_template_name, context)
        body_html = render_to_string(self.email_template_name, context)

        # Create email message
        email_message = EmailMultiAlternatives(subject, body_text, from_email, [to_email])
        email_message.attach_alternative(body_html, "authentication/reset_password/reset_password_email.html")  # Attach HTML version

        # Send email
        email_message.send()