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

        if len(users) == 0:
            logger.debug("User not found, maybe registration step...")
            return None

        if len(users) > 1:
            logger.debug("More than one user matches '%s': %s", email, len(users))
            raise MultipleUsersMatchingEmailException("Found {0} users that match the email {1}!".format(len(users), email))

        if self._enforce_standard_auth(email):
            logger.debug("Enforcing standard auth...")
            return None 

        user = users[0]
        logger.debug("Auth successful for user: %s", user.username)

        if not user.is_active:
            logger.debug("User is not active: %s", user.username)
            raise UserIsNotActiveException("User %s is not active!" % user.username)


        return user

    def user_can_authenticate(self, user):
        return True

    def _enforce_standard_auth(self, email):
        configured = settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAIN != None

        if configured:
            domain = email.split("@")[-1]
            if domain != settings.CLOUDFLARE_ACCESS_ALLOWED_DOMAIN:
                return True

        return False


class MultipleUsersMatchingEmailException(Exception):
    pass

class UserIsNotActiveException(Exception):
    pass