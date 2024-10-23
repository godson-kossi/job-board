from __future__ import annotations

import json

from django.http import HttpRequest, HttpResponse

from .constants import *
from . import auth, exceptions, models

import typing

ModelTV = typing.TypeVar('ModelTV')


class Route:

    @classmethod
    def to_route(cls, request, pk = None):
        """Take a http request, an optional object id, and return a http response"""

        route = cls(request, pk)
        route.process()
        return route.response

    def __init__(self, request: HttpRequest, pk):

        self.request = request
        self.id = pk

        self.response = HttpResponse()

    def process(self) -> None:
        """
        Process the request from the method
        Handle exceptions
        """

        self.set_code(OK)

        try:
            if self.request.method == POST: self.on_POST()
            elif self.request.method == GET: self.on_GET()
            elif self.request.method == PATCH: self.on_PATCH()
            elif self.request.method == DELETE: self.on_DELETE()
            else: raise exceptions.MethodNotAllowedError

        except exceptions.BaseHttpException as error: self.set_error(error)

    def on_POST(self) -> None: raise exceptions.MethodNotAllowedError
    def on_GET(self) -> None: raise exceptions.MethodNotAllowedError
    def on_PATCH(self) -> None: raise exceptions.MethodNotAllowedError
    def on_DELETE(self) -> None: raise exceptions.MethodNotAllowedError

    def set_code(self, code: int) -> None:
        """Set the code for the http response"""
        self.response.status_code = code

    def get_body(self, *args: str) -> dict:
        """
        Return the decoded json body
        If args are set, verify if all body keys match
        Raise BadRequestError if body is empty or keys don't match
        """

        try: data = json.loads(self.request.body)
        except json.JSONDecodeError: raise exceptions.BadRequestError('Expected json body')

        if args:
            try: self.verify_body(data, args)
            except KeyError as error: raise exceptions.BadRequestError(str(error))

        return data

    def set_body(self, **kwargs) -> None:
        """
        Set the body of the http response
        Encode kwargs in json
        """

        self.response.headers['content-type'] = 'application/json'
        self.response.write(json.dumps(kwargs))

    @staticmethod
    def verify_body(data: dict, keys: tuple[str, ...]) -> None:
        """
        Verify if all data keys match keys
        Raise keyerror if there is missing or unknown keys
        """

        required_keys = [key for key in keys if not key[0] == '~']

        missing_keys = set(required_keys) - set(data.keys())
        unknown_keys = set(data.keys()) - set(keys)

        if missing_keys: raise KeyError(f"Missing value(s) for : {', '.join(missing_keys)}")
        if unknown_keys: raise KeyError(f"Unknown key(s): {', '.join(unknown_keys)}")

    def set_error(self, error: exceptions.BaseHttpException) -> None:
        self.set_code(error.code)
        if error: self.set_body(error=f"{error}")

    @staticmethod
    def restrict(flags:int) -> typing.Callable[[typing.Callable[[Route], None]], typing.Callable[[Route], None]]:
        """Set the permission flags for this action"""
        def wrapper(func: typing.Callable[[Route], None]) -> typing.Callable[[Route], None]:
            def inner(route: Route) -> None:

                if not route.get_authenticated_user().authorizations & flags: raise exceptions.ForbiddenError

                func(route)

            return inner
        return wrapper

    def set_auth_cookie(self, cookie: str):

        self.response.set_cookie(
            key='jwt_token',
            value=cookie,
            httponly=True,
            secure=True,
            samesite='Strict')

    def get_authenticated_user(self) -> models.User:

        try: return auth.validate_token(self.request.COOKIES)
        except (KeyError, ValueError, PermissionError): raise exceptions.UnauthorizedError

    def get_model(self, model: typing.Type[ModelTV]) -> ModelTV:
        """Find the corresponding model to the id pass in the route"""

        try: return model.objects.get(pk=self.id)
        except model.DoesNotExist: raise exceptions.NotFoundError(f"{model.__name__}#{self.id} not found")
