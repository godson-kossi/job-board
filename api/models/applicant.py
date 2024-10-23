from __future__ import annotations

from django.db import models

from ..constants import *
from . import User


class Applicant(models.Model):

    KEYS = ('email', 'password', 'firstname', 'lastname', 'phone_number', 'degree', 'birthdate')

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    degree = models.CharField(max_length=100)
    birthdate = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"(APPLICANT){self.user}"

    @property
    def email(self) -> str: return self.user.email

    @property
    def password(self) -> str: return self.user.password

    @classmethod
    def create(cls, **data) -> Applicant:
        """
        Create an applicant from a dict
        Remove an unidentified applicant with same email if any
        raise ValueError if email us already used
        """

        data['user'] = User.create(data.pop('email'), data.pop('password'), APPLICANT)

        applicant = cls(**data)

        from . import UnidentifiedApplicant
        UnidentifiedApplicant.identify(applicant)

        applicant.save()

        return applicant

    def get_dict(self) -> dict:
        """Return a dict with applicant data for json response"""

        return {
            "type": 1,
            "email": self.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone_number": self.phone_number,
            "degree": self.degree,
            "birthdate": self.birthdate.isoformat(),
        }

    def update(self, patch: dict) -> None:
        """
        Update applicant data from patch dict containing one or more keys
        Raise KeyError if a key in patch doesn't exist
        """

        if 'firstname' in patch: self.firstname = patch.pop('firstname')
        if 'lastname' in patch: self.lastname = patch.pop('lastname')
        if 'phone_number' in patch: self.phone_number = patch.pop('phone_number')
        if 'degree' in patch: self.degree = patch.pop('degree')
        if 'birthdate' in patch: self.birthdate = patch.pop('birthdate')

        keys = patch.keys()

        if keys: raise KeyError(f"Unknown key(s): {', '.join(keys)}")

        self.save()
