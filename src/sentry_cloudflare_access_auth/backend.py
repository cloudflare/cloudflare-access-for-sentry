from __future__ import absolute_import

import logging

from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from sentry.utils.auth import find_users

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

class CloudflareAccessBackend(ModelBackend):
    """
    Authenticate a user by the e-mail and the flag indicating it was a valid token
    """
    def authenticate(self, email=None, jwt_validated=False):
        logger.debug("TRYING TO AUTH WITH CloudflareAccessBackend ...")

        if email == None or jwt_validated == False:
            return None

        users = find_users(email)

        logger.debug("Users found: %s", [u.username for u in users])

        if len(users) > 1:
            #TODO should give an error?
            return None 

        if self._enforce_standard_auth(email):
            logger.debug("Enforcing standard auth...")
            return None 

        logger.debug("Auth successful for user: %s", users[0].username)
        return users[0]

    def user_can_authenticate(self, user):
        return True

    def _enforce_standard_auth(self, email):
        configured = settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAIN != None

        if configured:
            domain = email.split("@")[-1]
            if domain != settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAIN:
                return True

        return False
