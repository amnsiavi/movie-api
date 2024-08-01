from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):

    def create_user(self,username,email,password=None,**extra_fields):

        if not username:
            raise ValueError('Username is Required')
        
        if not email:
            raise ValueError('Email is Required')
        
        if not password:
            raise ValueError('Password is Required')
        email = self.normalize_email(email)
        user = self.model(username=username,email=email,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None,**extra_fields):

        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self.create_user(username=username,email=email,password=password,**extra_fields)

class UserModel(AbstractUser):
    
    username = models.CharField(max_length=100,unique=True,blank=False)
    email = models.EmailField(unique=True,blank=False)
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

