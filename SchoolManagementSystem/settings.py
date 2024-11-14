from pathlib import Path
import os
import sys
from decouple import config, Csv
import dj_database_url

# Construction du chemin de base du projet
BASE_DIR = Path(__file__).resolve().parent.parent

# Chargement des variables d'environnement depuis le fichier .env

SECRET_KEY = config('SECRET_KEY', default='mAvtlbIYPcy4ATQz625BVLl2Jw365xYLQCHX/DIqOpDQdTD8/0/n0STIK2EhftIw')


# DEBUG = True pour local et False pour production, par défaut production
DEBUG = False

# Test if the application is running in test mode
TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

# Gestion des hôtes autorisés
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='dreametrix.onrender.com', cast=Csv())

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',  # développement local
    'http://localhost:8000',   # développement local
    'https://dreametrix-u5gk.onrender.com'  # production
]

# Temps d'expiration de la session (en secondes)
SESSION_COOKIE_AGE = 60 * 60 * 24  # Par exemple, 1 jour

# Active la session seulement si l'utilisateur ferme le navigateur
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Pour activer la rotation des cookies à chaque login
CSRF_COOKIE_AGE = None  # Renouvelle le jeton CSRF automatiquement


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'School',  # Application School
    'Authentication',  # Application Authentication
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Pour la gestion des fichiers statiques en production
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'Authentication.middleware.TenantMiddleware',  # Ajout du middleware pour la gestion des sous-domaines
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'SchoolManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SchoolManagementSystem.wsgi.application'


# Configuration de la base de données
if DEBUG:
    # Configuration pour le mode local
    DATABASES = {
        'default': {
            'ENGINE': config('DB_ENGINE'),
            'NAME': config('DB_NAME'),
            'USER': config('DB_USER'),
            'PASSWORD': config('DB_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', cast=int),
        }
    }
else:
    # Configuration pour Railway ou production avec dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
    }

# Validation des mots de passe
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalisation
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuration des fichiers statiques
STATIC_URL = '/static/'

# Répertoire pour collecter les fichiers statiques lors du déploiement
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Répertoires pour les fichiers statiques en développement
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'SchoolManagementSystem/static')]

# Configuration du stockage des fichiers statiques avec WhiteNoise en production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuration de l'envoi des emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Modèle personnalisé pour les utilisateurs
AUTH_USER_MODEL = "Authentication.User"

# URL de connexion
LOGIN_URL = "/auth/login"
