from django.contrib import admin
from .models import *
# Register your models here.
from django.contrib.auth.admin import UserAdmin


admin.site.register(User)
admin.site.register(Match)

