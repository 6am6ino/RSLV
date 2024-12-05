from django.contrib import admin
from .models import Case, UserProfile


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'status', 'created_at')  # Ensure 'status' is valid
    list_filter = ('status', 'created_at')  # Ensure 'status' is valid


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'get_full_name')  # Replace with a method for full name

    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"  # Assuming user is a ForeignKey

    get_full_name.short_description = 'Full Name'  # Optional: Set a short description
