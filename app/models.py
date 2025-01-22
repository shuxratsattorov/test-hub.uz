import random
from datetime import timedelta

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.db import models
from django.utils import timezone

from app.managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_test_time = models.DateTimeField(null=True, blank=True)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    verification_code_created_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []

    def generate_verification_code(self):
        return str(random.randint(100000, 999999))

    def is_code_expired(self):
        if not self.verification_code_created_at:
            return True
        expiration_time = self.verification_code_created_at + timedelta(minutes=1)
        return timezone.now() > expiration_time


class Profile(models.Model):
    first_name = models.CharField(max_length=55, null=True, blank=True)
    last_name = models.CharField(max_length=55, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')


class Category(models.Model):
    name = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.name


# class CoverCard(models.Model):
#     image = models.ImageField(upload_to='covercard/', null=True, blank=True)
#     description = models.TextField(null=True, blank=True)


class Test(models.Model):

    class TestCountChoices(models.IntegerChoices):
        FIFTEEN = 15, '15 ta'
        THIRTY = 30, '30 ta'
        SIXTY = 60, '60 ta'
        NINETY = 90, '90 ta'
        ONE_HUNDRED_TWENTY = 120, '120 ta'

    class DurationChoices(models.IntegerChoices):
        ZERO_MINUTES = 0, '0 minut'
        THIRTY_MINUTES = 30, '30 minut'
        SIXTY_MINUTES = 60, '60 minut'
        ONE_HUNDRED_TWENTY_MINUTES = 120, '120 minut'
        TWO_HUNDRED_FORTY_MINUTES = 240, '240 minut'

    test_count = models.IntegerField()
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='test/', null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, default=0)
    deadline = models.DateField(null=True, blank=True)
    test_ids = models.IntegerField(null=True, blank=True)
    test_password = models.CharField(max_length=55, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tests')

    def generate_unique_test_id(self):
        while True:
            random_id = random.randint(1000000, 9999999)
            if not Test.objects.filter(test_ids=random_id).exists():
                return random_id

    def __str__(self):

        if self.title:
            return f"{self.id} {self.title}"
        else:
            return f"Ma'lumot kiritilmagan"


class Question(models.Model):
    question = models.TextField()
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    question_number = models.IntegerField(null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    option = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.answer


class Result(models.Model):
    status = models.BooleanField(default=False)
    start_test = models.DateTimeField(auto_now_add=True)
    end_test = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)


class CorrectIncorrect(models.Model):
    correct_incorrect = models.BooleanField(null=True, blank=True)
    status = models.BooleanField(default=False)
    result = models.ForeignKey(Result, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)


class Notification(models.Model):
    notification = models.CharField(null=True, blank=True, max_length=255)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')