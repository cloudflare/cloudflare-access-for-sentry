# priv_cloudlare_access_sentry


Temporary repository for cloudflareacces Sentry plugin development.

## Install on your On-Premise Sentry instance

## Plugin Development

Prepare your Sentry on Docker environment first:

```
cd sentry-docker
./install.sh
# TODO something more is needed between...
docker-compose up -d
```

To reload the plugin code:

```
./build-docker.sh
```

