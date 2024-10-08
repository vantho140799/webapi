from django.db import models

# Create your models here.
class ColoringBook(models.Model):
    title = models.CharField(max_length=255)
    image_url = models.CharField(max_length=255)
    product_url = models.CharField(max_length=255)

    def __str__(self):
        return self.title