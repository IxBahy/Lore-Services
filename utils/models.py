from django.db import models
from django.contrib.postgres.fields import ArrayField
class User(models.Model):
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    username = models.CharField(max_length=250, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=True, null=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    clubs = models.ManyToManyField('club.Club', related_name='students' , blank=True)
    chats = models.ManyToManyField('Chat', related_name='chats', blank=True)
    roles= ArrayField(models.CharField(max_length=200), blank=True)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Chat(models.Model):
    type = models.CharField(max_length=250, blank=True, null=True)
    name = models.CharField(max_length=250, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    is_channel = models.BooleanField(blank=False, null=False)
    admins = models.ManyToManyField(User, related_name='admins', blank=True)
    class Meta:
        db_table = 'chat'
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'

class Message(models.Model):
    content = models.CharField(max_length=250, blank=True, null=True)
    chat_id=models.ForeignKey(Chat, on_delete=models.CASCADE, blank=False, null=False)
    sender_id=models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    class Meta:
        db_table = 'message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'