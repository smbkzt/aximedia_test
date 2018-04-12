from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{0!s}, {1}".format(self.id, str(self.name))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organizations = models.ManyToManyField("Organization")
    current_organization_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "{0!s}, {1}".format(self.id, self.user.username)


class ToDo(models.Model):
    name = models.CharField(max_length=100)
    organization = models.ForeignKey("Organization", default=1)

    def __str__(self):
        return "{0!s}, {1}".format(self.id, self.name)


class Task(models.Model):
    todo = models.ForeignKey("ToDo", default=1)
    task_name = models.CharField(max_length=100)
    is_done = models.BooleanField()

    def __str__(self):
        return "{0!s}, {1}".format(self.id, self.task_name)
