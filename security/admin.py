from django.contrib import admin

from .models import LoginOTP


@admin.register(LoginOTP)
class LoginOTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_valid')
    list_filter = ('is_valid', 'created_at')
    readonly_fields = ('created_at',)
