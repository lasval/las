# models.py in the users Django app
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from .utils import generate_unique_user_code


USER_TYPE_SELECTION = [
    ("S", "Staff or Superuser"),
    ("A", "Admin"),
    ("U", "User"),
    ("P", "Pro"),
]


class UserManager(BaseUserManager):
    """
    기존 User를 User(=CustomUser)로 사용하기 위해 UserManager를 오버라이드해주는 부분
    """

    def create_user(
        self, user_code, phone, username, user_type, password=None
    ):
        """
        Creates and saves a User with the given type, phone and password.
        """

        contain_types = filter(
            lambda x: (x[0] == user_type), USER_TYPE_SELECTION
        )
        contain_types = list(contain_types)
        length_of_contain_types = len(contain_types)
        if not user_type or length_of_contain_types == 0:
            raise ValueError("Users must have an type.")

        user = self.model(
            user_code=user_code,
            phone=phone,
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        user_code,
        user_type="S",
        phone=None,
        username=None,
        password=None,
    ):
        """
        Creates and saves a superuser with the given type, phone and password.
        """
        user = self.create_user(
            user_code=user_code,
            user_type=user_type,
            phone=phone,
            username=username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    User = 계정 (커스텀 유저 모델)
    (DRF에서 사용하는 유저를 기반으로 필드를 원하는대로 만들어서 사용하기 위함)
    """

    user_code = models.CharField(max_length=64, unique=True)
    user_type = models.CharField(max_length=1, choices=USER_TYPE_SELECTION)
    phone = models.CharField(
        _("phone number"), max_length=20, null=True, blank=True
    )
    username = models.CharField(
        _("username"), max_length=150, unique=False, null=True, blank=True
    )
    first_name = None
    last_name = None

    objects = UserManager()
    USERNAME_FIELD = "user_code"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"USER({self.id})(TYPE:{self.user_type}), PHONE : {self.phone}"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.is_superuser

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # simplest possible answer: Yes, always
        return True

    class Meta:
        # unique_together = ["user_type", "phone"]
        # 유저 타입별로 phone번호가 유니크하도록 처리
        constraints = [
            models.UniqueConstraint(
                fields=["user_type", "phone"],
                name="unique_phone",
            ),
        ]
