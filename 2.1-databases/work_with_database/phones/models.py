from django.db import models
from django.forms import ImageField


class Phone(models.Model):
     id = models.IntegerField(primary_key=True)
     name = models.CharField(max_length=50)
     image = models.URLField()
     price = models.IntegerField()
     release_date = models.DateField()
     lte_exists = models.BooleanField()
     slug = models.SlugField(unique=True)




