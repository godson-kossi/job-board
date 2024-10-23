from django.contrib import admin

from . import models

admin.site.register(models.User)
admin.site.register(models.Applicant)
admin.site.register(models.Company)
admin.site.register(models.UnidentifiedApplicant)
admin.site.register(models.Advert)
admin.site.register(models.Application)
