from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
