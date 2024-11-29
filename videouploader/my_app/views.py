from django.shortcuts import render
from django.http import JsonResponse
from firebase_admin import storage
import os
import uuid

# Create your views here.
def upload_media(request):
    if request.method == "POST" and request.FILES.get('video1'):
        media_file = request.FILES.get('video1')
        unique_suffix = uuid.uuid4().hex 
        bucket = storage.bucket()
        blob = bucket.blob(f'media/{unique_suffix}_{media_file.name}')
        temp_file_path = f'/tmp/{media_file.name}'
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in media_file.chunks():
                temp_file.write(chunk)
        blob.upload_from_filename(temp_file_path)
        blob.make_public()
        media_url = blob.public_url
        os.remove(temp_file_path)
        return JsonResponse({"success":"successfully uploaded","video url":media_url})
    return render(request,'upload.html')

