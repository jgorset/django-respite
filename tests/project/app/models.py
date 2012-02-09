from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Author(models.Model):
    name = models.CharField(max_length=255)

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_published = models.BooleanField()
    created_at = models.DateTimeField()
    tags = models.ManyToManyField(Tag, blank=True)
    author = models.ForeignKey(Author, related_name='articles')
