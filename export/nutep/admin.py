from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from nutep.models import (BaseError, UserProfile, Team, CompanyManager,
    Employee)

admin.site.unregister(User)


class ManagerInline(admin.TabularInline):
    model = CompanyManager  # @UndefinedVariable
    extra = 1


class UserProfileInline(admin.StackedInline):
    model = UserProfile  
    
    
class TeamInline(admin.TabularInline):
    model = Team.users.through  # @UndefinedVariable
    extra = 1


class UserProfileAdmin(UserAdmin):    
    inlines = [UserProfileInline, TeamInline, ManagerInline]


class TeamAdmin(admin.ModelAdmin):  
    pass


class EmployeeAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserProfileAdmin)
admin.site.register(BaseError)
admin.site.register(Team, TeamAdmin)
admin.site.register(Employee, EmployeeAdmin)
