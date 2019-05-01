from django.db import models

class Blog(models.Model):
    def __str__(self) :
        return self.title
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()

class hashtag(models.Model):
    name=models.CharField(max_length=100)

#models.무슨Field(무슨무슨~)