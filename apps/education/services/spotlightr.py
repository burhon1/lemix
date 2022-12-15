from django.forms import ValidationError
from django.conf import settings
from typing import List
import requests
vooKey = 'tJWzkNmqWSBksMlsup9jQXiHP'
url = "api.spotlightr.com/api"

def setUrl(scheme, method: str):
    return f"{scheme}://{url}/{method}?create=1"

def createVideo(scheme, name: str, video_url: str, vooKey:str=vooKey, file=None, customS3: int=0):
    if video_url is None: # and file is None:
        raise ValidationError("[\"video_url\"] soha kiritilishi majburiy.") # yoki [\"file\"] sohalardan biri
    url = setUrl(scheme, 'createVideo')
    print("URL: ", url)
    params = {
        'vooKey': vooKey,
        'hls': 1,
        'create': 1,
        'name': name,
        'formatURL': True
    }
    if video_url:
        params['URL'] = video_url
    # else:
    #     params['file'] = file
    params['name'] = name

    headers = {
        'Content-Type': 'application/json',
        # 'Content-Length': '25',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'User-Agent': 'PostmanRuntime/7.29.2',
    }
    print("PARAMS: ", params)
    try:
        response = requests.post(url, params=params, headers=headers)
        if response.status_code not in [200, 302]:
            raise ValidationError("Bajarilmadi.")
        return response.text+'?fallback=true'
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
