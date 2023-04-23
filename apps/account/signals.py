from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, User


# User model save receiver(Profile)
@receiver(post_save, sender=User)
def user_model_saved(sender, instance, created, *args, **kwargs):
    if created:
        # Create a profile for new user
        profile = Profile.objects.create(user=instance)
        profile.save()
