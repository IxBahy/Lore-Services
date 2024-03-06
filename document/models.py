from django.db import models
from club.models import Club
# Create your models here.

class Document(models.Model):
    name = models.CharField(max_length=250, unique=True,blank=False, null=False)
    description = models.CharField(max_length=500, unique=True,blank=False, null=False)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    file_url = models.CharField(max_length=250, blank=True, null=True)
    summarized_file_url = models.CharField(max_length=250, blank=True, null=True)
    gener= models.CharField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    size = models.IntegerField(blank=False, null=False)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    club_id=models.ForeignKey(Club, on_delete=models.CASCADE, blank=False, null=False)
    class Meta:
        db_table = 'document'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'

    def __str__(self):
        return self.name