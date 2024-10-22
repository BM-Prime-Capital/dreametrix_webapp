from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from .models import User

class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.META['HTTP_HOST']

        # In local development, use the first part of the host as a subdomain
        if settings.DEBUG and host.startswith('127.0.0.1'):
            subdomain = 'localhost'  # Fallback for local development
        else:
            # Extract subdomain (the first part of the host)
            subdomain = host.split('.')[0]

        # Try to find the school_admin user based on the subdomain
        try:
            school_admin = User.objects.get(subdomain=subdomain, user_type='school_admin')
            request.school_admin = school_admin  # Attach the school_admin object to the request
        except User.DoesNotExist:
            request.school_admin = None  # Handle the case where no school is found (e.g., redirect, error page)

