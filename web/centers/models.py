from cloudinary.models import CloudinaryField
from hvad.models import TranslatableModel, TranslatedFields
from multiselectfield import MultiSelectField
from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import ChainedForeignKey

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_libs.models_mixins import TranslationModelMixin


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

VENUE_TYPE = (
    (1, 'Multipurpose hall'), (2, 'Garden'), (3, 'Conference centre'), (4, 'Auditorium'),
    (5, 'Field'), (6, 'Pool Side'), (7, 'Open side'), (8, 'Hotel event hall'),
    (9, 'Club hall'), (10, 'Marquee'),
)

FACILITY = [
    (1, 'Tables'), (2, 'Chairs'), (3, 'Changing Room'), (4, 'Power Supply'),
    (5, 'Parking Space'), (6, 'Air Conditioner'), (7, 'Television'), (8, 'Security'),
    (9, 'Sound System'), (10, 'Projector'), (9, 'Pulpit'), (10, 'Writing Board'),
    (9, 'Rest Room'), (10, 'Fan'), (9, 'Stage'), (10, 'Staging Light'),
    (9, 'Cold Room'), (10, 'Traffic controllers')
]

ALL_LOCATIONS = NIGERIAN_LOCATIONS
ALL_AREA = LAGOS_AREAS

def valid_pct(val):
    if val.endswith("%"):
       return float(val[:-1])/100
    else:
       try:
          return float(val)
       except ValueError:          
          raise ValidationError(
              _('%(value)s is not a valid pct'),
                params={'value': value},
           )

class State(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)

    def __unicode__(self):
        return u'%s' % self.name


class LocalGovArea(models.Model):
    state = models.ForeignKey(State, related_name="state_lga")
    name = models.CharField(max_length=100, null=False, blank=False)

    def __unicode__(self):
        return u'%s' % self.name


class CenterManager(models.Manager):

    def get_lga_name(self, area):
        """Returns the area name
        """
        area_query = str(area).capitalize()
        places = LocalGovArea.objects.all()
        area = places.filter(name=area_query)
        return area


class Center(models.Model):
    user = models.ForeignKey(User)
    price = models.IntegerField()
    theatre_arrangement = models.IntegerField()
    banquet_arrangement = models.IntegerField()
    owner = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(blank=True, default='')
    slug = models.SlugField(blank=True, null=False, unique=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    state = models.ForeignKey(State, related_name="center_state")
    lga = ChainedForeignKey(LocalGovArea, chained_field="state", chained_model_field="state")
    address = models.CharField(max_length=100, blank=False, default='')
    center_type = MultiSelectField(choices=VENUE_TYPE)
    facility = MultiSelectField(choices=FACILITY)
    policy = models.TextField(blank=True, default='')
    active = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_last_modified = models.DateField(auto_now=True)
    commission = models.CharField(max_length=10, validators=[valid_pct])
    is_available = models.BooleanField(default=True)
    objects = CenterManager()

    def state_name(self):
        """Returns the state name
        """
        return dict(NIGERIAN_LOCATIONS).get(self.state)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/center/{}/" .format(self.id)

    def get_center_type(self):
        """Returns the list of center type
        """
        center_type_list = []
        for center_type in self.center_type:
            center_type_name = dict(VENUE_TYPE).get(int(center_type))
            center_type_list.append(center_type_name)
        return center_type_list

    def get_facility(self):
        """Returns the list of facility
        """
        facility_list = []
        for facility in self.facility:
            facility_name = dict(FACILITY).get(int(facility))
            facility_list.append(facility_name)
        return facility_list


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
        
