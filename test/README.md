# Cloudflare Access for Sentry Test Suite

Here you find an E2E test suite for the plugin.

## Running the tests

Prerequisites:

- Docker

## Docker compose services architecture:

- `cloudflare_mock_server`: Simulates Cloudflare Access behavior by generating a signed JWT and provides the certificates for Sentry to validate.
- `selenium_server`: The Selenium server that will host the browser
- `securesentry`: Nginx Proxy that to make the Cloudflare Access Mock Server and Sentry run under the same domain (allows for cookie auth)
- `selenium_test`: The actual test suite

### Securesentry - SSL Proxy

This is an SSL proxy with a self-signed certificate.

In case the certificate becomes invalid, the existing ones should be deleted and created new.

**When updated, the `proxy.crt` file should be updated on the sentry-docker docker-compose projects.**

On Sentry docker images the `proxy.crt` is used together with the environment variable `REQUESTS_CA_BUNDLE` to enable usage of a self signed certificate while executing the e2e test suite.

To setup new SSL certificates:

```
cd nginx_ssl_proxy
rm proxy.crt proxy.csr proxy.key
./gen_ssl.sh
cp proxy.crt ../sentry-docker-9x/proxy.crt
cp proxy.crt ../sentry-docker-10x/proxy.crt
```