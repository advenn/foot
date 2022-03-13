from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


def get_default_profile_photo():
    return 'https://www.gravatar.com/avatar/00000000000000000000000000000000?d=mp&f=y'


class UserManager(BaseUserManager):
    def create_user(self, email, password=None,**kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('username'):
            raise ValueError('Users must have a valid username.')

        user = self.model(
            email=self.normalize_email(email), username=kwargs.get('username')
        )

        user.set_password(password)
        user.save(using=self._db) 

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)

        user.is_admin = True
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)

        user.is_admin = True
        user.save()

        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    hide_email = models.BooleanField(default=True)


    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    

class Tour(models.Model):
    number = models.IntegerField()
    league = models.ForeignKey(to="League", on_delete=models.CASCADE)

    def __str__(self):
        return f"tour of {self.number} on {self.league}"

class U:
    pass

class League(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Match(models.Model):
    home_team = models.CharField(max_length=100)
    away_team = models.CharField(max_length=100)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)
    tour = models.ForeignKey(to="Tour", on_delete=models.CASCADE)
    league = models.ForeignKey(to="League", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} on {self.date} at {self.date.strftime('%H:%M')}"


class Predict(models.Model):
    match = models.ForeignKey('Match', on_delete=models.CASCADE)
    # user = 
    # def __str__(self):
    #     return f"{self.home_team} vs {self.away_team} on {self.date} at {self.date.strftime('%H:%M')}"

    def __str__(self):
        return self.match.home_team + " : " + self.match.away_team

    