from django.db import models
#from django_mysql.models import ListCharField

# Create your models here.
class Server(models.Model):
    number = models.CharField(max_length=50)
    newTitle = models.CharField(max_length=100)
    # category = models.CharField(max_length=100)
    # keyword = models.TextField()
    # number = models.TextField()