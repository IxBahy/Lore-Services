from django.db import models
from utils.models import UserBase

# Create your models here.
class Instructor(UserBase):
    class Meta:
        db_table = 'instructor'
        verbose_name = 'Instructor'
        verbose_name_plural = 'Instructors'

    def __str__(self):
        return self.first_name + " " + self.last_name