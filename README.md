# priv_cloudlare_access_sentry

Temporary repository for cloudflareacces Sentry plugin development.

## Install on your On-Premise Sentry instance

TODO: document setup for users

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

### Django

Note that Sentry is based on `Django 1.9` .
