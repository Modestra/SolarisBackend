from django.contrib import admin
from solaris.models import *

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id']
    pass

admin.site.register(User, UserAdmin)