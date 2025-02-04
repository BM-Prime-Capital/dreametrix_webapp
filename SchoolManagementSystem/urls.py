"""
URL configuration for SchoolManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # Add this
from django.conf.urls.static import static  # Add this

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('', include('School.urls')),  # Uncomment and ensure School app exists
    path('', include('Authentication.urls')),  # Application d'authentification
    path('', include('School.urls')),
    #path('select-school/', views.select_school, name='select_school'),  # Ajout d'une page pour la sélection de l'école
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#if settings.DEBUG:
 #   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#if settings.DEBUG:
#   urlpatterns += static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)


# Error handling
handler404 = "helpers.views.handle_not_found"
handler500 = "helpers.views.handle_server_error"
