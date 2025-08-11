from django.db import models
from cloudinary_storage.storage import RawMediaCloudinaryStorage
class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    college = models.CharField(max_length=255)
    branch = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50)
    file_url = models.URLField()
    file_type = models.CharField(max_length=10)
    size = models.IntegerField()  # Size in bytes
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Document(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/', storage=RawMediaCloudinaryStorage())
    public_id = models.CharField(max_length=255, blank=True)  # Add this
    resource_type = models.CharField(max_length=50, blank=True)  # Add this
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name