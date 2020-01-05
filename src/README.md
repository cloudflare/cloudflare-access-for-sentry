# Cloudflare Access for Sentry

Cloudflare Access for Sentry plugin to enable seamless authentication through Cloudflare Access JWT .

## Install on your On-Premise Sentry instance

To enable this plugin on your On-Premise installation of Sentry add the following to your `sentry.conf.py`:

### For Sentry 9.x

```
####################################################
# Cloudflare Access Plugin Setup and Configuration #
####################################################
from sentry_cloudflare_access_auth.helper import setup_cloudflare_access_for_sentry_9x
MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATE_DIRS = setup_cloudflare_access_for_sentry_9x(MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATE_DIRS)

CLOUDFLARE_ACCESS_POLICY_AUD = os.getenv("CF_POLICY_AUD")
CLOUDFLARE_ACCESS_AUTH_DOMAIN = os.getenv("CF_AUTH_DOMAIN")

# Emails that match this domain will authorize with their Access JWT. 
# All other emails will be required authorize again with their Sentry credentials.
#CLOUDFLARE_ACCESS_ALLOWED_DOMAIN = None
```

### For Sentry 10.x

```
####################################################
# Cloudflare Access Plugin Setup and Configuration #
####################################################
from sentry_cloudflare_access_auth.helper import setup_cloudflare_access_for_sentry_10x
MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATES = setup_cloudflare_access_for_sentry_10x(MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATES)

CLOUDFLARE_ACCESS_POLICY_AUD = os.getenv("CF_POLICY_AUD")
CLOUDFLARE_ACCESS_AUTH_DOMAIN = os.getenv("CF_AUTH_DOMAIN")

# Emails that match this domain will authorize with their Access JWT. 
# All other emails will be required authorize again with their Sentry credentials.
#CLOUDFLARE_ACCESS_ALLOWED_DOMAIN = None
```