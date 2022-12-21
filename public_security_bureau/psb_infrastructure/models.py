from django.db import models
from city.models import Analyst, Location

transport_type = (
    ('truck', 'truck'),
    ('passenger_car', 'passenger_car'),
)


class Transport(models.Model):
    transport_id = models.AutoField(primary_key=True)
    fk_analyst = models.ForeignKey(Analyst, models.CASCADE)
    transport_type = models.CharField(choices=transport_type, max_length=100)  # This field type is a guess.
    max_speed = models.SmallIntegerField()
    capacity = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'transport'


class HolographicDevice(models.Model):
    holographic_device_id = models.AutoField(primary_key=True)
    fk_current_location_id = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='current_location')
    fk_destination_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='destination_location')

    class Meta:
        managed = False
        db_table = 'holographic_device'
