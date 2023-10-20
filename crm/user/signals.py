from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from contact.models import Contact

@receiver(post_save, sender=User)
def update_corresponding_contact(sender, instance, **kwargs):
    try:
        # Check if there's a corresponding contact with the same email
        contact = Contact.objects.get(email=instance.email)
        contact.is_user = instance
        contact.save()
    except Contact.DoesNotExist:
        pass
