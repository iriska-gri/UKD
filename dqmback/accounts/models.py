from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ValidationError
import datetime
class Initial(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=150, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150, blank=True)
    middle_name = models.CharField(verbose_name='Отчество', max_length=150, blank=True)
    region = models.ForeignKey('statistic.Region', on_delete=models.PROTECT, verbose_name="Регион", help_text="Заполняется только для пользователей УФНС. Для Администратора и сотрудника ЦА оставьте пустым.", blank=True, null=True)
    permission = models.ForeignKey('Usergroup', on_delete=models.PROTECT, verbose_name="Группа",related_name="group_initial", default=1)
    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    REQUIRED_FIELDS = ["username", "first_name", "last_name", "middle_name"]
        
    def create_user(self, username,  password, lotus, **extra_fields):
        """
        email,
        Create and save a User with the given email and password.
        """
        # print(extra_fields)
        if not username:
            raise ValueError(_('The given username must be set'))


        if 'is_superuser' not in extra_fields or extra_fields['is_superuser'] == False:
            try:
                initial = Initial.objects.get(**extra_fields)
                region = initial.region
                permission = initial.permission
                
                initial.delete()
            except ObjectDoesNotExist:
                
                raise ValidationError({'username': ['Приглашение не найдено']})
            except Exception:
                raise ValidationError({'username': ['Произошла ошибка. Пожалуйста, обратитесь в службу поддержки на почту Lotus: SVC-COD2/М9966/МНС']})
                

        # email = self.normalize_email(email)
        #  email=email,
        user = self.model(username=username,permission=permission, lotus=lotus, region=region, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)

class Restoretable(models.Model):
    user = models.OneToOneField('FNSUser',on_delete=models.PROTECT)
    asktime = models.DateTimeField(auto_now=True)
    randomurl = models.CharField(verbose_name='секрет', max_length=100)

class Permission(models.Model):
    name = models.CharField(verbose_name='Название', max_length=150, blank=True)
    link=  models.CharField(verbose_name='Ссылка', max_length=150, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"


class Usergroup(models.Model):
    name = models.CharField(verbose_name='Название', max_length=150, blank=True)
    permission = models.ManyToManyField(Permission, verbose_name="Права")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

class FNSUser(AbstractUser):
    middle_name = models.CharField(verbose_name='Отчество', max_length=150, blank=True)
    photo = models.ImageField(verbose_name='Аватар', upload_to='avatar', blank=True, default='avatar/default.jpg')
    lotus = models.CharField(verbose_name='Адрес Lotus', max_length=350, blank=True)
    region = models.ForeignKey('statistic.Region', on_delete=models.PROTECT, verbose_name="Регион",related_name="region_region",help_text="Заполняется только для пользователей УФНС. Для Администратора и сотрудника ЦА оставьте пустым.", blank=True, null=True)
    phone = models.CharField(verbose_name='Телефон', max_length=350, blank=True, null=True)
    ip_client=models.CharField(verbose_name='Ip', max_length=350, blank=True, null=True)
    permission = models.ForeignKey('Usergroup', on_delete=models.PROTECT, verbose_name="Группа",related_name="group_user", default=1)
    objects = CustomUserManager()


