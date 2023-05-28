from django.contrib import admin

# Register your models here.
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_filter = ('name', 'email',)


admin.site.register(User)
