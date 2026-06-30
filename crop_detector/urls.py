from django.urls import path
from . import views

app_name = 'crop_detector'

urlpatterns = [
    path('', views.detector_home, name='home'),
    path('api/diagnose/', views.diagnose_image, name='diagnose_image'),
]
