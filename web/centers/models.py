from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_libs.models_mixins import TranslationModelMixin
from hvad.models import TranslatableModel, TranslatedFields
from cloudinary.models import CloudinaryField
from web.accounts.models import UserProfile


# States in Nigeria
NIGERIAN_LOCATIONS = [
    (1, 'Abia'), (2, 'Abuja'), (3, 'Adamawa'),
    (4, 'Akwa Ibom'), (5, 'Anambra'), (6, 'Bauchi'),
    (7, 'Bayelsa'), (8, 'Benue'), (9, 'Borno'),
    (10, 'Cross River'), (11, 'Delta'), (12, 'Ebonyi'),
    (13, 'Edo'), (14, 'Ekiti'), (15, 'Enugu'),
    (16, 'Gombe'), (17, 'Imo'), (18, 'Jigawa'),
    (19, 'Kaduna'), (20, 'Kano'), (21, 'Katsina'),
    (22, 'Kebbi'), (23, 'Kogi'), (24, 'Kwara'),
    (25, 'Lagos'), (26, 'Nassarawa'), (27, 'Niger'),
    (28, 'Ogun'), (29, 'Ondo'), (30, 'Osun'),
    (31, 'Oyo'), (32, 'Plateau'), (33, 'Rivers'),
    (34, 'Sokoto'), (35, 'Taraba'), (36, 'Yobe'),
    (37, 'Zamfara'),
]

ALL_LOCATIONS = NIGERIAN_LOCATIONS

class Center(models.Model):

    price = models.IntegerField()
    capacity = models.IntegerField()
    owner = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(blank=True, null=False, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    location = models.SmallIntegerField(choices=ALL_LOCATIONS, default=84)
    address = models.CharField(max_length=100, blank=False, default='')
    active = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    image = CloudinaryField(
        resource_type='image',
        type='upload',
        blank=True,
        default="img/test-run-gb.jpeg"
    )
    is_available = models.BooleanField(default=True)

    # def thumbnail_image_url(self):
    #     """Returns a thumbnail image URL
    #     """
    #     image_url = self.image.build_url(
    #         width=SITE_IMAGES['thumbnail_image_width'],
    #         height=SITE_IMAGES['thumbnail_image_height'],
    #         crop="fit",
    #     )
    #     return image_url

    def state_name(self):
        """Returns the state name
        """
        return dict(NIGERIAN_LOCATIONS).get(self.location)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/center/{}/" .format(self.id)


class Booking(models.Model):
    center = models.ForeignKey(Center)
    owner = models.ForeignKey(User)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    customer_name = models.CharField(max_length=100, null=False, blank=False)
    phone_number = models.IntegerField()
    is_approved = models.BooleanField(default=False)


class BookingStatus(TranslationModelMixin, TranslatableModel):
    """
    Master data containing all booking status.
    For translatable fields check ``BookingStatusTranslation``.
    :slug: A unique slug identifier.
    translated:
    :name: The displayable name for the status.
    """
    slug = models.SlugField(
        verbose_name=_('Slug'),
    )

    translations = TranslatedFields(
        name=models.CharField(
            verbose_name=_('Name'),
            max_length=128,
        )
    )
        
