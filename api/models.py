from django.db import models


class Topic(models.Model):
    text = models.CharField(max_length=100)
    parent = models.ForeignKey('self', related_name="children", blank=True,
                               null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Topics"
        verbose_name_plural = "Topics"

    def __unicode__(self):
        return "%s " % self.text

    def __str__(self):
        return u'%s' % self.text

    def save(self, *args, **kwargs):
        if Topic.objects.filter(parent=self.parent).count() == 5:
            return
        else:
            super().save(*args, **kwargs)
