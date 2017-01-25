from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from web.deals.models import COUNTRY_CHOICES, ALL_LOCATIONS

class UserProfile(models.Model):

    user = models.OneToOneField(User)
    is_merchant = models.BooleanField(default=False)
    location = models.SmallIntegerField(choices=ALL_LOCATIONS, default=84)
    phonenumber = models.CharField(blank=True, default='', max_length=20)

    def check_diff(self, request_value):

        for field in request_value:
            if getattr(self, field, False) != False \
                and getattr(self, field) != request_value[field] and \
                    request_value[field] != '':
                    setattr(self, field, request_value[field])
        self.save()
        return {
            u'is_merchant': self.is_merchant,
            u'location': self.location,
            u'phonenumber': self.phonenumber,
        }

    def is_complete(self):
        """Checks if a user's profile is completed"""
        for field in self._meta.get_all_field_names():
            try:
                fieldattr = getattr(self, field)
                if fieldattr == '':
                    return False
                if type(fieldattr) == User:
                    if fieldattr.first_name == '' or fieldattr.last_name == '':
                        return False
            except:
                pass
        return True

    def is_approved_merchant(self):
        """Checks if the user is an approved merchant"""
        try:
            return getattr(self.merchant, 'approved', False)
        except:
            return False

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
