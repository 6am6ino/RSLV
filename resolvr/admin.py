from django.contrib import admin
from .models import CustomUser, UserProfile, Case, Arbitrator, Customer


class CustomUserAdmin(admin.ModelAdmin):
    """Admin interface for CustomUser model."""
    list_display = (
        'username', 'email', 'phone_number', 'designation', 'role')  # Ensure these fields exist in CustomUser
    search_fields = ('username', 'email')  # Add search functionality
    list_filter = ('role',)  # Filter by role


# Register the CustomUser model with its admin class
admin.site.register(CustomUser, CustomUserAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    list_display = ('user', 'email')
    search_fields = ('user__username', 'email')  # Search by username or email


# Register the UserProfile model with its admin class
admin.site.register(UserProfile, UserProfileAdmin)


class CaseAdmin(admin.ModelAdmin):
    """Admin interface for Case model."""
    list_display = ('title', 'created_by', 'status')
    search_fields = ('title', 'description')  # Add search functionality
    list_filter = ('status',)  # Filter by status


# Register the Case model with its admin class
admin.site.register(Case, CaseAdmin)


class ArbitratorAdmin(admin.ModelAdmin):
    """Admin interface for Arbitrator model."""
    list_display = ('user', 'qualifications', 'experience')
    search_fields = ('user__username', 'qualifications')  # Search by username or qualifications


# Register the Arbitrator model with its admin class
admin.site.register(Arbitrator, ArbitratorAdmin)


class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model."""
    list_display = ('user',)  # Display user associated with the customer
    search_fields = ('user__username',)  # Search by username


# Register the Customer model with its admin class
admin.site.register(Customer, CustomerAdmin)
