# Cloudflare Access for Sentry

Repository for Cloudflare Access for Sentry plugin development.

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

## Plugin Development

Prepare your python environment to build the plugin:

```
pip install setuptools
pip install wheel
```

If you want to have code completion on your IDE probably is a good idea to also run:

```
pip install 'django<1.10'
```

Create a `sentry-docker/sentry.env` file with your Cloudflare Access test credentials based on the `sentry-docker/sentry.example.env`.

Prepare your Sentry on Docker environment:

```
cd sentry-docker
./install.sh
docker-compose up -d
```

To reload the plugin code:

```
./build-docker.sh
```

### Django version

Note that Sentry is based on `Django 1.9` .
