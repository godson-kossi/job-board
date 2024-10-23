from __future__ import annotations

from django.db import models

from . import Applicant


class UnidentifiedApplicant(models.Model):

    email = models.EmailField(unique=True)

    def __str__(self):
        return f"UnidentifiedUser[{self.email}]"

    @classmethod
    def identify(cls, applicant: Applicant) -> None:
        """
        Check if an unidentified user exists with the same email
        Edit the adverts foreign keys and delete the unidentified user
        """

        try: unidentified_applicant = cls.objects.get(email=applicant.user.email)
        except cls.DoesNotExist: return
        else:
            for app in unidentified_applicant.application_set.all():
                app.unidentified_applicant, app.applicant = None, applicant
                app.save()

        unidentified_applicant.delete()
