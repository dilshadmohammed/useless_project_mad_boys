from django.db import models

# Create your models here.
import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from utils.types import TokenType


def default_expiry():
    return timezone.now() + timedelta(days=7)

class User(AbstractBaseUser):
    id = models.CharField(primary_key=True, max_length=36, default=uuid.uuid4)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=200, blank=True, null=True)
    

    # Required fields for createsuperuser command
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
class UserProfile(models.Model):
    user = models.ForeignKey(User, related_name='profile', on_delete=models.CASCADE)
    xp = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s profile"

    def add_xp(self, points):
        self.xp += points
        self.save()
    
    def reduce_xp(self, points):
        self.xp -= points
        self.save()


class Token(models.Model):
    TOKEN_TYPE_CHOICES = [
        (TokenType.ACCESS, TokenType.ACCESS),
        (TokenType.REFRESH, TokenType.REFRESH)
        ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user')
    token = models.TextField(null=False)
    token_type = models.CharField(max_length=20,choices=TOKEN_TYPE_CHOICES,null=False)
    expiry = models.DateTimeField(default=default_expiry)
    
