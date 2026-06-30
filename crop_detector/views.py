from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
import tempfile
import os
from .ai_model import DiseaseDetectorModel

@login_required(login_url='accounts:login')
def detector_home(request):
    context = {'active_page': 'crop_detector'}
    return render(request, 'crop_detector/home.html', context)

@login_required(login_url='accounts:login')
@require_POST
def diagnose_image(request):
    if not request.FILES.get('image'):
        return JsonResponse({'error': 'No image uploaded'}, status=400)
        
    uploaded_file = request.FILES['image']
    crop_type = request.POST.get('crop', 'Tomato')
    
    try:
        fd, temp_path = tempfile.mkstemp(suffix='.jpg')
        try:
            with os.fdopen(fd, 'wb') as tmp:
                for chunk in uploaded_file.chunks():
                    tmp.write(chunk)
            
            detector = DiseaseDetectorModel()
            result = detector.predict(temp_path, crop_type)
            return JsonResponse(result)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    except Exception as e:
        return JsonResponse({'error': f'Diagnosis failed: {str(e)}'}, status=500)
