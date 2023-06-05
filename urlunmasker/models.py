from django.db import models

# Create your models here.
class UnsafeURL(models.Model):
    short_url = models.CharField(max_length=2000,blank=True, null=True)
    origianl_url = models.CharField(max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=20, blank=True, null=True)


    def __str__(self):
        return self.origianl_url
    