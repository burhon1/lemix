from django.forms import ValidationError
from typing import List
import requests

url = "api.spotlightr.com/api/"

def setUrl(request, method: str):
    return f"{request.scheme}://{url}/{method}"

def createVideo(request, vooKey:str, name: str, video_url: str=None, file=None, customS3: int=0):
    if video_url is None and file is None:
        raise ValidationError("[\"video_url\"] yoki [\"file\"] sohalardan biri kiritilishi majburiy.")
    url = setUrl(request, 'createVideo')
    payload = {
        'vooKey': vooKey,
        'name': name,
        'customS3': customS3
    }

    if video_url:
        payload['URL'] = video_url
    else:
        payload['file'] = file
    try:
        response = requests.post(url, data=payload)
        return response
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
