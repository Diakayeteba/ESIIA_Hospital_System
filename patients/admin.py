from django.contrib import admin

from .models import Patient, PatientDocument


class PatientDocumentInline(admin.TabularInline):
    model = PatientDocument
    extra = 0
    readonly_fields = ('uploaded_at', 'uploaded_by')


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('unique_id', 'name', 'age', 'user', 'created_by', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('unique_id', 'name')
    readonly_fields = ('unique_id', 'created_at')
    inlines = [PatientDocumentInline]


@admin.register(PatientDocument)
class PatientDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'patient', 'uploaded_at', 'uploaded_by')
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)
