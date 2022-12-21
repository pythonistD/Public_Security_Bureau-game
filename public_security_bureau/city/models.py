from django.db import models
from django.contrib.auth.models import User
import psb_infrastructure


# class Analyst(models.Model):
#     first_name = models.CharField(max_length=100)
#     second_name = models.CharField(max_length=100)
#
#
# class Citizen(models.Model):
#     fk_analyst_id = models.ForeignKey(Analyst, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     second_name = models.CharField(max_length=100)
#     stamina = models.SmallIntegerField()
#     intelligence = models.SmallIntegerField()
#
#     class Meta:
#         constraints = [
#             models.CheckConstraint(check=(models.Q(stamina__gte=0) & models.Q(stamina__lte=5)), name='stamina0-5')
#         ]
class Analyst(models.Model):
    analyst_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'analyst'


location_type = (
    ('criminal', 'criminal'),
    ('office', 'office'),
)


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    fk_analyst = models.ForeignKey(Analyst, models.CASCADE)
    location_type = models.CharField(choices=location_type, max_length=100)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'location'


class Sybil(models.Model):
    sybil_id = models.AutoField(primary_key=True)
    fk_analyst = models.ForeignKey(Analyst, models.CASCADE)
    day_counter = models.SmallIntegerField()
    crimes_report = models.TextField(blank=True, null=True)
    number_of_crimes = models.SmallIntegerField()
    blackening_coefficient = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sybil'


class Citizen(models.Model):
    citizen_id = models.AutoField(primary_key=True)
    fk_analyst = models.ForeignKey(Analyst, models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True, null=True)
    second_name = models.CharField(max_length=100, blank=True, null=True)
    stamina = models.SmallIntegerField()
    intelligence = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'citizen'


class PsychoPassport(models.Model):
    series = models.IntegerField()
    number = models.IntegerField()
    fk_citizen_id = models.OneToOneField(Citizen, unique=True, on_delete=models.CASCADE)
    crime_rate = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'psycho_passport'
        constraints = [models.UniqueConstraint(fields=['series', 'number'], name='composite pk psychopass')]


weapons_type = (
    ('knife', 'knife'),
    ('dominator', 'dominator'),
    ('pistol', 'pistol'),
    ('rifle', 'rifle'),
)


class Criminal(models.Model):
    criminal_id = models.AutoField(primary_key=True)
    fk_citizen = models.OneToOneField(Citizen, models.CASCADE, blank=False, null=False)
    fk_location = models.OneToOneField(Location, models.CASCADE)
    weapons = models.CharField(choices=weapons_type, max_length=100)  # This field type is a guess.
    hostages = models.SmallIntegerField()
    number_of_crimes = models.SmallIntegerField()
    threat_coefficient = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'criminal'
