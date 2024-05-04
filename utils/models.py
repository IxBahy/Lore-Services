from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import (BaseUserManager,AbstractUser,AbstractBaseUser)

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password,username, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        try:
            if not email:
                raise ValueError('The Email must be set')
            if not username:
                raise ValueError('The Username must be set')
            email = self.normalize_email(email)
            user = self.model(email=self.normalize_email(email),username=username, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
        except:
            return None

class User(AbstractUser):
    first_name = models.CharField(max_length=250, blank=True, null=True)
    last_name = models.CharField(max_length=250, blank=True, null=True)
    username = models.CharField(max_length=250,unique=True, blank=True, null=True)
    password = models.CharField(max_length=250, blank=True, null=True)
    img_url = models.CharField(max_length=250, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField(max_length=250, blank=False, null=False, unique=True)
    type = models.CharField(max_length=250, blank=True, null=True)
    clubs = models.ManyToManyField('club.Club', related_name='members',related_query_name="member" , blank=True)
    chats = models.ManyToManyField('Chat', related_name='chats', blank=True)
    roles= ArrayField(models.CharField(max_length=200), blank=True,null=True)
    friends=models.ManyToManyField('self',symmetrical=True)

    USERNAME_FIELD='username'
    objects = CustomUserManager()


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