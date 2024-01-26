from django.contrib.auth.models import User
from authors.models import AuthorRegister

class TestMixin():
    def create_user(self, first_name='First', last_name='Last', username='username', email='email@gmail.com',
                    password='pass123456'):
        return User.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                        password=password)

    def create_profile_and_user(self, author='', marital_status='Solteiro', age='44', hometown='Acre',
                                       current_city='Acre',
                                       phone_number='11949558023',
                                       description='Description', slug='slug', profile_status='Público',
                                       is_active=True):

        if not author:
            author = self.create_user()

        return AuthorRegister.objects.create(author=author, marital_status=marital_status, age=age,
                                             hometown=hometown,
                                             current_city=current_city, phone_number=phone_number,
                                             description=description, slug=slug, profile_status=profile_status,
                                             is_active=is_active)