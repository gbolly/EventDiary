from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db import models
from web.accounts.models import UserProfile
from web.centers.models import Center


class Merchant(models.Model):

    userprofile = models.OneToOneField(User)
    user_centers = models.OneToOneField(Center, blank=True,)
    bank_acc_num = models.CharField(blank=True, default='', max_length=10)
    approved = models.BooleanField(default=False)

    def __unicode__(self):
        return u'Merchant with username %s' % (self.userprofile.username)
