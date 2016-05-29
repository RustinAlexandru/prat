from django.contrib import admin

from prat import models


class UserGroupMembershipInline(admin.TabularInline):
    model = models.UserGroupMembership
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (UserGroupMembershipInline,)


class UserGroupAdmin(admin.ModelAdmin):
    inlines = (UserGroupMembershipInline,)

admin.site.register(models.Task)
admin.site.register(models.UserProfile)
admin.site.register(models.PredefinedTask)
# admin.site.register(models.UserGroup)
admin.site.register(models.UserGroupComment)
admin.site.register(models.Theme)
admin.site.register(models.UserThemes)
admin.site.register(models.Achievement)
admin.site.register(models.Category)
admin.site.register(models.UserTaskActivity)
admin.site.register(models.UserGroupMembership)
admin.site.register(models.UserGroup, UserGroupAdmin)
admin.site.register(models.Ong)
