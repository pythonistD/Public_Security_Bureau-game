from django.db import models
from city.models import Citizen, Criminal
from psb_infrastructure.models import HolographicDevice, Transport


class Inspector(models.Model):
    inspector_id = models.AutoField(primary_key=True)
    fk_citizen = models.OneToOneField(Citizen, models.CASCADE, blank=False, null=False)
    successful_detentions = models.SmallIntegerField()
    factor_of_utility = models.SmallIntegerField()
    authority = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'inspector'


class Performer(models.Model):
    performer_id = models.AutoField(primary_key=True)
    fk_citizen = models.OneToOneField(Citizen, models.CASCADE, blank=False, null=False)
    successful_detentions = models.SmallIntegerField()
    fk_inspector = models.ForeignKey(Inspector, models.CASCADE, blank=True, null=True)
    factor_of_utility = models.SmallIntegerField()
    authority = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'performer'


class TaskForce(models.Model):
    task_force_id = models.AutoField(primary_key=True)
    fk_performers_ids = models.ForeignKey(Performer, on_delete=models.CASCADE)
    fk_inspector_id = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    fk_transport_id = models.ForeignKey(Transport, on_delete=models.CASCADE)
    fk_criminal_id = models.ForeignKey(Criminal, on_delete=models.CASCADE)
    fk_holographic_device = models.ForeignKey(HolographicDevice, models.CASCADE)
    success_rate = models.SmallIntegerField()

    class Meta:
        managed = False
        db_table = 'task_force'
