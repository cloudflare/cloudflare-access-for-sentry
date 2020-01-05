from __future__ import absolute_import

import os

def setup_cloudflare_access_for_sentry_10x(MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATES):
    MIDDLEWARE_CLASSES = setup_cloudflare_access_middleware(MIDDLEWARE_CLASSES)
    
    AUTHENTICATION_BACKENDS = (
        'sentry_cloudflare_access_auth.backend.CloudflareAccessBackend',
    ) + AUTHENTICATION_BACKENDS

    TEMPLATES[0]['DIRS'] += [os.path.join(get_cloudflare_access_os_root(), "templates")]

    return MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATES
    

def setup_cloudflare_access_for_sentry_9x(MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATE_DIRS):
    MIDDLEWARE_CLASSES = setup_cloudflare_access_middleware(MIDDLEWARE_CLASSES)
    
    AUTHENTICATION_BACKENDS = (
        'sentry_cloudflare_access_auth.backend.CloudflareAccessBackend',
    ) + AUTHENTICATION_BACKENDS

    TEMPLATE_DIRS += (os.path.join(get_cloudflare_access_os_root(), "templates"),)

    return MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATE_DIRS



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