from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

User = get_user_model()

class CropDetectorTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testfarmer',
            password='testpassword123'
        )
        self.home_url = reverse('crop_detector:home')
        self.diagnose_url = reverse('crop_detector:diagnose_image')

    def test_unauthenticated_access_redirects(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    def test_authenticated_home_page(self):
        self.client.login(username='testfarmer', password='testpassword123')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crop_detector/home.html')

    def test_diagnose_api_no_image(self):
        self.client.login(username='testfarmer', password='testpassword123')
        response = self.client.post(self.diagnose_url, {})
        self.assertEqual(response.status_code, 400)
        self.assertIn('No image uploaded', response.json()['error'])

    def test_diagnose_api_with_valid_image(self):
        self.client.login(username='testfarmer', password='testpassword123')
        
        # Create a small valid 224x224 RGB image in memory
        file_obj = io.BytesIO()
        img = Image.new('RGB', (224, 224), color='green')
        img.save(file_obj, 'JPEG')
        file_obj.seek(0)
        
        uploaded_image = SimpleUploadedFile(
            name='test_crop.jpg',
            content=file_obj.read(),
            content_type='image/jpeg'
        )
        
        response = self.client.post(
            self.diagnose_url,
            {'image': uploaded_image, 'crop': 'Tomato'}
        )
        if response.status_code != 200:
            print("RESPONSE ERROR:", response.content)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data['crop'], 'Tomato')
        self.assertIn('status', data)
        self.assertIn('disease', data)
        self.assertIn('confidence', data)
        self.assertIn('severity', data)
        self.assertIn('treatment', data)
        self.assertIn('fertilizer', data)
        self.assertIn('prevention', data)

