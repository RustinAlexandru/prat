from django.contrib import admin
from prat import models

admin.site.register(models.Task)
admin.site.register(models.UserProfile)
admin.site.register(models.PredefinedTask)
admin.site.register(models.UserGroup)
admin.site.register(models.UserTaskEvidence)
admin.site.register(models.UserGroupComment)
admin.site.register(models.Theme)
admin.site.register(models.UserThemes)
admin.site.register(models.Achievement)
admin.site.register(models.Category)
admin.site.register(models.UserTaskActivity)
