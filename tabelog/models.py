from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from django.shortcuts import reverse


class UserType(models.TextChoices):
    FREE = 'FREE', '無料'
    PAID = 'PAID', '有料'
    SUPPORTER = 'SUPPORTER', 'サポーター'


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("user_type", UserType.SUPPORTER)
        return self.create_user(email, password, **extra_fields)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(max_length=150)
    email = models.EmailField(verbose_name='メールアドレス', unique=True)
    first_name = models.CharField(verbose_name='姓', max_length=20)
    last_name = models.CharField(verbose_name='名', max_length=20)
    user_type = models.CharField(max_length=10, choices=UserType.choices, default=UserType.FREE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_card_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    @property
    def is_free(self):
        return self.user_type == UserType.FREE

    @property
    def is_paid(self):
        return self.user_type == UserType.PAID

    @property
    def is_supporter(self):
        return self.user_type == UserType.SUPPORTER


class Category(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=150)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=150)
    adress = models.CharField(max_length=150)
    opening_hours = models.TimeField()
    close_hours = models.TimeField()
    budget = models.PositiveIntegerField()
    tel = models.CharField(max_length=15)
    image = models.ImageField(null=True, blank=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    category = models.ManyToManyField(Category, related_name='tags', blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    content = models.TextField(blank=True, null=True)
    star = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True, null=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)
    is_publish = models.BooleanField(default=True) #非公開設定の実装が未


class Reservation(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    date = models.DateField(blank=False, null=False)
    time = models.TimeField(blank=False, null=False)
    people = models.IntegerField(blank=False, null=False)
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)


# お気に入り
class Favarit(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    create_datetime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)