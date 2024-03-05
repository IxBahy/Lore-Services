from django.db import models
from utils.models import UserBase
# Create your models here.
class Student(UserBase):

    class Meta:
        db_table = 'student'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.first_name + " " + self.last_name
