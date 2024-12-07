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

class TeacherAdmin(admin.ModelAdmin):
    readonly_fields = ['teacher_id']
    pass

class PupilAdmin(admin.ModelAdmin):
    readonly_fields = ['shop_id']
    pass

class CompetitionAdmin(admin.ModelAdmin):
    readonly_fields = ['competition_id']
    pass

admin.site.register(User, UserAdmin)
admin.site.register(SchoolUser, UserAdmin)
admin.site.register(Token, TokenAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Pupil, PupilAdmin)
admin.site.register(Competition, CompetitionAdmin)

