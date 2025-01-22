from datetime import date, timedelta

from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import Question, Answer, Test, User, Category


class TestForm(forms.ModelForm):
    test_count = forms.IntegerField(required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    class Meta:
        model = Test
        fields = ['test_count', 'title', 'duration', 'deadline', 'category']

    def clean_all(self):

        all_fields_empty = not any(self.cleaned_data.get(field) for field in ['test_count', 'title', 'deadline'])

        if all_fields_empty:
            raise ValidationError("Maydonlar boʻsh boʻlishi mumkin emas.")

        return all_fields_empty

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError('Title: maydoni boʻsh boʻlishi mumkin emas.')
        return title

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline:
            today = date.today()
            one_week_later = today + timedelta(weeks=1)
            if not (today <= deadline <= one_week_later):
                self.add_error('deadline',
                               f"Deadline bugundan boshlab bir hafta ichida bo'lishi kerak. ({today} / {one_week_later})")


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


class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Answer
        fields = ['answer', 'is_correct']

    def clean(self):
        cleaned_data = super().clean()
        answer = cleaned_data.get('answer')
        is_correct = cleaned_data.get('is_correct')

        if not answer and is_correct is None:
            raise ValidationError("Maydonlar boʻsh boʻlishi mumkin emas.")

        if self.question and answer == self.question.question:
            raise ValidationError("Javob savol bilan bir xil boʻlmasligi kerak.")

    def clean_answer(self):
        answer = self.cleaned_data.get('answer')
        if not answer:
            raise ValidationError("Maydon boʻsh boʻlishi mumkin emas.")
        return answer

    def clean_is_correct(self):
        is_correct = self.cleaned_data.get('is_correct')
        if is_correct is None:
            raise ValidationError("Maydon boʻsh boʻlishi mumkin emas.")
        return is_correct


AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=5)


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=255)

    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(email=email)
            if not user.check_password(password):
                raise forms.ValidationError('password error')
        except User.DoesNotExist:
            raise forms.ValidationError('email topilmadi.')
        return password


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=55)
    confirm_password = forms.CharField(max_length=55)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email already exists')
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('password error')
        return password
