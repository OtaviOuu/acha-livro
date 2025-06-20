from django.db import models
# Create your models here.

class Termo(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='termos')

    def __str__(self):
        return self.name