import urllib.parse
from datetime import timedelta

import openpyxl
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, F, Q, ExpressionWrapper, FloatField
from django.db.models.functions import Extract
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import now
from hashids import Hashids
from openpyxl.styles import Font

from app.forms import TestForm, QuestionForm, AnswerFormSet
from app.models import Test, Question, Answer, Result, Notification, Profile, CorrectIncorrect, Category

hashids = Hashids(min_length=70, salt="your_salt")


@login_required
def tests_page(request):
    test_id_query = request.GET.get('test_ids', '')
    categories = Category.objects.exclude(id=1).prefetch_related('tests')

    """ Testni ID faqat raqamlardan iborat ekanligini tekshirish mavjud datani oladi """
    if test_id_query.isdigit():
        test = Test.objects.filter(test_ids=test_id_query)
    else:
        test = Test.objects.none()

    """ User kiritgan password olish """
    test_password = request.POST.get('test_password', '')
    if test_password:
        tests_with_password = Test.objects.filter(test_password=test_password, test_ids=test_id_query)

        """ Password check qiladi """
        if tests_with_password.exists():
            test_instance = tests_with_password.first()
            return redirect('view_test', test_ids=test_instance.test_ids, question_number=1)
        else:
            messages.error(request, "Parol noto‘g‘ri!")

    """ Deadline data 01.01.2025 bo'lsa kunga formatlab beradi """
    for t in test:
        if t.deadline:
            t.days_until_deadline = (t.deadline - now().date()).days
        else:
            t.days_until_deadline = None

    context = {
        'tests': test,
        'test_id_query': test_id_query,
        'categories': categories,
    }

    return render(request, 'app/tests.html', context)


@login_required
def test_view_page(request, test_ids, question_number=1):
    profile = request.user.profile
    test = get_object_or_404(Test, test_ids=test_ids)
    questions = test.questions.all().order_by('question_number')
    category = test.category

    """ Agar foydalanuvchining ism yoki familiyasi bo'sh bo'lsa, profilni to'ldirishni talab qilamiz """
    if not profile.first_name or not profile.last_name:
        messages.error(request, "Iltimos, profilingizni to‘ldiring.")
        return redirect('profile_page')

    """ Foydalanuvchi natijasini olish yoki yaratish """
    result, created = Result.objects.get_or_create(user=request.user, test=test)

    """ Agar test kategoriyasi 1 bo'lmasa va test allaqachon bajarilgan bo'lsa, eski natijani o‘chirib, yangisini yaratamiz """
    if category.id != 1:
        if result.status:
            result.save()
            CorrectIncorrect.objects.filter(result=result).delete()
            result.delete()
            result = Result.objects.create(user=request.user, test=test)

    """ Agar foydalanuvchi testni tugatgan bo'lsa, unga xabar berib testlar sahifasiga yo‘naltiramiz """
    if result.status:
        messages.error(request, f"Siz testni allaqachon tugatkansiz")
        return redirect('tests')

    """ Agar yangi natija yaratilgan bo‘lsa, test boshlanish vaqtini belgilaymiz """
    if created:
        result.start_test = now()
        result.save()

    """ Chegaralangan vaqt None yoki 0 kelishini xatolik oldini olish """
    remaining_time = None

    """ Agar test vaqti chegaralangan bo‘lsa, qolgan vaqtni hisoblaymiz """
    if result.start_test and test.duration:
        elapsed_time = now() - result.start_test
        allowed_duration = timedelta(minutes=test.duration)
        remaining_time = max(round((allowed_duration - elapsed_time).total_seconds(), 0), 0)

        """ Agar test vaqti tugagan bo'lsa, testni tugatish """
        if elapsed_time > allowed_duration:
            result.end_test = now()
            result.status = True
            result.save()
            return redirect('test_result', test_ids)

    """ Javoblanmagan savollarni topamiz """
    unanswered_questions = questions.exclude(
        correctincorrect__result=result, correctincorrect__status=True
    ).order_by('question_number')


    """ Barcha savollar javoblangan bo‘lsa, testni yakunlab, natijalar sahifasiga yo‘naltiramiz """
    if not unanswered_questions.exists():
        result.end_test = now()
        result.status = True
        result.save()
        return redirect('test_result', test_ids)

    """ Foydalanuvchiga ko‘rsatiladigan hozirgi savolni tanlaymiz """
    current_question = unanswered_questions.filter(question_number=question_number).first()
    if not current_question:
        current_question = unanswered_questions.first()
        question_number = current_question.question_number

    """ Agar "finish_test" tugmasi bosilgan bo‘lsa, testni yakunlaymiz """
    if request.method == "POST":
        if "finish_test" in request.POST:
            result.end_test = now()
            result.status = True
            result.save()
            return redirect('test_result', test_ids)

        # User tanlagan javobni olish
        selected_answer_id = request.POST.get('answer')
        if selected_answer_id:
            # Tanlangan javobni va hozirgi savolga tegishli ekanligini tekshiradi
            selected_answer = Answer.objects.filter(id=selected_answer_id, question=current_question).first()
            if selected_answer:
                # Javobni foydalanuvchi natijalar bazasiga saqlash
                correct_result, result_created = CorrectIncorrect.objects.get_or_create(
                    result=result, question=current_question, answer=selected_answer
                )
                # Shu savolga yana qaytmasligi uchun status True qilib save qiladi
                correct_result.status = True
                correct_result.correct_incorrect = selected_answer.is_correct
                correct_result.save()

                """ Keyingi savolni o'tish, agar barcha savollar javoblangan bo‘lsa, testni yakunlaymiz """
                next_unanswered_question = unanswered_questions.exclude(
                    question_number=current_question.question_number
                ).first()

                if next_unanswered_question:
                    return redirect('view_test', test_ids=test_ids, question_number=next_unanswered_question.question_number)
                else:
                    result.end_test = now()
                    result.status = True
                    result.save()
                    return redirect('test_result', test_ids)

    """ Foydalanuvchining har bir savol bo‘yicha natijalarini saqlash uchun dictionary yaratamiz,
        test viewda javoblanganlarni tog'ri, nato'g'ri ekanligini aks etiramiz
    """
    correct_incorrect_value = {}
    for question in questions:
        correct_incorrect_instance = CorrectIncorrect.objects.filter(
            result=result, question=question).first()

        correct_incorrect_value[question.question_number] = correct_incorrect_instance

    context = {
        'test': test,
        'current_question': current_question,
        'answers': current_question.answers.all(),
        'question_number': question_number,
        'correct_incorrect': correct_incorrect_value,
        'remaining_time': remaining_time,
    }

    return render(request, 'app/view-test.html', context)


@login_required
def test_result(request, test_id):
    test = get_object_or_404(Test, test_ids=test_id)

    """ Foydalanuvchiga tegishli test bo‘yicha olingan natijalar """
    results = (
        Result.objects.filter(user=request.user, test=test)
        .annotate(
            # Testdagi umumiy savollar sonini olish
            total_questions=F('test__test_count'),

            # To‘g‘ri javoblar sonini hisoblash
            correct_answers=Count('correctincorrect', filter=Q(correctincorrect__correct_incorrect=True)),

            # To‘g‘ri javoblar foizini hisoblash
            percentage=ExpressionWrapper(
                (F('correct_answers') * 100.0) / F('total_questions'),
                output_field=FloatField()
            ),
            # Test yechishga ketgan vaqtni minutlarda hisoblash
            time_taken=ExpressionWrapper(
                Extract(F('end_test'), 'epoch') - Extract(F('start_test'), 'epoch'),
                output_field=FloatField()
            ) / 60.0
        )
        # Umumiy savollar soni 0 dan katta bo‘lgan natijalarni filtr qilish
        .filter(total_questions__gt=0)

        # user qo‘shimcha ma’lumotlarni oldindan chaqirib olish
        .select_related('user', 'user__profile')
    )

    context = {
        'results': results,
        'test': test
    }
    return render(request, 'app/result.html', context)


@login_required
def test_add_page(request):
    categories = Category.objects.all()
    user = request.user
    last_test_time = user.last_test_time

    """ User dastur qoydalariga amal qilmasa malum bir vaqtda blok qilib turamiz """
    if last_test_time:
        if timezone.now() < last_test_time + timedelta(minutes=1):
            remaining_time = (last_test_time + timedelta(minutes=1)) - timezone.now()
            seconds = remaining_time.seconds
            messages.error(request, f"Savol qo'shish bo'limiga o'tin, qayta urunish {seconds} sekund")

            """ Blok xolatda malumot qo'shmoqchi bo'lsa sessiyadagi urlga redirect qilamiz """
            redirect_url = request.session.get('last_redirect_url')
            if redirect_url:
                return redirect(redirect_url)

    """ Agar so‘rov turi POST bo‘lsa """
    if request.method == 'POST':
        test_form = TestForm(request.POST, request=request)
        if test_form.is_valid():
            test = test_form.save(commit=False)

            """ Agar foydalanuvchi superuser bo‘lsa, u kategoriyani o‘zi tanlashi mumkin """
            if user.is_superuser:
                test.category_id = request.POST.get('category')
            else:
                """ Oddiy foydalanuvchilar uchun default kategoriya """
                test.category_id = request.POST.get('category', 1)
            test.user = user
            test.save()

            """ Test ID dan hashlaymiz (bu test havolasini maxfiy qilishga yordam beradi) """
            hash_id = hashids.encode(test.id)

            """ Oxirgi test qo‘shgan vaqtni yangilaymiz """
            user.last_test_time = timezone.now()
            user.save()

            """ Redirect urlni sessiyada saqlab turamiz """
            request.session['last_redirect_url'] = f'/add-question-with-answers/{hash_id}/'

            messages.success(request, "Test muvaffaqiyatli qo'shildi.")

            return redirect('add_question_with_answers', hash_id=hash_id)
    else:
        test_form = TestForm()

    context = {
        'test_form': test_form,
        'user': user,
        'categories': categories,
    }

    return render(request, 'app/add-test.html', context)


def renumber_questions(test):
    """ question_numberni raqamlab beradigan funksiya """
    questions = Question.objects.filter(test=test).order_by('id')
    for index, question in enumerate(questions):
        question.question_number = index + 1
        question.save()


@login_required
def add_question_with_answers(request, hash_id):
    """ Hashlangan test ID olamiz """
    try:
        test_id = hashids.decode(hash_id)[0]
    except IndexError:
        return redirect('error_page')

    test = get_object_or_404(Test, id=test_id)
    question = Question.objects.filter(test=test)
    answer = Answer.objects.filter(question__in=question)

    paginator = Paginator(question, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    current_question_count = test.questions.count()

    """ Agar POST so‘rov bo‘lsa """
    if request.method == 'POST':
        """ Test count oxiriga yetkanda password ornatishni talab qilish """
        if 'test_password' in request.POST:
            test.test_password = request.POST['test_password']
            test.save()
            return redirect('tests')

        """ Savol va javoblar uchun formalarni yaratish """
        question_form = QuestionForm(request.POST, request.FILES)
        formset = AnswerFormSet(request.POST)

        """ Savol va javoblar chech qilamiz """
        if question_form.is_valid() and formset.is_valid():
            """ Test maksimal savollar soniga yetmagan bo‘lsa """
            if current_question_count < test.test_count:
                question = question_form.save(commit=False)
                question.test = test
                """ question saqlimiz """
                question.save()

                """ Variantlar ro‘yxati """
                options = ['A', 'B', 'C', 'D', 'E']

                """ Answerni vaqtincha saqlab turamiz """
                answers = formset.save(commit=False)
                """ Javoblarni varinatlab saqlab ketamiz """
                for index, answer in enumerate(answers):
                    answer.question = question
                    """ Agar variantlar 5 tadan oshib ketsa, `None` beriladi """
                    answer.option = options[index] if index < len(options) else None
                    answer.save()

                """ Agar savol qo'shish oxiriga yetkanda """
                if current_question_count + 1 == test.test_count:
                    """ Savollarni raqamlimiz """
                    renumber_questions(test)
                    """ Test ID uchun maxsus takrorlanmas ID generatsiya qilamiz """
                    test.test_ids = test.generate_unique_test_id()
                    test.save()

                    request.user.last_test_time = None
                    request.user.save()

                    """ Xabarnomaga message jonatamiz """
                    Notification.objects.create(
                        user=request.user,
                        notification=f"Testni muvaffaqiyatli qo'shdingiz! Test id:{test.test_ids}",
                    )

                hash_id = hashids.encode(test.id)
                return redirect('add_question_with_answers', hash_id=hash_id)

    else:
        question_form = QuestionForm()
        formset = AnswerFormSet()

    context = {
        'question_form': question_form,
        'formset': formset,
        'test': test,
        'current_question_count': current_question_count,
        'page_obj': page_obj,
        'answer': answer,
        'hash_id': hash_id,
        'test_ids': test.test_ids,
        'show_modal': current_question_count + 1 == test.test_count,
    }

    return render(request, 'app/add-test.html', context)


@login_required
def delete_question_with_answers(request, hash_id, question_id):
    """ Savol va unga tegishli javoblar o'chiradigon funksiya """
    try:
        test_id = hashids.decode(hash_id)[0]
    except IndexError:
        return redirect('error_page')

    test = get_object_or_404(Test, id=test_id)
    question = get_object_or_404(Question, id=question_id, test=test)

    if request.method == "POST":
        question.delete()
        messages.success(request, "Savol va unga tegishli javoblar o'chirildi.")
        return redirect('add_question_with_answers', hash_id=hash_id)

    messages.error(request, "Xato so'rov!")
    return redirect('add_question_with_answers', hash_id=hash_id)


@login_required
def test_rating_page(request):
    test_id = request.GET.get('test_id')
    test = get_object_or_404(Test, id=test_id) if test_id else None
    current_date = timezone.now().date()
    tests = Test.objects.none()
    deadline_passed_days = 0

    if test:
        deadline_passed_days = (current_date - test.deadline).days

    if 0 <= deadline_passed_days <= 1:
        user_results = Result.objects.filter(user=request.user, test__category_id=1).values_list('test', flat=True)
        tests = Test.objects.filter(id__in=user_results)

    page_obj = None

    if request.user and test:
        """ Rating deadline tugagandan keyin 1 kun davomida ko'rinadi """
        if 0 <= deadline_passed_days <= 1:
            results = (
                Result.objects.filter(test=test)
                .annotate(
                    # Testdagi umumiy savollar sonini olish
                    total_questions=F('test__test_count'),

                    # To‘g‘ri javoblar sonini hisoblash
                    correct_answers=Count('correctincorrect', filter=Q(correctincorrect__correct_incorrect=True)),

                    # To‘g‘ri javoblar foizini hisoblash
                    percentage=ExpressionWrapper(
                        (F('correct_answers') * 100.0) / F('total_questions'),
                        output_field=FloatField()
                    ),

                    # Test yechishga ketgan vaqtni minutlarda hisoblash
                    time_taken=ExpressionWrapper(
                        Extract(F('end_test'), 'epoch') - Extract(F('start_test'), 'epoch'),
                        output_field=FloatField()
                    ) / 60.0
                )
                # Umumiy savollar soni 0 dan katta bo‘lgan natijalarni filtr qilish
                .filter(total_questions__gt=0)

                # User qo‘shimcha ma’lumotlarni oldindan chaqirib olish
                .select_related('user', 'user__profile')

                # Rating tartiblash
                .order_by('-correct_answers', 'time_taken')
            )

            paginator = Paginator(results, 12)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

    context = {
        'tests': tests,
        'page_obj': page_obj,
        'selected_test': test_id
    }

    return render(request, 'app/rating.html', context)


@login_required
def profile_page(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        if 'profile_edit' in request.POST:
            if 'profile_pic' in request.FILES:
                profile.image = request.FILES['profile_pic']

            first_name = request.POST.get('first-name')
            last_name = request.POST.get('last-name')
            phone = request.POST.get('phone')

            if first_name:
                profile.first_name = first_name
            if last_name:
                profile.last_name = last_name
            if phone:
                profile.phone_number = phone

            profile.updated_at = timezone.now()
            profile.save()
            messages.success(request, "Profil ma'lumotlari muvaffaqiyatli yangilandi!")

        elif 'password_edit' in request.POST:
            old_password = request.POST.get('oldPassword')
            new_password = request.POST.get('newPassword')
            confirm_password = request.POST.get('confirmPassword')

            if not request.user.check_password(old_password):
                messages.error(request, "Eski parol noto'g'ri!")
            elif new_password != confirm_password:
                messages.error(request, "Yangi parol va tasdiqlash paroli mos emas!")
            else:
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Parol muvaffaqiyatli o'zgartirildi!")

        return redirect('profile_page')

    context = {
        'profile': profile
    }
    return render(request, 'app/profile.html', context)


def export_questions_as_json(request, hash_id):
    try:
        test_id = hashids.decode(hash_id)[0]
    except IndexError:
        return JsonResponse({"error": "Noto‘g‘ri test ID"}, status=400)

    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test).prefetch_related('answers')

    data = {
        "questions": []
    }

    for question in questions:
        question_data = {
            "question": question.question,
            "image": question.image.url if question.image else None,
            "answers": [
                {"answer": answer.answer, "is_correct": answer.is_correct}
                for answer in question.answers.all()
            ]
        }
        data["questions"].append(question_data)

    return JsonResponse(data)


def export_questions_as_excel(request, hash_id):
    """ Export JSON or EXCEL """
    try:
        test_id = hashids.decode(hash_id)[0]
    except IndexError:
        return redirect('error_page')

    test = get_object_or_404(Test, id=test_id)
    questions = Question.objects.filter(test=test).prefetch_related('answers')

    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = f"TestHub"

    header_font = Font(bold=True)
    sheet.append(["Questions", "Answers", "Is correct"])

    for cell in sheet[1]:
        cell.font = header_font

    for question in questions:
        answers = Answer.objects.filter(question=question)

        for answer in answers:
            sheet.append([
                question.question,
                answer.answer,
                "True" if answer.is_correct else "False"
            ])

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    filename = f"TestHub_{now().strftime('%Y%m%d')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    workbook.save(response)
    return response


@login_required()
def redirect_to_telegram(request):
    """ User emaili bilan telegram yunaltirish """
    user_email = request.user.email

    telegram_bot_username = "testhubsupport_bot"
    encoded_email = urllib.parse.quote(user_email)

    telegram_url = f"https://t.me/{telegram_bot_username}?start={encoded_email}"

    return redirect(telegram_url)


@login_required
def hide_instruction(request):
    """ User birinchi marta register qilganda info banner chiqazish """
    profile = Profile.objects.get(user=request.user)
    profile.show_instruction = False
    profile.save()
    return JsonResponse({"success": True})


@login_required
def custom_404_view(request, exception):
    return render(request, 'app/404.html', status=404)