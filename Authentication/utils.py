from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
import base64
from pathlib import Path
from django.conf import settings


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_email_verified))


generate_token = TokenGenerator()



def get_image_url_or_base64(image_path, request):
    """
    Returns an absolute URL for production or a Base64-encoded image for development.
    """
    if settings.DEBUG:
        # Development: Embed the image as Base64
        full_path = Path(settings.STATIC_ROOT) / image_path
        try:
            with open(full_path, "rb") as img_file:
                return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
        except FileNotFoundError:
            raise FileNotFoundError(f"Image file not found at {full_path}")
    else:
        # Production: Generate absolute URL
        return request.build_absolute_uri(settings.STATIC_URL + image_path)

