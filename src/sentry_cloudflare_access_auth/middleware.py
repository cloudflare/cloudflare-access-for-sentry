from __future__ import absolute_import

import logging
import requests
import jwt
import json

from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from sentry.web.helpers import render_to_response

from sentry_cloudflare_access_auth.backend import MultipleUsersMatchingEmailException, UserIsNotActiveException

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

static_resources_extension = ["js", "css", "png", "jpg", "jpeg", "woff", "ttf"]

class CloudflareAccessAuthMiddleware:
    _certs_url = "https://{}/cdn-cgi/access/certs".format(settings.CLOUDFLARE_ACCESS_AUTH_DOMAIN)


    def __init__(self, get_response=None):
        self.get_response = get_response
        logger.info("CloudflareAccessAuthMiddleware initialized")
        logger.info("Certificates URL: %s", self._certs_url)

    def process_request(self, request):
        logger.debug("Handling request...")

        if self._proceed_with_token_verification(request):
            try:
                token = self._get_token_payload_from_request(request)
            except JWTValidationException as e:
                return self._render_error(request, e.message)

            if token == None:
                logger.debug("JWT token not present, bypassing auth process: %s", request.get_full_path())
                return None

            
            user_email = token[u'email']
            logger.info("Token user_email: %s", user_email)

            if self._is_already_authenticated(request, user_email):
                return None
            
            #TODO bypass auth headers
            
            if self._should_go_to_login_form(request):
                return None

            try:
                user = authenticate(email=user_email, jwt_validated=True)
            except MultipleUsersMatchingEmailException:
                return self._render_error(request, (
                    "More than one user matches the email %s" % user_email
                ))
            except UserIsNotActiveException:
                return self._render_error(request, (
                    "The user is currently disabled"
                ))
            else:
                if not user == None:
                    logger.info("Login user: %s", user.username)
                    login(request, user)

        #continue to next middleware
        return None


    def _proceed_with_token_verification(self, request):
        mandatory_settings = [settings.CLOUDFLARE_ACCESS_POLICY_AUD, settings.CLOUDFLARE_ACCESS_AUTH_DOMAIN]
        if None in mandatory_settings:
            logger.error("Middleware not configured, CLOUDFLARE_ACCESS_POLICY_AUD={0} CLOUDFLARE_ACCESS_AUTH_DOMAIN={1}".format(*mandatory_settings))
            return False
        
        extension = request.path.split(".")[-1]
        logger.debug("Testing extension: {0} (path: {1})".format(*[extension, request.get_full_path()]))
        if extension in static_resources_extension:
            logger.debug("Skipping middleware for static resources, extension: %s" % extension)
            return False

        return True

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
                logger.debug("Token payload:")
                logger.debug(t)
                return t
            except Exception as e:
                raise JWTValidationException("Unable to validate JWT: %s" % e.message)

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


    def _is_already_authenticated(self, request, user_email):
        if request.user == None:
            return False

        if request.user.username != user_email:
            return False

        return True


    def _should_go_to_login_form(self, request):
        should_go_to_login = 'goToLogin' in request.GET
        logger.debug("query string: %s" % should_go_to_login)
        return should_go_to_login


    def _render_error(self, request, message):
        context = {"message": message}
        return render_to_response("cloudflareaccess/error.html", context=context, request=request)


class JWTValidationException(Exception):
    pass