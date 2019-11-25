from django.db import models

# Create your models here.
class Server(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()