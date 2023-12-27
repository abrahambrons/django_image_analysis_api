#Author: Abraham Bronstein https://github.com/abrahambrons/django_image_analysis_api
from rest_framework import serializers
from .models import UploadedImage

class UploadedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedImage
        fields = ['id', 'image', 'description']