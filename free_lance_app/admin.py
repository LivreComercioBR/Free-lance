from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register your models here.

@admin.register(User)
class PersonAdmin(UserAdmin):
    list_display = ('username', 'email',)
    search_fields = ('username', 'email',)
    list_filter = ('username', )