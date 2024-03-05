from django.db import models

class BaseInfo(models.Model):
# ======================================================================================
# Almost all models in the project inherit from a common base class named BaseInfo.
# This base class provides common fields such as created_by, creation_date, is_active,
# update_date, updated_by, and version. By inheriting from this base class, models
# automatically gain these fields and their functionalities.
# ======================================================================================
    created_by = models.BigIntegerField(blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    update_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_by = models.BigIntegerField(blank=True, null=True)
    class Meta:
        abstract = True

