from django.shortcuts import redirect
from user.models import Logger
import logging

def write_logger(get_response):
    def middleware(request):
        response = get_response(request)
        try:
            if request.user.phone:
                logger = logging.getLogger(__name__)
                print(logger.name)
                # log = Logger(title=logger.name,user=request.user)
                # log.save()
        finally:        
            return response
    return middleware
