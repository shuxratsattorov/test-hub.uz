import random
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.html import strip_tags
from hashids import Hashids

from app.forms import LoginForm
from app.forms import RegisterForm
from app.models import User

hashids = Hashids(min_length=70, salt="your_salt")


def login_page(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('tests')
            else:
                messages.add_message(
                    request,
                    level=messages.WARNING,
                    message='User not found'
                )

    return render(request, 'app/login.html', {'form': form})


def logout_page(request):
    if request.method == 'GET':
        logout(request)
        return redirect(reverse('login'))


def generate_verification_code():
    return random.randint(100000, 999999)


def generate_new_verification_code(user):
    verification_code = hashids.encode(generate_verification_code())
    user.verification_code = verification_code
    user.verification_code_created_at = timezone.now()
    user.save()

    decoded_code = hashids.decode(verification_code)[0]

    subject = 'Email manzilingizni tasdiqlang'
    html_message = render_to_string('app/email_verification.html', {'verification_code': decoded_code})
    plain_message = strip_tags(html_message)
    from_email = 'test-hub.uz <no-reply@example.com>'
    recipient_list = [user.email]

    send_mail(
        subject,
        plain_message,
        from_email,
        recipient_list,
        html_message=html_message,
        fail_silently=False,
    )


User = get_user_model()


def register_page(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = User.objects.create_user(email=email, password=password)
            user.is_active = False
            user.save()

            generate_new_verification_code(user)

            messages.info(request, 'Tasdiqlash kodi email manzilingizga yuborildi.')

            total_users = User.objects.count()
            subject = "Yangi foydalanuvchi ro'yxatdan o'tdi"
            message = f"User: {email}\nJami foydalanuvchilar soni: {total_users}"
            from_email = 'shuhratsattorov2004@gmail.com'
            recipient_list = ['shuhratsattorov2004@gmail.com']

            send_mail(
                subject,
                message,
                from_email,
                recipient_list
            )

            return redirect('email_verification', verification_code=user.verification_code)

    return render(request, 'app/register.html', {'form': form})


def verify_email(request, verification_code):
    try:
        profile = User.objects.get(verification_code=verification_code)
    except User.DoesNotExist:
        raise Http404("Tasdiqlash kodi noto'g'ri yoki muddati o'tgan.")

    if profile.verification_code_created_at:
        expiration_time = profile.verification_code_created_at + timedelta(minutes=1.5)
        code_expired = timezone.now() > expiration_time
        remaining_time = max(round((expiration_time - timezone.now()).total_seconds(), 0), 0)
    else:
        code_expired = True

    if request.method == 'POST':
        if 'resend_code' in request.POST:
            generate_new_verification_code(profile)
            messages.success(request, 'Yangi tasdiqlash kodi email manzilingizga yuborildi.')
            return redirect('email_verification', verification_code=profile.verification_code)

        elif 'verification_code' in request.POST:
            entered_code = request.POST.get('verification_code')

            decoded_code = hashids.decode(profile.verification_code)[0]

            if entered_code == str(decoded_code) and not code_expired:
                user = profile
                user.is_active = True
                user.verification_code = None
                user.save()
                return redirect('login')
            elif code_expired:
                messages.error(request, 'Tasdiqlash kodi muddati tugagan. Iltimos, yangi kod so‘rang.')
            else:
                messages.error(request, 'Tasdiqlash kodi noto‘g‘ri.')

    context = {
        'verification_code': verification_code,
        'code_expired': code_expired,
        'remaining_time': remaining_time
    }

    return render(request, 'app/verification_code.html', context)