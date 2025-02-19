from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import Question, Answer, Test, User, Category


class TestForm(forms.ModelForm):
    test_count = forms.IntegerField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Test
        fields = ['test_count', 'title', 'duration', 'deadline', 'category']

    def clean(self):
        cleaned_data = super().clean()
        title = self.cleaned_data.get('title')
        deadline = self.cleaned_data.get('deadline')

        user = self.request.user if self.request else None

        if not title and not deadline:
            self.add_error("title", "")
            return cleaned_data

        if not title:
            self.add_error("title", "Maydon boʻsh boʻlishi mumkin emas.")
            return cleaned_data

        if user and user.is_superuser:
            return cleaned_data

        if not deadline:
            self.add_error("deadline", "Maydon boʻsh boʻlishi mumkin emas.")
        elif deadline:
            today = date.today()
            one_week_later = today + timedelta(weeks=1)
            if not (today <= deadline <= one_week_later):
                self.add_error("deadline", f"Diapazon: ({today} / {one_week_later})")
        return cleaned_data


def validate_image_size(image):
    max_size = 10 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Rasmning o'lchami 10 MB dan oshmasligi kerak.")


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question', 'image']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            validate_image_size(image)
        return image

    def clean_question(self):
        question = self.cleaned_data.get('question')
        if not question:
            raise ValidationError("Maydon boʻsh boʻlishi mumkin emas.")
        return question


class Profile(forms.ModelForm):
    first_name = forms.CharField(max_length=55, required=False)
    last_name = forms.CharField(max_length=55, required=False)

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get("email")
        last_name = cleaned_data.get("password")

        if not first_name and not last_name:
            self.add_error("first_name", "")
        elif not first_name:
            self.add_error("first_name", "Ism kiritilishi shart!")
        elif not last_name:
            self.add_error("last_name", "Familiya kiritilishi shart!")

        return cleaned_data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']

    def clean(self):
        cleaned_data = super().clean()
        answer = cleaned_data.get('answer')
        is_correct = cleaned_data.get('is_correct')

        if not answer:
            raise ValidationError({'answer': 'Maydon boʻsh boʻlishi mumkin emas.'})

        if is_correct is None:
            raise ValidationError({'is_correct': 'Maydon boʻsh boʻlishi mumkin emas.'})

        return cleaned_data


AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=5)


class LoginForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=55, required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")

        if not email and not password:
            self.add_error("email", "")
        elif not email:
            self.add_error("email", "Email kiritilishi shart!")
        elif not password:
            self.add_error("password", "Parol kiritilishi shart!")

        if email and password:
            try:
                user = User.objects.get(email=email)
                if not user.check_password(password):
                    self.add_error("password", "Parol noto‘g‘ri.")
            except User.DoesNotExist:
                self.add_error("email", "Bunday email topilmadi.")

        return cleaned_data


class RegisterForm(forms.Form):
    email = forms.EmailField(required=False)
    password = forms.CharField(max_length=55, required=False)
    confirm_password = forms.CharField(max_length=55, required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if not email and not password and not confirm_password:
            self.add_error("email", "")
            return cleaned_data

        if not email:
            self.add_error("email", "Email kiritilishi shart!")
            return cleaned_data
        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email allaqachon mavjud.")
            return cleaned_data

        if not password:
            self.add_error("password", "Parol kiritilishi shart!")
            return cleaned_data
        if len(password) < 8:
            self.add_error("password", "Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
            return cleaned_data

        if not confirm_password:
            self.add_error("confirm_password", "Parol tasdiqlash kiritilishi shart!")
            return cleaned_data
        if password != confirm_password:
            self.add_error("confirm_password", "Parol mos kelmadi.")

        return cleaned_data
