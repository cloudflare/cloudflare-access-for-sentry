from __future__ import absolute_import

import logging
import requests
import jwt
import json

from django.conf import settings
from django.http import HttpResponse


logger = logging.getLogger(__name__)

class CloudflareAccessAuthMiddleware:
    _certs_url = "https://{}/cdn-cgi/access/certs".format(settings.CLOUDFLARE_ACCESS_AUTH_DOMAIN)


    def __init__(self, get_response=None):
        self.get_response = get_response
        logger.info("CloudflareAccessAuthMiddleware initialized")
        logger.info("Certificates URL: %s", self._certs_url)
        
        # One-time configuration and initialization.

    def process_request(self, request):
        logger.debug("Handling request...")
        logger.debug(request.COOKIES)
        
        token = self._get_token_payload_from_request(request)
        logger.debug("Token payload:")
        logger.debug(token)

        if token == None:
            #TODO where should it go? custom error page? login page?
            return HttpResponse('<h1>no token :(</h1>')
   
        user_email = token[u'email']
        logger.info("Token user_email: %s", user_email)
        #response = self.get_response(request)

        return HttpResponse('<h1>middleware works ;)</h1>')

    def _get_token_payload_from_request(self, request):
        """
        Returns:
            Token paylod (claims) or None if the decode failed or 
            no token is present.
        """
        token = ''
        if 'CF_Authorization' in request.COOKIES:
            token = request.COOKIES['CF_Authorization']
        else:
            return None
        keys = self._get_public_keys()

        for key in keys:
            try:
                t = jwt.decode(token, key=key, audience=settings.CLOUDFLARE_ACCESS_POLICY_AUD)
                return t
            except:
                pass

        return None

    def _get_public_keys(self):
        """
        Returns:
            List of RSA public keys usable by PyJWT.
        """
        r = requests.get(self._certs_url)
        public_keys = []
        jwk_set = r.json()
        for key_dict in jwk_set['keys']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key_dict))
            public_keys.append(public_key)
        return public_keys