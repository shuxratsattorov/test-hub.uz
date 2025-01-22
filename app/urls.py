from django.urls import path

from app.views import view_test, add_test, add_question_with_answers, export_questions_as_json, \
    export_questions_as_excel, test_result, tests, profile_page, login_page, logout_page, rating_view, \
    delete_question_with_answers, register_page, verify_email

urlpatterns = [
    path('tests/', tests, name='tests'),
    path('test-view/<int:test_ids>/<int:question_number>/', view_test, name='view_test'),
    path('result/<int:test_id>/', test_result, name='test_result'),
    path('add-test/', add_test, name='add_test'),
    path('add-question-with-answers/<str:hash_id>/', add_question_with_answers, name='add_question_with_answers'),
    path('delete/<str:hash_id>/<int:question_id>/', delete_question_with_answers, name='delete_question_with_answers'),

    path('rating/<int:test_id>/', rating_view, name='rating'),
    path('profile/', profile_page, name='profile_page'),

    # Export ====================================================================================================
    path('export/json/<str:hash_id>/', export_questions_as_json, name='export_questions_as_json'),
    path('export/excel/<str:hash_id>/', export_questions_as_excel, name='export_questions_as_excel'),

    # Auth ======================================================================================================
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register_page, name='register'),
    path('verify/<str:verification_code>/', verify_email, name='email_verification'),
]
