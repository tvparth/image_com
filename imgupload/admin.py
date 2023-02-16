from django.contrib import admin
from . models import ImageModel
# Register your models here.
@admin.register(ImageModel)
class PhotoModelAdmin(admin.ModelAdmin):
    list_display = ['upd_image']
