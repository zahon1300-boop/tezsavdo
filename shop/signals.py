from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Mahsulot, Fikr, KaroshaTarixi, SavatchaMahsulot
import logging

logger = logging.getLogger(__name__)
User = get_user_model()


@receiver(post_save, sender=Mahsulot)
def mahsulot_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Yangi mahsulot qoshildi: {instance.nom}")


@receiver(post_save, sender=Fikr)
def fikr_created(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Yangi fikr: {instance.user.username} - {instance.mahsulot.nom}")


@receiver(post_delete, sender='shop.MahsulotRasm')
def rasm_deleted(sender, instance, **kwargs):
    if instance.rasm:
        instance.rasm.delete(save=False)


@receiver(post_save, sender=SavatchaMahsulot)
def savatcha_updated(sender, instance, created, **kwargs):
    if not created:
        logger.info(f"Savatcha yangilandi: {instance.savatcha.id}")
