from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from common.models import BaseModel


class UserManager(BaseUserManager):
    use_in_migrations = True


    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields) 


    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True set.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True set.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True set.')

        return self._create_user(email, password, **extra_fields)



# Create your models here.


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()
    def __str__(self):
        return self.email



class Profile(BaseModel):
    profile_name = models.CharField(max_length=100)
    def __str__(self):
        return self.profile_name

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    profile = models.ForeignKey(Profile, on_delete= models.CASCADE, related_name='profile')
    activation_code = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.user) + " " + str(self.profile)