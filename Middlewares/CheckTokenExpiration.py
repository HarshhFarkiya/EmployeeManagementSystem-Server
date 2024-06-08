import jwt
from datetime import datetime

def is_token_expired(token):
    try:
        payload = jwt.decode(token, verify=False)  # Decode the token without verification
        expiration_time = payload['exp']
        current_time = datetime.utcnow().timestamp()
        return current_time > expiration_time
    except jwt.ExpiredSignatureError:
        return True  # Token has expired
    except jwt.InvalidTokenError:
        return True  # Invalid token

