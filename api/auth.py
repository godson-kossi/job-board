
import jwt, datetime

from django.conf import settings

from . import models



def generate_token(user: models.User) -> str:
    """Generate a new token for a user"""

    payload = {
        'user_id': user.id,
        'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=1),
        'iat': datetime.datetime.now(datetime.UTC),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def validate_token(cookies: dict) -> models.User:
    """
    Validate a token and return the corresponding user
    Raise PermissionError if the token is invalid
    Raise KeyError if the user does not exist
    """

    token = cookies.get('jwt_token')

    if not token: raise ValueError

    try: body = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError): raise PermissionError

    try: return models.User.objects.get(id=body['user_id'])
    except models.User.DoesNotExist: raise KeyError


def remove_token() -> str:
    """Generate an expirated token"""

    payload = {
        'exp': datetime.datetime.now(datetime.UTC) - datetime.timedelta(weeks=1),
        'iat': datetime.datetime.now(datetime.UTC),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token