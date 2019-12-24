from __future__ import absolute_import

import os

def setup_cloudflare_access_middleware(MIDDLEWARE_CLASSES):
    """
    Includes the Cloudflare Access Middleware right after the Authetication Middleware
    """
    updated_tuple = ()
    for middleware in MIDDLEWARE_CLASSES:
        updated_tuple = updated_tuple + (middleware,)
        if middleware.split(".")[-1] == 'AuthenticationMiddleware':
            updated_tuple = updated_tuple + ("sentry_cloudflare_access_auth.middleware.CloudflareAccessAuthMiddleware",)
    return updated_tuple

def get_cloudflare_access_os_root():
    return os.path.normpath(os.path.join(os.path.dirname(__file__), os.pardir, 'sentry_cloudflare_access_auth'))