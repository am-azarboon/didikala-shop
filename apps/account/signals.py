from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Profile


# User model save receiver(Profile)
@receiver(post_save, sender=User)
def user_model_saved(sender, instance, created, **kwargs):
    if created:
        # Create new profile for user
        profile = Profile.objects.create(user=instance)
        profile.save()
