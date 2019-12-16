from __future__ import absolute_import

import logging


from django.http import HttpResponse

logger = logging.getLogger(__name__)

class CloudflareAccessAuthMiddleware:
    def __init__(self, get_response=None):
        self.get_response = get_response
        logger.info("CloudflareAccessAuthMiddleware INITIALIZED")
        # One-time configuration and initialization.

    def process_request(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        #print("INTERCEPTING REQUEST>>>>", request.COOKIES)
        logger.info("INTERCEPTING REQUEST>>>>")
        logger.info(request.COOKIES)
        
        #response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return HttpResponse('<h1>middleware works ;)</h1>')