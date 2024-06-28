from django.db import models
from django.contrib.auth.models import User

class Booklet(models.Model):
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='booklets/')
    upload_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title