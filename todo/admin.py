from django.contrib import admin
from todo import models

admin.site.register(models.ToDo)
admin.site.register(models.Task)
admin.site.register(models.Organization)
admin.site.register(models.Profile)
