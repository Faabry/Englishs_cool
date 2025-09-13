from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

# This decorator tells Django to run this function whenever a User object is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Creates or updates the user profile.
    This function is a signal receiver for the User model's post_save signal.
    It ensures that a Profile object is created or updated whenever a User is created or updated.
    
    Arguments:
        sender (Model): The model class that sent the signal. In this case, the User model.
        instance (User): The actual User instance being saved.
        created (bool): True if a new User instance was created.
        kwargs (dict): A dictionary of keyword arguments.
    """
    if created:
        # If a new user was created, also create a new profile for them
        Profile.objects.create(user=instance)
    # The `else` part can be added here if you need to update the profile on every user save
    # For now, we only need to create it.