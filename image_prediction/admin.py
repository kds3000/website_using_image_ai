from django.contrib import admin
from image_prediction.models import Image

admin.site.register(Image)

class ImageAdmin(admin.ModelAdmin):
    fields = ['image']