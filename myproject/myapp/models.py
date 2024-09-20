from django.db import models

class datab(models.Model):
    title = models.CharField(max_length = 255)
    image = models.ImageField(upload_to='images/')
    jn = models.CharField(max_length=225, null=True, blank=True) 
    vn = models.CharField(max_length=225, null=True, blank=True)
    sn = models.CharField(max_length=225, null=True, blank=True)
    my = models.CharField(max_length=225, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
  

class datab2(models.Model):
    year = models.IntegerField()
    pdf = models.FileField(upload_to='pdfs/')
    
    def __str__(self):
       return f"{self.year} - {self.pdf.name}"  
