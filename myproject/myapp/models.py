from django.db import models

class datab(models.Model):
    title = models.CharField(max_length = 255)
    image = models.ImageField(upload_to='images/')
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    