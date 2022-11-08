from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class MyAccountManager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username=username,
            password=password
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user 
      

class Account(AbstractBaseUser):
    username                = models.CharField(verbose_name="username", max_length=30, unique=True)
    date_joined             = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    is_superuser            = models.BooleanField(default=False)
    

    USERNAME_FIELD = 'username'
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.username

