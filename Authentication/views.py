from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.conf import settings
from .models import User, Student, Teacher, Parent, Notification
from .utils import generate_token
from django.contrib.sites.shortcuts import get_current_site
import threading
from django.utils.timezone import now
from datetime import timedelta
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.hashers import make_password


# ================= Role Selection =================
def select_role(request):
    """ View to display role selection screen for Teachers, Students, and Parents """
    return render(request, 'authentication/select_role.html')

def home_page(request):
    """ View to display role selection screen for Teachers, Students, and Parents """
    return render(request, 'index.html')

# ================= Helper Functions =================

# Thread class for sending emails asynchronously
class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

# Pure function to send an activation email
# Function to send activation email
def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate Your Account'

    # Construction de l'URL avec ou sans sous-domaine
    if user.user_type in ['student', 'teacher', 'parent']:
        # Utiliser le sous-domaine de l'école si c'est un étudiant, un enseignant ou un parent
        subdomain = user.school.subdomain if user.user_type != 'school_admin' else None
        domain = f"{subdomain}.{current_site.domain}" if subdomain else current_site.domain
    else:
        # Pas de sous-domaine pour les school_admins
        domain = current_site.domain

    # Render the email body using the template and context
    email_body = render_to_string('authentication/activate.html', {
        'user': user,
        'domain': domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(
        subject=email_subject,
        body=email_body,
        from_email=settings.EMAIL_HOST_USER,
        to=[user.email]
    )

    email.content_subtype = "html"  # Ensures the email is sent as HTML

    if not settings.TESTING:
        email.send()

def register_user(request, user_type):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Création pour les admins d'école
        if user_type == 'school_admin':
            school_name = request.POST.get('school_name')
            address = request.POST.get('address')

            # Vérification de l'existence du sous-domaine
            subdomain = school_name.replace(" ", "").lower()
            if User.objects.filter(subdomain=subdomain).exists():
                messages.error(request, "A school with this subdomain already exists")
                return render(request, 'authentication/register.html', {'user_type': user_type})

            # Création du compte school_admin sans sous-domaine dans le lien d'email
            user = User.objects.create_user(
                school_name=school_name,
                address=address,
                subdomain=subdomain,
                username=username,
                email=email,
                password=password,
                user_type='school_admin'
            )

            send_activation_email(user, request)
            # Rediriger vers la page de vérification de l'email pour le school_admin
            return redirect('verify_email', user.id)

        # Création pour parents, étudiants, enseignants avec sous-domaine
        elif user_type in ['parent', 'student', 'teacher']:
            school_code = request.POST.get('school_code')
            school_admin = User.objects.filter(code=school_code, user_type='school_admin').first()

            if not school_admin:
                messages.error(request, "Invalid school code")
                return render(request, 'authentication/register.html', {'user_type': user_type})

            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists")
                return render(request, 'authentication/register.html', {'user_type': user_type})

            user = User.objects.create_user(
                first_name=request.POST.get('first_name'),
                last_name=request.POST.get('last_name'),
                username=username,
                email=email,
                password=password,
                school=school_admin,
                user_type=user_type
            )

            # Création des profils étudiants ou enseignants
            if user_type == 'student':
                Student.objects.create(user=user, school=school_admin)
            elif user_type == 'teacher':
                Teacher.objects.create(user=user, school=school_admin)
            elif user_type == 'parent':
                student_code = request.POST.get('student_code')
                student = Student.objects.filter(user__code=student_code).first()
                if not student:
                    messages.error(request, "Invalid student code")
                    return render(request, 'authentication/register.html', {'user_type': user_type})
                Parent.objects.create(user=user, student=student)

            # Envoyer un email avec sous-domaine
            send_activation_email(user, request)

            # Redirige vers la page de vérification d'email avec le sous-domaine
            return redirect(f"https://{school_admin.subdomain}.dreametrix.onrender.com/verify_email/{user.id}")

    return render(request, 'authentication/register.html', {'user_type': user_type})


# ================= Authentication (Login/Logout) =================

def login_user(request):
    """ Login view that handles authentication for all user types, including school admins """
    user_type = request.GET.get('user_type', 'student')  # Get the user type from query parameters, default to 'student'

    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # This can be either username or email
        password = request.POST.get('password')

        # Check if the identifier is an email or username
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
                username = user.username  # Retrieve the username based on the email
            except User.DoesNotExist:
                messages.error(request, 'Invalid email or password')
                return render(request, 'authentication/select_role.html', {'user_type': user_type})
        else:
            username = identifier  # If it's not an email, treat it as a username

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        # Check if the user exists and is associated with the correct school (subdomain)
        if user:
            if user.user_type == 'school_admin' or (
                    user.school and request.school_admin and user.school == request.school_admin):
                login(request, user)

                # Redirect to the correct dashboard based on user type
                if user.user_type == 'student':
                    return redirect(f"https://{request.school_admin.subdomain}.dreametrix.onrender.com/student_dashboard/")
                elif user.user_type == 'teacher':
                    return redirect(f"https://{request.school_admin.subdomain}.dreametrix.onrender.com/teacher_dashboard/")
                elif user.user_type == 'parent':
                    return redirect(f"https://{request.school_admin.subdomain}.dreametrix.onrender.com/parent_dashboard/")
                elif user.user_type == 'school_admin':
                    return redirect(f"https://{user.subdomain}.dreametrix.onrender.com/school_admin_dashboard/")
            else:
                messages.error(request, 'Invalid school or mismatch with credentials')
        else:
            messages.error(request, 'Invalid username/email or password')

    return render(request, 'authentication/login.html', {'user_type': user_type})

def logout_user(request):
    """ View for logging out users """
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect(reverse('login'))

# ================= Email Activation =================

def activate_user(request, uidb64, token):
    """ View for activating user accounts via email """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        messages.success(request, 'Email verified successfully! Your account has been created.')

        # Si c'est un school_admin, redirige vers la page d'accueil (index.html)
        if user.user_type == 'school_admin':
            return redirect('home_page')
        else:
            # Pour les autres utilisateurs, redirige vers la page de connexion
            return redirect('login')

    return render(request, 'authentication/activate-failed.html', {"user": user})


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

    expiration_time = now() + timedelta(minutes=1)

    return render(request, 'authentication/verify_email.html', {
        'user': user,
        'expiration_time': expiration_time,
    })


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


def select_school(request, school_subdomain):
    """Redirects user to the selected school's subdomain and renders the select_role template"""

    # In development mode, render the role selection page
    if settings.DEBUG:
        return render(request, 'authentication/select_role.html')

    # In production, redirect and render the select_role template for the subdomain
    else:
        return render(request, 'authentication/select_role.html', {
            'subdomain_url': f"https://{school_subdomain}.dreametrix.onrender.com/select_role/"
        })



def get_schools(request):
    """API endpoint to get the list of schools with verified emails"""
    # Filtrer les schools_admin dont l'email est vérifié
    schools = User.objects.filter(user_type='school_admin', is_email_verified=True).values('school_name', 'code', 'subdomain')
    return JsonResponse(list(schools), safe=False)
