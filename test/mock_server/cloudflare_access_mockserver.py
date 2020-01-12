import os
import json
import random
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime

from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class CloudflareAccessCertificates(Resource):
    """
    Mock endpoint to return the signing certificates 
    """
    def get(self):
        response = {'keys':[self._get_cert_as_json(1), self._get_cert_as_json(2)]}
        print(response)
        return response

    def _get_cert_as_json(self, index):
        with open('cert_0%d.key' % index, 'rb') as fh:
            jwk_obj = jwk.JWK.from_pem(fh.read())
            jwk_json = jwk_obj.export_public()
            return json.loads(jwk_json)


class Authenticate(Resource):
    """
    Signs a JWT with one of the certificates and sets the auth cookie.
    """

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        args = parser.parse_args()
        payload = self._create_payload(args['email'])
        return {'success': True}, 200, {'Set-Cookie': 'CF_Authorization=%s;path=/' % self._sign_payload(payload)}

    def _sign_payload(self, payload):
        rand_cert = random.randint(1,2)
        with open('cert_0%d.key' % rand_cert, 'rb') as fh:
            signing_key = jwk.JWK.from_pem(fh.read())
            token = jwt.generate_jwt(payload, signing_key, 'RS256', datetime.timedelta(minutes=60))
            return token
        

    def _create_payload(self, email):
        return {
            "aud": [
                "f73c7a6712258428dd625be8da1f6660b74d9a10d8877f579f8429490baa3a64"
            ],
            "email": email,
            "iss": "securesentry",
        }

class Logout(Resource):
    def get(self):
        return "Logout succesful"

api.add_resource(CloudflareAccessCertificates, '/cdn-cgi/access/certs')
api.add_resource(Authenticate, '/cdn-cgi/access/auth')
api.add_resource(Logout, '/cdn-cgi/access/logout')


if __name__ == '__main__':
    app.run(ssl_context='adhoc', debug=True, host='0.0.0.0')