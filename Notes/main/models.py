from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField(null=True, blank=True)
    last_edited = models.DateTimeField(auto_now=True, null=True, blank=True)
