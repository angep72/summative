# admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')  # Adjust fields as needed
    search_fields = ('username', 'email')  # Optional: Make searching easier in the admin panel

admin.site.register(User, UserAdmin)
