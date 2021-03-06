import json
import base64
import requests
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'coffeeshopprojectudacity.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffeeshop'

## AuthError AuthError
'''
AuthError AuthError
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
@TODO implement get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''
def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)
    
    jwt = request.headers.get('Authorization')
    jwtParts = jwt.split(" ")

    if len(jwtParts) != 2:
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)
    elif jwtParts[0].lower() != 'bearer':
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)

    token = jwtParts[1]
    return token

'''
@TODO implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    # raise AuthError('Not Implemented')
    if permission =='':
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)
    error = True
    for Permission in payload['permissions']:
        if Permission == permission:
            error =False
    if error ==True :
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)
    return True

'''
@TODO implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    # raise AuthError('Not Implemented')

    tokenParts = token.split(".")
    if len(tokenParts) !=3:
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)
    Header = json.loads(base64.b64decode(tokenParts[0]))
    if "kid" not in Header:
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)
    kid = requests.get('https://coffeeshopprojectudacity.us.auth0.com/.well-known/jwks.json?_ga=2.19285688.1448347622.1616603528-1677198890.1615769745').json()['keys'][0]['kid']
    if Header["kid"] != kid:
        raise AuthError({"code": "authorization_header_missing","description":"Authorization header is expected"}, 401)
    payloadEncoded = str(tokenParts[1])
    if len(payloadEncoded) != 0:
        i = 3- (len(payloadEncoded) % 3)
        for x in range(i):
            payloadEncoded = payloadEncoded + '='
    payload = json.loads(base64.b64decode(payloadEncoded))
    
    return payload

'''
@TODO implement @requires_auth(permission) decorator method
    @INPUTS
        permission: string permission (i.e. 'post:drink')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f( *args, **kwargs)

        return wrapper
    return requires_auth_decorator