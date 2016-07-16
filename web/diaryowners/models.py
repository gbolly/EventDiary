from django.db import models
# from eventdiaryusers.models import User

class EventCenterOwner(models.Model):
    # user = models.ForeignKey(User)
    center_name = models.CharField(max_length=128)

    def __str__(self):
        return self.center_name
