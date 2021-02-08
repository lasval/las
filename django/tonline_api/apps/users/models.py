# models.py in the users Django app
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """
    기존 User를 CustomUser로 사용하기 위해 UserManager를 오버라이드해주는 부분
    """

    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email and password.
        """

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username=None, password=None):
        """
        Creates and saves a superuser with the given type, email and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    """
    커스텀 유저 모델
    (DRF에서 사용하는 유저를 기반으로 필드를 원하는대로 만들어서 사용하기 위함)
    """

    email = models.EmailField(
        _("email address"), unique=True, max_length=254, null=True, blank=True
    )
    username = models.CharField(
        _("username"), max_length=150, unique=False, null=True, blank=True
    )
    first_name = None
    last_name = None

    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"USER({self.id}), EMAIL : {self.email}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # simplest possible answer: Yes, always
        return True
