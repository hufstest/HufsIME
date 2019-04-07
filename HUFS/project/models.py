from django.db import models

class Blog(models.Model):
    def __str__(self) :
        return self.title
    title = models.CharField(max_length = 200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()
    
#models.무슨Field(무슨무슨~)