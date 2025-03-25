from django.db import models

# Create your models here.
class MenuItem(models.Model):
    title = models.CharField()