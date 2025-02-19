from datetime import timedelta

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now

from app.models import User, Profile, Result, Notification


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, show_instruction=True)
        total_users = User.objects.count()
        subject = "Yangi foydalanuvchi ro'yxatdan o'tdi"
        message = f"User: {instance.email}\n\nJami foydalanuvchilar soni: {total_users}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = ['shuhratsattorov2004@gmail.com']

        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
            fail_silently=False,
        )


@receiver(post_save, sender=Result)
def notify_users_about_results(sender, instance, **kwargs):
    """
    Testning deadline muddati tugagandan keyin 1 kun ichida natijalar e'lon qilinsa,
    foydalanuvchilarga xabar yuborish.
    """
    test = instance.test  # Natijalar qaysi testga tegishli ekanligini aniqlaymiz
    current_date = now().date()

    # Deadline tugaganidan keyin 1 kun ichida bo‘lsa, foydalanuvchilarga xabar yuboriladi
    if test.deadline and test.deadline < current_date <= test.deadline + timedelta(days=1):
        Notification.objects.create(
            user=instance.user,
            notification=f"Natijalar elon qilindi, test: {instance.test.test_ids}",
        )