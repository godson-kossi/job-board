from __future__ import annotations

from django.db import models

from . import Company


class Advert(models.Model):

    KEYS = ('title', 'salary', 'contract', 'duration', 'competences', 'short_desc', 'long_desc')

    CONTRACT_TYPES = {
        "FX": "Fixed-Term Contract",
        "PX": "Permanent Contract",
        "AS": "Apprenticeship",
        "TJ": "Temp Job",
        "IS": "Internship"
    }

    title = models.CharField(max_length=50)
    salary = models.PositiveSmallIntegerField()
    contract = models.TextField(choices=CONTRACT_TYPES)
    duration = models.PositiveIntegerField()
    competences = models.CharField(max_length=100)
    short_desc = models.CharField(max_length=200)
    long_desc = models.CharField(max_length=1000)

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return f"Advert[{self.title}@{self.company}]#{self.id}"

    def get_dict(self) -> dict:
        """Return a dict with advert data for json response"""

        return {
            "key": self.id,
            "title": self.title,
            "company": self.company.name,
            "salary": self.salary,
            "contract": self.contract,
            "duration": self.duration,
            "competences": self.competences,
            "short_desc": self.short_desc,
            "long_desc": self.long_desc,
        }

    def update(self, patch: dict) -> None:
        """
        Update advert data from patch dict containing one or more keys
        Raise KeyError if a key in patch doesn't exist
        """

        if 'title' in patch: self.title = patch.pop('title')
        if 'salary' in patch: self.salary = patch.pop('salary')
        if 'contract' in patch: self.contract = patch.pop('contract')
        if 'duration' in patch: self.duration = patch.pop('duration')
        if 'short_desc' in patch: self.short_desc = patch.pop('short_desc')
        if 'long_desc' in patch: self.long_desc = patch.pop('long_desc')

        keys = patch.keys()

        if keys: raise KeyError(f"Unknown key(s): {', '.join(keys)}")

        self.save()
