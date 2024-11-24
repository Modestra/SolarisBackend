from django.contrib import admin
from solaris.models import *

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id']
    pass

class SchoolUserAdmin(admin.ModelAdmin):
    readonly_fields = ['user_id']
    pass

class TokenAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(SchoolUser, UserAdmin)
admin.site.register(Token, TokenAdmin)
