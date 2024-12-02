from django.db import models


# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=255, unique=True)
    
    def __str__(self) -> str:
        return str(self.id) + '-' + self.name
