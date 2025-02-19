from datetime import timedelta

from django.utils.timezone import now

from app.models import Profile, Notification


def context_manager(request):
    context = {}

    if request.user.is_authenticated:
        user = request.user

        try:
            profile = Profile.objects.filter(user=user).first()
        except Profile.DoesNotExist:
            profile = None

        # 24 soat ichidagi xabarlarni olish
        bir_kun_oldin = now() - timedelta(days=1)
        notifications = Notification.objects.filter(user=user, created_at__gte=bir_kun_oldin).order_by('-created_at')

        # O'qilmagan xabarlar sonini hisoblash
        unread_count = notifications.filter(status=False).count()

        # Xabarlarni o'qilgan deb belgilash
        notifications.filter(status=False).update(status=True)

        context['profile'] = profile
        context['notifications'] = notifications
        context['unread_count'] = unread_count  # O'qilmagan xabarlar soni

    return context