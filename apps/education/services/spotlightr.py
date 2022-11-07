from django.forms import ValidationError
from django.conf import settings
from typing import List
import requests
vooKey = settings.SPOTLIGHTR_vooKEY
url = "api.spotlightr.com/api/"

def setUrl(request, method: str):
    return f"{request.scheme}://{url}/{method}"

def createVideo(request, vooKey:str, name: str, video_url: str=None, file=None, customS3: int=0):
    if video_url is None and file is None:
        raise ValidationError("[\"video_url\"] yoki [\"file\"] sohalardan biri kiritilishi majburiy.")
    url = setUrl(request, 'createVideo')
    
    params = {
        'vooKey': vooKey,
        'hls': 1,
        'create': 1,
        'name': name,
    }
    if video_url:
        params['URL'] = video_url
    else:
        params['file'] = file
    params['name'] = name
    
    try:
        response = requests.post(url, params=params)
        return response.status_code
    except Exception as e:
        raise e

    
def deleteVideo(request, vooKey:str, IDs:List[int]):
    url = setUrl(request, 'deleteVideo')
    payload = {
        'vooKey': vooKey,
        'IDs': IDs
    }
    try:
        response = requests.post(url, data=payload)
        return response
    except Exception as e:
        raise e
