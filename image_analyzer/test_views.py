import os
from PIL import Image, ImageDraw, ImageFont
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from .views import ImageAnalysisView
import json

class ImageAnalysisViewTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = ImageAnalysisView.as_view()
        self.valid_image_path = os.getcwd()+'/media/uploaded_images/valid.jpeg'
        self.valid_image_path_ovwerwritten = os.getcwd()+'/media/uploaded_images/valid_ow.png'
        self.invalid_image_path = os.getcwd()+'/media/uploaded_images/image.txt'

    def test_valid_image_analysis(self):
        # Make a POST request with the valid image
        request = self.factory.post('/analyze-image/', {'image': open(self.valid_image_path, 'rb')})
        response = self.view(request)
        
        # Assert that the response is successful and contains the expected description
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['name'], 'Food') 

    def test_invalid_image_format(self):
        # Create an invalid image file
        with open(self.valid_image_path_ovwerwritten, 'w') as file:
            file.write('This is not an image')

        # Make a POST request with the invalid image
        request = self.factory.post('/analyze-image/', {'image': open(self.invalid_image_path, 'rb')})
        response = self.view(request)
        # Assert that the response has a 400 status code and contains the expected error message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['image'][0].code, 'invalid_image')

        # Clean up the created image file
        os.remove(self.valid_image_path_ovwerwritten)
