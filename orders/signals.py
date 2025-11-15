from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Item
from .firebase_functions import save_item_to_firebase

@receiver(post_save, sender=Item)
def sync_item_to_firebase(sender, instance, **kwargs):
    save_item_to_firebase(instance)
