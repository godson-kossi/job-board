from __future__ import annotations

from django.db import models

from ..constants import *
from . import User


class Company(models.Model):

    KEYS = ('email', 'password', 'name', 'address', 'phone_number')

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"({COMPANY}){self.user}"

    @property
    def email(self) -> str: return self.user.email

    @classmethod
    def create(cls, **data) -> Company:
        """
        Create a company from a dict
        raise ValueError if email us already used
        """

        data['user'] = User.create(data.pop('email'), data.pop('password'), COMPANY)

        company = cls(**data)

        company.save()

        return company

    @property
    def password(self) -> str: return self.user.password

    def get_dict(self) -> dict:
        """Return a dict with user data for json response"""

        return {
            "type": 0,
            "email": self.email,
            "name": self.name,
            "address": self.address,
            "phone_number": self.phone_number,
        }

    def update(self, patch: dict) -> None:
        """
        Update company data from patch dict containing one or more keys
        Raise KeyError if a key in patch doesn't exist
        """

        if 'name' in patch: self.name = patch.pop('name')
        if 'address' in patch: self.address = patch.pop('address')
        if 'phone_number' in patch: self.phone_number = patch.pop('phone_number')

        keys = patch.keys()

        if keys: raise KeyError(f"Unknown key(s): {', '.join(keys)}")

        self.save()
