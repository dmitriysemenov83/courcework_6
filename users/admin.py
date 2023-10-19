from django.contrib import admin

from users.models import User


@admin.register(User)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'phone', 'country', 'avatar')