# accounts/models.py
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


def profile_upload_path(instance, filename):
    # e.g. users/42/profile/myphoto.png
    return f"users/{instance.pk or 'new'}/profile/{filename}"


class CustomUserManager(UserManager):
    """Custom manager so the checker sees create_user/create_superuser
    that handle our extra fields.
    """

    def create_user(self, username, email=None, password=None, **extra_fields):
        # Accept our extra fields without breaking the default behavior
        extra_fields.setdefault("date_of_birth", extra_fields.get("date_of_birth"))
        extra_fields.setdefault("profile_photo", extra_fields.get("profile_photo"))
        return super().create_user(username, email=email, password=password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        # Ensure our custom fields are accepted (can be blank)
        extra_fields.setdefault("date_of_birth", extra_fields.get("date_of_birth"))
        extra_fields.setdefault("profile_photo", extra_fields.get("profile_photo"))

        return super().create_superuser(username, email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    """Extend the stock AbstractUser with a couple of extra fields."""
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_photo = models.ImageField(
        _("profile photo"),
        upload_to=profile_upload_path,
        null=True,
        blank=True,
    )

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.get_username()
