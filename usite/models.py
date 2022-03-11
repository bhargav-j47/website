from django.db import models

from tinymce.models import HTMLField
import uuid
from django.core.validators import MinLengthValidator
# Create your models here.


class Contact(models.Model):

    name = models.CharField(max_length=122, default='SOME STRING')
    email = models.EmailField(max_length=122)
    phone = models.CharField(max_length=12, default=00000000)
    desc = models.TextField()

    def __str__(self):
        return self.name


class blogposts(models.Model):


    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    #uuid=models.BigAutoField(primary_key=True,max_length=4,validators=[MinLengthValidator(4)],editable=False)

    title= models.CharField( max_length=100)

    content=HTMLField()

    date=models.DateField((""), auto_now_add = True)

    author=models.CharField(max_length = 25, default = "Indian Nerds")

    about=models.CharField( max_length=500 , default= "this blog contens a wide information about topic . you can get wide knowledge of it after you read it. It will cover all your queries abot this topic")

    thumbnail=models.ImageField(upload_to="thumbnail/",default="/thumbnail/icon.jpg")


    def __str__(self):
        return self.title


