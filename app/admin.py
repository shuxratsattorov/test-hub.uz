from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Profile, Category, Test, Question, Answer, Result, CorrectIncorrect


class UserAdmin(BaseUserAdmin):
    list_display = ('id', 'email', 'is_staff', 'is_active', 'is_superuser', 'verification_code', 'last_test_time')
    list_filter = ('is_staff', 'is_active', 'is_superuser')

    search_fields = ('email',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('verification_code', 'last_test_time')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    readonly_fields = ('date_joined',)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone_number', 'image', 'updated_at')
    search_fields = ('user__email',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'test_count', 'duration', 'deadline', 'test_ids', 'test_password', 'created_at', 'category')
    search_fields = ('test_ids', 'category__name')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'question_number', 'image')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'option', 'is_correct')


class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test__test_ids', 'status', 'test__duration', 'test__deadline', 'start_test', 'end_test')
    search_fields = ('user__email', 'test__test_ids')


class CorrectIncorrectAdmin(admin.ModelAdmin):
    list_display = ('id', 'result__user__email', 'question__test__test_ids', 'correct_incorrect', 'status')


admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(CorrectIncorrect, CorrectIncorrectAdmin)
# admin.site.unregister()