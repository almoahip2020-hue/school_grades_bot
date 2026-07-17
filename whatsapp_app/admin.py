from django.contrib import admin
from .models import Student, Grade

class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'parent_phone')
    search_fields = ('student_id', 'name', 'parent_phone')
    inlines = [GradeInline]

admin.site.register(Grade)