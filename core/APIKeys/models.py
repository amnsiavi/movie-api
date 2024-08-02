from django.db import models
from Users.models import UserModel
from datetime import datetime
import uuid
import secrets
# Create your models here.

class ApiKeys(models.Model):

    user = models.ForeignKey(UserModel,on_delete=models.CASCADE)
    access_key = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    secret_key = models.CharField(max_length=200,default=secrets.token_urlsafe,unique=True)
    created_at = models.DateTimeField(default=datetime.now())

    def __str__(self):
        return f'{self.user} - {self.access_key}'

    def save(self,*args,**kwargs):

        if not self.secret_key:
            self.secret_key = secrets.token_urlsafe
        return super(ApiKeys,self).save(*args,**kwargs)
        

    
