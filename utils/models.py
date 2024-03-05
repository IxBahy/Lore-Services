from django.db import models

class UserBase(models.Model):
# ======================================================================================
# Almost all models in the project inherit from a common base class named BaseInfo.
# This base class provides common fields such as created_by, creation_date, is_active,
# update_date, updated_by, and version. By inheriting from this base class, models
# automatically gain these fields and their functionalities.
# ======================================================================================
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    class Meta:
        abstract = True

