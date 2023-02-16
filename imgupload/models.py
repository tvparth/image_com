from django.db import models
from django.contrib.auth.models import User

class Cuser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class ImageModel(models.Model):
    upd_image = models.ImageField(upload_to='photos')