import random

from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from django.core.files.base import ContentFile
from django.db import models

from app.managers import CustomUserManager
from .utils import compress_image


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_test_time = models.DateTimeField(null=True, blank=True)
    verification_code = models.CharField(max_length=255, blank=True, null=True)
    verification_code_created_at = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Profile(models.Model):
    show_instruction = models.BooleanField(default=False)
    first_name = models.CharField(max_length=55, null=True, blank=True)
    last_name = models.CharField(max_length=55, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    image = models.ImageField(upload_to='profile/', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    def save(self, *args, **kwargs):
        if self.image:
            compressed_image = compress_image(self.image)

            self.image.save(self.image.name, ContentFile(compressed_image.read()), save=False)

        super(Profile, self).save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.name


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

    image_card = models.ImageField(upload_to='test/', null=True, blank=True)
    description_card = models.TextField(null=True, blank=True)
    test_count = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
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


class Question(models.Model):
    question = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='questions/', null=True, blank=True)
    question_number = models.IntegerField(null=True, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')

    def save(self, *args, **kwargs):
        if self.image:
            compressed_image = compress_image(self.image)

            self.image.save(self.image.name, ContentFile(compressed_image.read()), save=False)

        super(Question, self).save(*args, **kwargs)


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    option = models.CharField(max_length=255, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')


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