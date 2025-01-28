from django.urls import path

from app.views import views, auth_views

urlpatterns = [

    # Tests Page ================================================================================================
    path('', views.tests_page, name='tests'),

    # Test View =================================================================================================
    path('test-view/<int:test_ids>/<int:question_number>/', views.test_view_page, name='view_test'),
    path('result/<int:test_id>/', views.test_result, name='test_result'),

    # Test Add Page =============================================================================================
    path('test-add/', views.test_add_page, name='add_test'),
    path('add-question-with-answers/<str:hash_id>/', views.add_question_with_answers, name='add_question_with_answers'),
    path('delete/<str:hash_id>/<int:question_id>/', views.delete_question_with_answers, name='delete_question_with_answers'),

    # Test Rating Page ===========================================================================================
    path('test-rating/<int:test_id>/', views.test_rating_page, name='rating'),

    # Profile Page ===============================================================================================
    path('profile/', views.profile_page, name='profile_page'),

    # Export ====================================================================================================
    path('export/json/<str:hash_id>/', views.export_questions_as_json, name='export_questions_as_json'),
    path('export/excel/<str:hash_id>/', views.export_questions_as_excel, name='export_questions_as_excel'),

    # Auth ======================================================================================================
    path('login/', auth_views.login_page, name='login'),
    path('logout/', auth_views.logout_page, name='logout'),
    path('register/', auth_views.register_page, name='register'),
    path('verify/<str:verification_code>/', auth_views.verify_email, name='email_verification'),
]
