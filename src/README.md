# Cloudflare Access for Sentry

Cloudflare Access for Sentry plugin to enable seamless authentication through Cloudflare Access JWT .

## Install on your On-Premise Sentry instance

To enable this plugin on your On-Premise installation of Sentry add the following to your `sentry.conf.py`:

```
####################################################
# Cloudflare Access Plugin Setup and Configuration #
####################################################
MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATES = setup_cloudflare_access_for_sentry(MIDDLEWARE_CLASSES, AUTHENTICATION_BACKENDS, TEMPLATES)

# Set the environment variables on your system or replace the values below.
# CF_POLICY_AUD: Your Cloudflare Access Policy Audience
# CF_AUTH_DOMAIN: Your Cloudflare Access authentication domain
CLOUDFLARE_ACCESS_POLICY_AUD = os.getenv("CF_POLICY_AUD")
CLOUDFLARE_ACCESS_AUTH_DOMAIN = os.getenv("CF_AUTH_DOMAIN")

# Emails that match this domain will authorize with their Access JWT. 
# All other emails will be required authorize again with their Sentry credentials.
# Leave it as a comment or set to None if all domains should be authorized only with the JWT.
#CLOUDFLARE_ACCESS_ALLOWED_DOMAIN = None