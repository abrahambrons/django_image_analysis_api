#Author: Abraham Bronstein https://github.com/abrahambrons/django_image_analysis_api
from django.urls import path
from .views import ImageAnalysisView

urlpatterns = [
    path('analyze-image/', ImageAnalysisView.as_view(), name='analyze_image'),
]