from django.db import models
from utils.models import User

# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=250, unique=True,blank=False, null=False)
    description = models.CharField(max_length=500, unique=True,blank=False, null=False)
    type = models.CharField(max_length=250,blank=False, null=False)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    current_capacity = models.IntegerField(blank=False, null=False)
    max_capacity = models.IntegerField(blank=False, null=False)
    rating = models.FloatField(blank=False,default='0.0' ,null=False)
    owner=models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    roadmap=models.ForeignKey('Roadmap', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'club'
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'

    # def __str__(self):
    #     return self.name



class Roadmap(models.Model):
    weeks_count = models.IntegerField(blank=False, null=False)
    weeks_capacity = models.IntegerField(blank=False, null=False)
    class Meta:
        db_table = 'roadmap'
        verbose_name = 'Roadmap'
        verbose_name_plural = 'Roadmaps'


class RoadmapWeek(models.Model):
    week_number = models.IntegerField(blank=False, null=False)
    degree =models.IntegerField(blank=False, null=False)
    title = models.CharField(max_length=250, unique=True,blank=False, null=False)
    description = models.CharField(max_length=500, unique=True,blank=False, null=False)
    roadmap_id=models.ForeignKey(Roadmap,related_name="weeks", on_delete=models.CASCADE, blank=False, null=False)
    is_completed = models.BooleanField(blank=False,default=False, null=False)
    class Meta:
        db_table = 'roadmap_week'
        verbose_name = 'RoadmapWeek'
        verbose_name_plural = 'RoadmapWeeks'