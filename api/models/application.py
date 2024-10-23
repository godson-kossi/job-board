from __future__ import annotations

import typing

from django.db import models

from . import Applicant, UnidentifiedApplicant, Advert


class Application(models.Model):

    KEYS = ('firstname', 'lastname', 'email', 'phone_number', 'degree', 'birthdate')

    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50) #TODO
    degree = models.CharField(max_length=100)
    birthdate = models.DateField()

    advert = models.ForeignKey(Advert, on_delete=models.CASCADE)

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, null=True, default=None, blank=True)
    unidentified_applicant = models.ForeignKey(UnidentifiedApplicant, on_delete=models.SET_NULL, null=True, default=None, blank=True)

    def __str__(self):
        return f"App({self.user})=>({self.advert})#{self.id}"

    @property
    def user(self) -> typing.Union[Applicant, UnidentifiedApplicant]:
        """Return the user corresponding to this application"""

        try: return self.applicant
        except Applicant.DoesNotExist: return self.unidentified_applicant

    @classmethod
    def create(cls,
               applicant: typing.Union[Applicant, UnidentifiedApplicant, None],
               advert: Advert,
               infos: dict) -> Application:
        """
        Create an application for a user, advert and user infos
        Raise ValueError if infos are incomplete or User already applied
        """

        for key in cls.KEYS:
            if not infos[key]: raise ValueError(f"Expected value for key {key}")

        if applicant is None:
            infos['unidentified_applicant'] = UnidentifiedApplicant.objects.get_or_create(email=infos['email'])[0]
        else: infos['applicant'] = applicant

        for application in cls.objects.all():
            if application.user.email == infos['email']: raise ValueError(f"User already applied")

        del infos['email']
        infos['advert'] = advert

        instance = cls(**infos)
        instance.save()
        return instance

    def get_dict(self) -> dict:
        """Return a dict with user data for json response"""

        return {
            "email": self.user.email,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "phone_number": self.phone_number,
            "degree": self.degree,
            "birthdate": self.birthdate.isoformat(),
        }
