from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "get_full_name",
        "course",
        "year_level",
        "email",
        "contact_number",
    )
    search_fields = ("student_id", "first_name", "last_name", "course", "email")
    list_filter = ("course", "year_level")
    ordering = ("student_id",)

