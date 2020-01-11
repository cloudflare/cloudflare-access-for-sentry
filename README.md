# Cloudflare Access for Sentry

Repository for Cloudflare Access for Sentry plugin development.

## Install on your On-Premise Sentry instance

To enable this plugin on your On-Premise installation of Sentry you need to install via `pip` and update your `sentry.conf.py`

The Access *Audience* and *Auth Domain* may be set in your OS environment or directly in Sentry conf file.

### Install with `pip`

While the repository is **private** run with your Github SSH keys set:

```
pip install "git+ssh://git@github.com/cloudflare/cloudflare-access-for-sentry.git@master#egg=sentry_cloudflare_access_auth&subdirectory=src"
```

When it become public can change to:

```
pip install "git+https://github.com/cloudflare/cloudflare-access-for-sentry@master#egg=sentry_cloudflare_access_auth&subdirectory=src"
```

And restart your Sentry after updating the configuration.

### Configuration For Sentry 9.x

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

### Configuration For Sentry 10.x

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

Create a `sentry-docker-9x/.env` and `sentry-docker-10x/sentry.env` files with your Cloudflare Access test credentials like:

```
CF_POLICY_AUD="YOUR POLICY AUDIENCE VALUE"
CF_AUTH_DOMAIN="YOUR ACCESS LOGIN PAGE DOMAIN"
```

Prepare your Sentry on Docker environment:

```
#Or replace 9x with 10x
cd sentry-docker-9x
./install.sh
docker-compose up -d
```

To reload the plugin code:

```
#Or replace 9x with 10x
./build-docker-9x.sh
```

### Django version

Sentry 9.x is based on `Django 1.7` .

Sentry 10.x is based on `Django 1.9` .
