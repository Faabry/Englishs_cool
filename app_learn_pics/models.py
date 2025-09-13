from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    A one-to-one extension of the default Django User model,
    used to store additional user-specific data like a verification code.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        """Returns the username of the associated user."""
        return self.user.username

# The signal handlers are now in the signals.py file, as per best practices.
