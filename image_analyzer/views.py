import logging

# Set up logging
logging.basicConfig(filename='image_analysis.log', level=logging.INFO)

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UploadedImage
from .serializers import UploadedImageSerializer
from google.cloud import vision
import json
import os
from PIL import Image

class ImageAnalysisView(APIView):
    """
    API view for analyzing uploaded images.

    This view handles the POST request for analyzing an uploaded image. It performs the following steps:
    1. Validates the image format and size.
    2. Calls an external API to analyze the image.
    3. Updates the description field of the UploadedImage object with the analysis result.

    Methods:
    - post: Handles the POST request and performs the image analysis.
    - is_valid_image_dimensions: Checks if the image dimensions meet the minimum requirements.
    - analyze_image: Calls the external API to analyze the image.
    - is_valid_image_format: Checks if the image format is valid.
    - is_valid_image_size: Checks if the image size is within the allowed limit.
    """

    def post(self, request, *args, **kwargs):
        image_serializer = UploadedImageSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            
            # Validate image format
            if not self.is_valid_image_format(image_serializer.data['image']):
                logging.error('Invalid image format')
                return Response({'error': 'Invalid image format'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate image size
            if not self.is_valid_image_size(image_serializer.data['image']):
                logging.error('Image size exceeds 20MB')
                return Response({'error': 'Image size exceeds 20MB'}, status=status.HTTP_400_BAD_REQUEST)

            # Validate image dimensions
            if not self.is_valid_image_dimensions(image_serializer.data['image']):
                logging.error('Image dimensions must be 640x480 min')
                return Response({'error':'Image dimensions must be 640x480 min'}, status=status.HTTP_400_BAD_REQUEST)

            #calling the analyzer external API
            analysis_result = self.analyze_image(image_serializer.data['image'])
            
            if analysis_result:
                #update the description field of the UploadedImage object
                image_instance = UploadedImage.objects.get(id=image_serializer.data['id'])
                image_instance.description = analysis_result
                image_instance.save()

                return Response(json.loads(analysis_result), status=status.HTTP_200_OK)
            else:
                logging.error('Image analysis failed')
                return Response({'error': 'Image analysis failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logging.error('Invalid image')
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def is_valid_image_dimensions(self, path):
        """
        Checks if the image dimensions meet the minimum requirements.

        Args:
        - path: The path to the image file.

        Returns:
        - True if the image dimensions meet the minimum requirements, False otherwise.
        """
        image = Image.open(os.getcwd()+path)
        width, height = image.size
        return width >= 640 and height >= 480

    def analyze_image(self, path):
        """
        Calls the external API to analyze the image.

        Args:
        - path: The path to the image file.

        Returns:
        - The analysis result as a JSON object if objects are found in the image, None otherwise.
        """
        client = vision.ImageAnnotatorClient()
        #print current work directory
        with open(os.getcwd()+path, "rb") as image_file:
            content = image_file.read()
        
        image = vision.Image(content=content)
        objects = client.object_localization(image=image).localized_object_annotations

        if objects:
            # Convert objects to JSON object
            objects_json = json.dumps([{
                'name': object_.name,
                'confidence': object_.score,
            } for object_ in objects])

            return objects_json
        else:
            return None

    def is_valid_image_format(self, path):
        """
        Checks if the image format is valid.

        Args:
        - path: The path to the image file.

        Returns:
        - True if the image format is valid, False otherwise.
        """
        valid_formats = ['JPEG', 'PNG','GIF', 'BMP', 'WEBP', 'RAW', 'ICO', 'PDF', 'TIFF', 'JPG']
        try:
            image = Image.open(os.getcwd()+path)
            format = image.format
            return format.upper() in valid_formats
        except (IOError, FileNotFoundError):
            logging.error('Invalid image format')
            return False
    
    def is_valid_image_size(self, path):
        """
        Checks if the image size is within the allowed limit.

        Args:
        - path: The path to the image file.

        Returns:
        - True if the image size is within the allowed limit, False otherwise.
        """
        max_size = 20 * 1024 * 1024  # 20MB
        try:
            size = os.path.getsize(os.getcwd()+path)
            return size <= max_size
        except (IOError, FileNotFoundError):
            logging.error('Invalid image size')
            return False