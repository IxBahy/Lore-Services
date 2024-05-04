from django.db import models
from django.conf import settings
# Create your models here.

class Club(models.Model):
    name = models.CharField(max_length=250, unique=True,blank=False, null=False)
    description = models.CharField(max_length=500, unique=True,blank=False, null=False)
    type = models.CharField(max_length=250,blank=False, null=False)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    current_capacity = models.IntegerField(blank=False, null=False)
    max_capacity = models.IntegerField(blank=False, null=False)
    rating = models.FloatField(blank=False,default='0.0' ,null=False)
    owner=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    category = models.CharField(max_length=250, blank=False, null=False ,default='General')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'club'
        verbose_name = 'Club'
        verbose_name_plural = 'Clubs'

    # def __str__(self):
    #     return self.name



class Roadmap(models.Model):
    weeks_count = models.IntegerField(blank=False, null=False)
    weeks_capacity = models.IntegerField(blank=False, null=False)
    club=models.OneToOneField(Club,related_name="roadmap", on_delete=models.CASCADE, blank=False, null=True)
    class Meta:
        db_table = 'roadmap'
        verbose_name = 'Roadmap'
        verbose_name_plural = 'Roadmaps'


class RoadmapWeek(models.Model):
    degree =models.IntegerField(blank=False, null=False)
    title = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    roadmap_id=models.ForeignKey(Roadmap,related_name="weeks", on_delete=models.CASCADE, blank=False, null=False)
    users_progress = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UserRoadmapWeek', related_name='weeks_progress')
    class Meta:
        db_table = 'roadmap_week'
        verbose_name = 'RoadmapWeek'
        verbose_name_plural = 'RoadmapWeeks'



class ClubReview(models.Model):
    club_id=models.ForeignKey(Club,related_name="reviews", on_delete=models.CASCADE, blank=False, null=False)
    user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
    review = models.CharField(max_length=500, unique=True,blank=False, null=False)
    rating = models.FloatField(blank=False,default='0.0' ,null=False)
    class Meta:
        db_table = 'club_review'
        verbose_name = 'ClubReview'
        verbose_name_plural = 'ClubReviews'


class UserRoadmapWeek(models.Model):

     user_id=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null=False)
     week_id=models.ForeignKey(RoadmapWeek, on_delete=models.CASCADE, blank=False, null=False)
     is_completed = models.BooleanField(blank=False,default=False, null=False)

     class Meta:
        db_table = 'user_roadmap_week'
        verbose_name = 'UserRoadmapWeek'
        verbose_name_plural = 'UserRoadmapWeeks'