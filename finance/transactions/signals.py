from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, Balance
from ..authentication.models import UserProfile


@receiver(post_save, sender=Transaction)
def update_balance(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        profile, created = UserProfile.objects.get_or_create(user=user)
        balance = Balance.objects.get(user_profile=profile)
        if instance.transaction_type == 'income':
            balance.amount += instance.amount
            balance.save()
        elif instance.transaction_type == 'expense':
            balance.amount -= instance.amount
            balance.save()

        profile.save()
