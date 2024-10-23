from .constants import *
from . import generic, models, exceptions, auth


class Adverts:

    class Index(generic.Route):

        @generic.Route.restrict(COMPANY | ADMIN)
        def on_POST(self):
            """Create a new advert"""

            data = self.get_body(*models.Advert.KEYS, '~company')

            company = self.get_company(data.get('company', None))

            models.Advert(
                title=data['title'],
                salary=data['salary'],
                contract=data['contract'],
                duration=data['duration'],
                competences=data['competences'],
                short_desc=data['short_desc'],
                long_desc=data['long_desc'],
                company=company
            ).save()

            self.set_code(CREATED)

        def on_GET(self):
            """Get all adverts"""

            try: user = self.get_authenticated_user().get_type()
            except (exceptions.UnauthorizedError, KeyError): user = None

            if isinstance(user, models.Company): adverts = user.advert_set.all()
            else: adverts = models.Advert.objects.all()

            self.set_body(adverts=list(map(lambda advert: advert.get_dict(), adverts)))

        def get_company(self, pk: int | None) -> models.Company:
            """Return the company user instance"""

            try: return self.get_authenticated_user().get_type()
            except KeyError:

                if pk is None:
                    raise exceptions.BadRequestError('Not a company account and company key not set')

                try: return models.Company.objects.get(pk=pk)
                except models.Company.DoesNotExist:
                    raise exceptions.BadRequestError('Not a company account and given company does not exist')


    class Advert(generic.Route):

        def on_GET(self):
            """Return an advert"""
            self.set_body(**self.get_advert().get_dict())

        @generic.Route.restrict(ADMIN)
        def on_DELETE(self):
            """Delete an advert"""
            self.get_advert().delete()

        @generic.Route.restrict(ADMIN)
        def on_PATCH(self):
            """Update an advert"""
            try: self.get_advert().update(self.get_body())
            except KeyError as error: raise exceptions.BadRequestError(str(error))

        def get_advert(self) -> models.Advert:
            """Return the advert from the path id"""
            return self.get_model(models.Advert)


    class Apply(generic.Route):

        def on_POST(self):
            """
            Create a new Application from user if token is set, UnidentifiedUser otherwise.
            Excepts user data in body and advert in path
            """

            try: applicant = super().get_authenticated_user().applicant_set.all()[0]
            except exceptions.UnauthorizedError: applicant = None

            models.Application.create(applicant,
                                      self.get_model(models.Advert),
                                      self.get_body(*models.Application.KEYS))
            self.set_code(CREATED)

    class Apps(generic.Route):

        #@generic.Route.restrict(BUSINESS | ADMIN)
        def on_GET(self):
            apps = models.Application.objects.filter(advert=self.get_model(models.Advert))
            self.set_body(apps=list(map(lambda app: app.get_dict(), apps)))


class Users:

    class Index(generic.Route):

        def on_GET(self) -> None:
            """Return data on a user"""

            user = self.get_authenticated_user()

            try: data = user.get_type().get_dict()
            except KeyError: data = {}

            self.set_body(**data)

        def on_DELETE(self):
            """Delete an advert"""
            self.set_auth_cookie(auth.remove_token())

        def on_PATCH(self):
            """Update an advert"""
            try: self.get_authenticated_user().get_type().update(self.get_body())
            except KeyError as error: raise exceptions.BadRequestError(str(error))


    class Authenticate(generic.Route):

        def on_POST(self) -> None:
            """
            Verify user login
            raise BadRequestError if infos are invalid
            Add token to header otherwise
            """

            try: user = models.User.authenticate(**self.get_body('email', 'password'))
            except ValueError as error: raise exceptions.UnauthorizedError(str(error))

            self.set_auth_cookie(auth.generate_token(user))

    class Register(generic.Route):

        def on_POST(self) -> None:
            """
            Register a new user
            Add token to header
            """

            try: user_type = self.get_body()['type']
            except KeyError: raise exceptions.BadRequestError('Missing user type')

            if user_type == 0: user_class = models.Applicant
            elif user_type == 1: user_class = models.Company
            else: raise exceptions.BadRequestError('Invalid user type')

            data = self.get_body(*user_class.KEYS, 'type')
            del data['type']

            try: user_instance = user_class.create(**data)
            except ValueError as error: raise exceptions.BadRequestError(str(error))
            self.set_auth_cookie(auth.generate_token(user_instance.user))
            self.set_code(CREATED)

    class User(generic.Route):

        @generic.Route.restrict(ADMIN)
        def on_POST(self) -> None:
            """Create a new user"""

            try: user_type = self.get_body()['type']
            except KeyError: raise exceptions.BadRequestError('Missing user type')

            if user_type == 0: user_class = models.Applicant
            elif user_type == 1: user_class = models.Company
            else: raise exceptions.BadRequestError('Invalid user type')

            try: user_class.create(**self.get_body(*user_class.KEYS))
            except ValueError as error: raise exceptions.BadRequestError(str(error))

            self.set_code(CREATED)

        @generic.Route.restrict(ADMIN)
        def on_GET(self) -> None:
            """Return data on a user"""
            self.set_body(**self.get_user().get_type().get_dict())

        @generic.Route.restrict(ADMIN)
        def on_DELETE(self):
            """Delete an advert"""
            self.get_user().delete()

        @generic.Route.restrict(ADMIN)
        def on_PATCH(self):
            """Update an advert"""
            try: self.get_user().get_type().update(self.get_body())
            except KeyError as error: raise exceptions.BadRequestError(str(error))

        def get_user(self) -> models.User:
            """Return user from id"""
            return self.get_model(models.User)
