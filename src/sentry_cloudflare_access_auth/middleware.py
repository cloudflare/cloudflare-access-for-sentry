from __future__ import absolute_import

import logging
import requests
import jwt
import json

from django.core.exceptions import ValidationError
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from sentry.web.helpers import render_to_response

from sentry_cloudflare_access_auth.backend import MultipleUsersMatchingEmailException, UserIsNotActiveException

logger = logging.getLogger(__name__)

static_resources_extension = ["js", "css", "png", "jpg", "jpeg", "woff", "ttf"]

cf_sentry_logout_cookie_name = "cf_sentry_logout"

class CloudflareAccessAuthMiddleware:
    _certs_url = "https://{}/cdn-cgi/access/certs".format(settings.CLOUDFLARE_ACCESS_AUTH_DOMAIN)


    def __init__(self, get_response=None):
        self.get_response = get_response
        logger.info("CloudflareAccessAuthMiddleware initialized")
        logger.info("Certificates URL: %s", self._certs_url)


    def process_request(self, request):
        logger.debug("Handling request...")

        if self._should_redirect_to_logout(request):
            return self._redirect_to_logout(request)


        if self._proceed_with_token_verification(request):
            try:
                token = self._get_token_payload_from_request(request)
            except JWTValidationException as e:
                return self._render_error(request, e.message)

            if token == None:
                logger.debug("JWT token not present, bypassing auth process: %s", request.get_full_path())
                return None

            if u'common_name' in token and token[u'common_name']:
                logger.debug("JWT token contains common_name, bypassing auth process for service token: %s", request.get_full_path())
                return None
            
            user_email = "" if not u'email' in token else token[u'email']
            logger.info("Token user_email: %s", user_email)

            
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


    def process_response(self, request, response):
        logger.debug("response: %s - %s", request.method, request.path)
        if request.path == "/api/0/auth/" and request.method == 'DELETE':
            response.set_cookie(cf_sentry_logout_cookie_name, "1")
        return response


    def _should_redirect_to_logout(self, request):
        return cf_sentry_logout_cookie_name in request.COOKIES and request.COOKIES[cf_sentry_logout_cookie_name] == "1"


    def _redirect_to_logout(self, request):
        logout_absolute_url = request.build_absolute_uri("/cdn-cgi/access/logout").replace("http://", "https://")
        logger.info("redirecting to: %s" % logout_absolute_url)
        redirect_response = redirect(logout_absolute_url)
        redirect_response.delete_cookie(cf_sentry_logout_cookie_name)
        return redirect_response

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

        if self._should_go_to_login_form(request):
            return False

        if self._is_already_authenticated(request):
            return False

        return True


    def _get_token_payload_from_request(self, request):
        """
        Returns:
            Token paylod (claims) or None if no token is present.
            In case of invalid JWT a exception is raised.
        """
        token = ''
        if 'CF_Authorization' in request.COOKIES:
            token = request.COOKIES['CF_Authorization']
        else:
            return None
        keys = self._get_public_keys()

        error_messages = set()
        for key in keys:
            try:
                t = jwt.decode(token, key=key, audience=settings.CLOUDFLARE_ACCESS_POLICY_AUD)
                logger.debug("Token payload:")
                logger.debug(t)
                return t
            except Exception as e:
                logger.debug("Unable to validate JWT: %s" % e.message)
                error_messages.add(e.message)
                pass

        raise JWTValidationException("Unable to validate JWT: %s" % ", ".join(error_messages))


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


    def _is_already_authenticated(self, request):
        if request.user == None:
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