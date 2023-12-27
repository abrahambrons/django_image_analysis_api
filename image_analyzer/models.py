#Author: Abraham Bronstein https://github.com/abrahambrons/django_image_analysis_api
from django.db import models

# Create your models here.

class UploadedImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='uploaded_images/')
    description = models.TextField(null=True, blank=True)