from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=250)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Feedback"
        verbose_name_plural = "User Feedback"
    
    def __str__(self):
        return self.subject

class TouristSpot(models.Model):
    tourist_spot_name= models.CharField(max_length=400)
    image = models.ImageField(upload_to='tourist_spots/')
    description = models.TextField()
    link = models.URLField()

    def __str__(self):
        return self.tourist_spot_name