from django.db import models

# Create your models here.
class Support(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Thời gian tạo

    def __str__(self):
        return self.name
