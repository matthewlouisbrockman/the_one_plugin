# requires that the header has an auth0 access token
import json
import os
from jose import jwt
from flask import request, g, jsonify
from functools import wraps
from urllib.request import urlopen
from config import IS_LOCALHOST
from models.subscriptions import TOPSubscription

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "theoneplugin.us.auth0.com")
ALGORITHMS = os.getenv("ALGORITHMS", ["RS256"])
API_AUDIENCE = os.getenv("API_AUDIENCE", "https://api.theoneplugin.net")
DEFAULT_USERNAME = os.getenv("DEFAULT_USERNAME", "test_account")

# AuthError Exception
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
    
    def __str__(self):
        return json.dumps(self.error)

def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description":
                         "Authorization header is expected"}, 401)
    
    parts = auth.split()
    
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must start with"
                         " Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description":
                         "Authorization header must be"
                         " Bearer token"}, 401)
    
    token = parts[1]
    return token

def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if "kid" not in unverified_header:
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization malformed."}, 401)
    
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }
    
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )
            
            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "token_expired",
                             "description": "Token expired."}, 401)
        
        except jwt.JWTClaimsError:
            raise AuthError({"code": "invalid_claims",
                             "description":
                             "Incorrect claims,"
                             "please check the audience and issuer."}, 401)
        except Exception:
            raise AuthError({"code": "invalid_header",
                             "description":
                             "Unable to parse authentication"
                             " token."}, 400)
    
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find appropriate key"}, 400)



def auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):

        try:
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            g.user_id = payload["sub"]
        except AuthError as e:
            if IS_LOCALHOST:
                g.user_id = DEFAULT_USERNAME
            else:
                return {
                    "success": False,
                    "message": "Authentication failed, please logout and login again. If using chatgpt, you may need to uninstall and reinstall the plugin"
                }, 401

        # Call the actual function
        try:
            response = f(*args, **kwargs)

        except Exception as e:
            response = jsonify({"message": str(e)}), 500

        return response
    
    return wrapper

# wrapper to add the subscription status to g
def rate_limited(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Call the actual function
        try:
            # check if user has sub
            subscription = TOPSubscription.find_by_user_id(g.user_id)
            if subscription:
                g.subscription = subscription
            else:
                g.subscription = None
            response = f(*args, **kwargs)

        except Exception as e:
            response = jsonify({"message": str(e)}), 500

        return response
    
    return wrapper


