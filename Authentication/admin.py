# admin.py
from django.contrib import admin
from .models import User, Student, Teacher, Parent

class UserAdmin(admin.ModelAdmin):
    # Display different fields depending on the user type (e.g., for school admins)
    list_display = ('username', 'email', 'user_type', 'is_staff', 'code', 'photo', 'subdomain', 'address')
    search_fields = ('username', 'email', 'user_type', 'code', 'subdomain')
    list_per_page = 25

    # If you want to filter by user type or school code
    list_filter = ('user_type', 'is_staff', 'code')

admin.site.register(User, UserAdmin)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Parent)
