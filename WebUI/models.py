from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)
from validators import ContactNumberValidator
# Create your models here.

request_choices = ( ('P','Pending'), ('A','Accepted'), ('D','Declined'))

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    ##Profile Detail Fields
    first_name = models.CharField(max_length=128,verbose_name="First Name")
    last_name = models.CharField(max_length=128,verbose_name="Last Name")
    contact_number = models.BigIntegerField(verbose_name="Contact Number", validators=[ContactNumberValidator], null=True)

    objects = CustomUserManager()


    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name + ' ' + self.last_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def is_authenticated(self):
        return True

    def __unicode__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_confirmed_trips(self):
        return Trip.objects.filter(user=self)

    def accept_request(self, req):
        if req.trip.user == self:
            Request.accept()
            return True
        else:
            return False

    def decline_request(self,req):
        if req.trip.user == self:
            Request.decline()
            return True
        else:
            return False

    def received_requests(self):
        return Request.objects.filter(trip__user=self)

    def sent_requests(self):
        return Request.objects.filter(from_user=self)

class Trip(models.Model):
    user = models.ForeignKey(CustomUser, null=False, blank=False)
    time = models.DateTimeField(verbose_name='Time of Journey', blank=False, null=False)
    cluster = models.TextField(null=False, blank=False)
    travel_distance = models.FloatField(null=False, blank=False)
    start_place = models.TextField(verbose_name="Starting Place", null=False, blank=True)
    end_place = models.TextField(verbose_name="Ending Place", null=False, blank=True)

    def __unicode__(self):
        return self.start_place + " - " + self.last_name + " on " + self.time

class Request(models.Model):
    from_user = models.ForeignKey(CustomUser, null=False, blank=False)
    trip = models.ForeignKey(Trip, null=False, blank=False)
    start_lat = models.FloatField(null=False, blank=False)
    start_lng = models.FloatField(null=False, blank=False)
    end_lat = models.FloatField(null=False, blank=False)
    end_lng = models.FloatField(null=False, blank=False)
    start_place = models.TextField(verbose_name="Pick-up Location",null=False, blank=True)
    end_place = models.TextField(verbose_name="Drop-off Location", null=False, blank=True)
    status = models.CharField(max_length=20, choices = request_choices)

    def __unicode__(self):
        return self.from_user + " to " + self.trip.user + " - " + self.trip

    def accept(self):
        self.status='A'

    def decline(self):
        self.status='D'
