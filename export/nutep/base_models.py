from django.db import models


class BaseContainer(models.Model):
    number = models.CharField(max_length=12)
    size = models.CharField(blank=True, null=True, max_length=3)
    type = models.CharField(blank=True, null=True, max_length=10)    
    line = models.CharField(blank=True, null=True, max_length=150)
    def __unicode__(self):
        return u'{0}'.format(self.number if self.number else self.id)        
    class Meta:
        abstract = True