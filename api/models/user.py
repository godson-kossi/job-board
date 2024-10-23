from __future__ import annotations

import typing

from django.db import models

from .. import exceptions


class User(models.Model):

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    authorizations = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"User[{self.email}]#{self.id}"

    @classmethod
    def authenticate(cls, email: str, password: str) -> typing.Self:
        """
        Return the user where email and password match
        Raise ValueError if no user has email or password is wrong
        """

        try: user = cls.objects.get(email=email)
        except cls.DoesNotExist: raise ValueError("Incorrect email")

        #if user.password != hash(password): raise ValueError("Incorrect password")
        if user.password != password: raise ValueError("Incorrect password")

        return user

    def get_type(self):

        try: return self.applicant_set.all()[0]
        except IndexError:
            try: return self.company_set.all()[0]
            except IndexError: raise KeyError("No type")

    @classmethod
    def create(cls, email: str, password: str, authorizations: int = 0) -> User:
        """
        Create a new user and return it
        Raise ValueError if email is already used
        """

        #data['password'] = hash(data['password'])

        user, created = cls.objects.get_or_create(email=email, defaults={"password": password, "authorizations": authorizations})
        if not created: raise ValueError("Email already used")

        user.save()

        return user