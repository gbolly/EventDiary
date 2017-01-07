from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_libs.models_mixins import TranslationModelMixin
from hvad.models import TranslatableModel, TranslatedFields
from cloudinary.models import CloudinaryField
from web.accounts.models import UserProfile
from phonenumber_field.modelfields import PhoneNumberField


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

LAGOS_AREAS = [
    (1, 'Abule Ijesha'), (2, 'Abule egba'), (3, 'Alagbado'), (4, 'Akowonjo'),
    (5, 'Baruwa'), (6, 'Dopemu'), (7, 'Egbe'), (8, 'Egbeda'),
    (9, 'Ejigbo'), (10, 'Ijegun'), (11, 'Ikotun'), (12, 'Egan'),
    (13, 'Iyana Ipaja'), (14, 'Ipaja'), (15, 'Jakande'), (16, 'Ojo'),
    (17, 'Ojota'), (18, 'Idimu'), (19, 'Adeniyi jones'), (20, 'Agbara'),
    (21, 'Agege'), (22, 'Agidingbi'), (23, 'Agric'), (24, 'Aguda'),
    (25, 'Airport road'), (26, 'Ajah'), (27, 'Ajao estate'), (28, 'Ajeromi-Ajegunle'),
    (29, 'Ajeromi-Ifelodun'), (30, 'Akessan Estate'), (31, 'Akoka'), (32, 'Akute-Ajuwon'),
    (33, 'Alausa'), (34, 'Alimosho'), (35, 'Allen'), (36, 'Amuwo-odofin'),
    (37, 'Anthony'), (38, 'Apapa'), (39, 'Apapa-Ajegunle'), (40, 'Awolowo'),
    (41, 'Awolowo way'), (42, 'Badagry'), (43, 'Banana-Island'), (44, 'Bariga'),
    (45, 'Bode Thomas'), (46, 'Bourdillon'), (47, 'Chisco'), (48, 'Constain-Ijora Olopa'),
]

ALL_LOCATIONS = NIGERIAN_LOCATIONS
ALL_AREA = LAGOS_AREAS

class CenterManager(models.Manager):

    def get_area_name(self, area):
        """Returns the area name
        """
        c = str(area).capitalize()
        places = dict(LAGOS_AREAS)
        for i, k in places.iteritems():
            if k == c:
                area = super(CenterManager, self).get_queryset().filter(area__icontains=i)
                return area

class Center(models.Model):
    user = models.ForeignKey(User)
    price = models.IntegerField()
    capacity = models.IntegerField()
    owner = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(blank=True, null=False, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    location = models.SmallIntegerField(choices=ALL_LOCATIONS, default=25)
    address = models.CharField(max_length=100, blank=False, default='')
    area = models.SmallIntegerField(choices=ALL_AREA, default=33)
    active = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    is_available = models.BooleanField(default=True)
    objects = CenterManager()

    def state_name(self):
        """Returns the state name
        """
        return dict(NIGERIAN_LOCATIONS).get(self.location)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/center/{}/" .format(self.id)

    def get_area_name(self):
        """Returns the area name
        """
        return dict(LAGOS_AREAS).get(self.area)

class CenterPhoto(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    center = models.ForeignKey(Center, null=True, blank=True)
    image = CloudinaryField(
        resource_type='image',
        type='upload',
        blank=True,
        default="http://res.cloudinary.com/theeventdiary/image/upload/v1483614044/lg_m8sc17.jpg",
    )

    """ Informative name for mode """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.center, public_id) or u''


class Booking(models.Model):
    user = models.ForeignKey(User)
    center = models.ForeignKey(Center)
    booking_start_date = models.DateField()
    booking_end_date = models.DateField()
    customer_name = models.CharField(max_length=100, null=False, blank=False)
    customer_email = models.EmailField(max_length=70, blank=True, null=True,)
    phone_number = PhoneNumberField()
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
        
