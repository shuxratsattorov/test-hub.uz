from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from .models import User, Profile, Category, Test, Question, Answer


class UserAdmin(BaseUserAdmin):
    # Admin panelda ko'rinadigan maydonlar
    list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined', 'last_test_time')
    list_filter = ('is_staff', 'is_active')

    # Foydalanuvchilarni qo'shish va tahrirlashda ko'rinadigan maydonlar
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_test_time', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )

    search_fields = ('email', 'username')
    ordering = ('email',)

    # Tahrir qilishda so'nggi test vaqtini yangilash
    def save_model(self, request, obj, change):
        # Agar foydalanuvchi yangilanayotgan bo'lsa, so'nggi test vaqtini yangilash
        if change:
            # So'nggi test vaqtini hozirgi vaqtga o'rnatish (admin paneldan yangilanishi uchun)
            obj.last_test_time = timezone.now()
        super().save_model(request, obj, change)


# Admin panelda User modelini ro'yxatdan o'tkazish
admin.site.register(User, UserAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Test)
admin.site.register(Question)
admin.site.register(Answer)