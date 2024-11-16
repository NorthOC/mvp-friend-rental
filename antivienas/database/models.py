from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.files.storage import FileSystemStorage

from PIL import Image
import random
import os
import datetime as dt

NO_AVATAR_IMG_PATH = "/user-no-avatar.png"

class CityOfService(models.TextChoices):
    """ Susitikimo vietos """
    VILNIUS =           "Vilnius"
    KAUNAS =            "Kaunas"
    KLAIPEDA =          "Klaipėda"
    SIAULIAI =          "Šiauliai"
    PANEVEZYS =         "Panevėžys"
    AKMENE =            "Akmenė"
    ALYTUS =            "Alytus"
    ANYKSCIAI =         "Anykščiai"
    BIRSTONAS =         "Birštonas"
    BIRZAI =            "Biržai"
    DRUSKININKAI =      "Druskininkai"
    ELEKTRENAI =        "Elektrėnai"
    GARGZDAI =          "Gargždai"
    IGNALINA =          "Ignalina"
    JONAVA =            "Jonava"
    JONISKIS =          "Joniškis"
    JURBARKAS =         "Jurbarkas"
    KAISIADORYS =       "Kaišiadorys"
    KALVARIJA =         "Kalvarija"
    KAZLU_RUDA =        "Kazlų Rūda"
    KEDAINIAI =         "Kėdainiai"
    KELME =             "Kelmė"
    KREKENAVA =         "Krekenava"
    KRETINGA =          "Kretinga"
    KUPISKIS =          "Kupiškis"
    KURSENAI =          "Kuršėnai"
    LAZDIJAI =          "Lazdijai"
    LENTVARIS =         "Lentvaris"
    MARIJAMPOLE =       "Marijampolė"
    MAZEIKIAI =         "Mažeikiai"
    MOLETAI =           "Molėtai"
    NAUJOJI_AKMENE =    "Naujoji Akmenė"
    NEMENCINE =         "Nemenčinė"
    NERINGA =           "Neringa"
    PABRADE =           "Pabradė"
    PAGEGIAI =          "Pagėgiai"
    PAKRUOJIS =         "Pakruojis"
    PALANGA =           "Palanga"
    PASVALYS =          "Pasvalys"
    PLUNGE =            "Plungė"
    PRIENAI =           "Prienai"
    RADVILISKIS =       "Radviliškis"
    RASEINIAI =         "Raseiniai"
    RIETAVAS =          "Rietavas"
    ROKISKIS =          "Rokiškis"
    SAKIAI =            "Šakiai"
    SALCININKAI =       "Šalčininkai"
    SILALE =            "Šilalė"
    SILUTE =            "Šilutė"
    SIRVINTOS =         "Širvintos"
    SKUODAS =           "Skuodas"
    SVENCIONYS =        "Švenčionys"
    TAURAGE =           "Tauragė"
    TELSIAI =           "Telšiai"
    TRAKAI =            "Trakai"
    UKMERGE =           "Ukmergė"
    UTENA =             "Utena"
    VARENA =            "Varėna"
    VIEVIS =            "Vievis"
    VILKAVISKIS =       "Vilkaviškis"
    VISAGINAS =         "Visaginas"
    ZARASAI =           "Zarasai"

class Genders(models.TextChoices):
    VYRAS = "Vyras"
    MOTERIS = "Moteris"

class OrderStatuses(models.IntegerChoices):
    INITIATED   = 1, 'Initiated'     # sukuriamas užsakymas
    CONFIRMED   = 2, 'Confirmed'     # patvirtinamas užsakymas
    PAID        = 3, "Paid"          # užsakymas apmokėtas ir laukia 4 sk. kodo iš draugo
    COMPLETE    = 4, "Complete"      # įvykdytas užsakymas
    CANCELLED   = 5, 'Cancelled'     # atšauktas užsakymas
    ABANDONED   = 6, "Abandoned"     # apleistas užsakymas
    DISPUTED    = 7, "Disputed"      # skundžiamas užsakymas
    FAILED      = 8, "Failed"        # užsakymas buvo apmokėtas, bet nesulaukė kodo
    
class MeetingHours(models.TextChoices):
    DEVYNIOS ="09:00","09:00"
    DEVYNIOS_TRISDESIMT ="09:30","09:30"
    DESIMT="10:00","10:00"
    DESIMT_TRISDESIMT="10:30","10:30"
    VIENUOLIKA="11:00","11:00"
    VIENUOLIKA_TRISDESIMT="11:30","11:30"
    DVYLIKA="12:00","12:00"
    DVYLIKA_TRISDESIMT="12:30","12:30"
    TRYLIKA="13:00","13:00"
    TRYLIKA_TRISDESIMT="13:30","13:30"
    KETURIOLIKA="14:00","14:00"
    KETURIOLIKA_TRISDESIMT="14:30","14:30"
    PENKIOLIKA="15:00","15:00"
    PENKIOLIKA_TRISDESIMT="15:30","15:30"
    SESIOLIKA="16:00","16:00"
    SESIOLIKA_TRISDESIMT="16:30","16:30"
    SEPTYNIOLIKA="17:00","17:00"
    SEPTYNIOLIKA_TRISDESIMT="17:30","17:30"
    ASTUONIOLIKA="18:00","18:00"
    ASTUONIOLIKA_TRISDESIMT="18:30","18:30"
    DEVYNIOLIKA="19:00","19:00"
    DEVYNIOLIKA_TRISDESIMT="19:30","19:30"
    DVIDESIMT="20:00","20:00"

class ProfileTypes(models.TextChoices):
    # vartotojų tipai (vartotojas arba draugas)
    USER =      "User"
    FRIEND =    "Friend"

class InterestColorHexes(models.TextChoices):
    GRAY =      "#D9D9D9", "Gray"
    RED =       "#F6C4C4", "Red"
    BLUE =      "#B2D8EE", "Blue"
    GREEN =     "#B8F2C1", "Green"
    PURPLE =    "#F1B8F2", "Purple"
    YELLOW =    "#F6EAA5", "Yellow"

class EducationChoices(models.TextChoices):
    PAGRINDINIS = "Pagrindinis"
    VIDURINIS = "Vidurinis"
    AUKSTASIS = "Aukštasis"
    AUKSTESNYSIS = "Aukštesnysis"
    PRADINIS = "Pradinis"

class LvlOfExperience(models.IntegerChoices):
    NEWBIE      = 1, "Naujokas"         # pradinis lygis
    EXPERIENCED = 2, "Patyręs"          # po 2 sėkmingų užsakymų
    EXPERT      = 3, "Ekspertas"        # po 10 sėkmingų užsakymų
    VETERAN     = 4, "Veteranas"        # po 50 sėkmingų užsakymų

class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
    
    def _save(self, name, content):
        self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

def user_img_upload_path(instance, filename):
    return os.path.join(f"user_uploads/user_{instance.user.pk}", filename)

class User(AbstractUser):
    """
    Vartotojo modelis
    """
        
    # ID verifikavimui
    is_id_verified =    models.BooleanField(default=False)
    id_img =            models.ImageField(upload_to=user_img_upload_path, blank=True, null=True)

    # vartotojo duomenys
    profile_type =      models.CharField(max_length=6, choices=ProfileTypes, default=ProfileTypes.USER)
    birthday =          models.DateField(default=dt.date(1998,5,14))
    city =              models.CharField(max_length=15,choices=CityOfService,null=True,blank=True)
    job =               models.CharField(max_length=40, blank=True)
    description =       models.TextField(max_length=2500, blank=True)
    gender =            models.CharField(max_length=10, choices=Genders, blank=True, null=True)
    education =         models.CharField(max_length=15, choices=EducationChoices, blank=True, null=True)
    
    selected_avatar =  models.SmallIntegerField(default=0)

    interest_one =      models.CharField(max_length=50, blank=True)
    interest_two =      models.CharField(max_length=50, blank=True)
    interest_three =    models.CharField(max_length=50, blank=True)
    interest_four =     models.CharField(max_length=50, blank=True)

    interest_color_one =    models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_two =    models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_three =  models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_four =   models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)

    orders_completed =  models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.email)
    
    @property
    def age(self):
        return int((dt.datetime.now().date() - self.birthday).days / 365.25)
    
    @property
    def avatar(self):
        return UserProfilePicture.avatar(self)

class FriendSetting(models.Model):
    """
    Vartotojai, kurie tampa draugais, įgyja papildomų parametrų
    """
    friend =            models.OneToOneField(User, related_name="friend", on_delete=models.CASCADE, primary_key=True)
    # 20% fee
    price_per_hour =    models.PositiveIntegerField(default=0)
    is_public =         models.BooleanField(default=False)
    
    account_number =            models.CharField(max_length=20, blank=True)
    account_holder_details =    models.CharField(max_length=200, blank=True)
    
    level =     models.SmallIntegerField(choices=LvlOfExperience, default=LvlOfExperience.NEWBIE)
    created =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.friend.email)

class UserProfilePicture(models.Model):
    """User profile pictures"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=user_img_upload_path)
    is_avatar = models.BooleanField(default=False)
    created =   models.DateTimeField(auto_now_add=True)
    
    @classmethod
    def avatar(cls, user):
        """returns a users selected avatar"""

        try:
            image = UserProfilePicture.objects.filter(user=user, is_avatar=True)[0]
        except:
            return None
        return image
    
    def rebalance_avatar(self, *args, **kwargs):
        """after deleting an image, makes sure that there's an avatar image"""

        user_images = UserProfilePicture.objects.filter(user=self.user).order_by("created")

        if user_images.count() == 0:
            return

        avatar = user_images.filter(is_avatar=True).first()

        if not avatar:
            image = user_images.first()
            image.is_avatar = True
            image.save()
    
    @classmethod
    def set_avatar(cls, user, avatar_id):
        """sets the users preferred avatar"""
        user_images = UserProfilePicture.objects.filter(user=user).order_by("created")
        user_images.update(is_avatar=False)

        if user_images.count() == 0:
            return

        if user_images.count() > avatar_id:
            image = user_images[avatar_id]
            image.is_avatar = True
            image.save()


    def delete(self, *args, **kwargs):
        super().delete()
        self.rebalance_avatar()

    def crop_and_save(self, *args, **kwargs):
        super().save()

        # delete if this is 4th picture uploaded
        images = UserProfilePicture.objects.filter(user=self.user).order_by('created')

        if images.count() > 3:
            images[0].delete()
        
        if images.count() == 1:
            avatar = images.first()
            avatar.is_avatar = True
            avatar.save()
                  

        img_path = self.image.path
        img = Image.open(img_path)
        width, height = img.size  # Get dimensions

        # check which one is smaller
        if height < width:
            # make square by cutting off equal amounts left and right
            left = (width - height) / 2
            right = (width + height) / 2
            top = 0
            bottom = height
            img = img.crop((left, top, right, bottom))

        elif width < height:
            # make square by cutting off bottom
            left = 0
            right = width
            top = 0
            bottom = width
            img = img.crop((left, top, right, bottom))

        if width > 400 or height > 400:
            img.thumbnail((400, 400))

        img.save(img_path)

class Order(models.Model):
    """
    Susitikimo užsakymas
    """

    user =          models.ForeignKey(User, on_delete=models.DO_NOTHING)
    friend =        models.ForeignKey(FriendSetting, on_delete=models.DO_NOTHING)
    meeting_day =   models.DateField()
    meeting_hour =  models.CharField(max_length=6, choices=MeetingHours)
    no_of_hours =   models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(72)])
    meeting_place = models.CharField(max_length=300)
    comment =       models.TextField(max_length=1500)
    cancel_reason = models.TextField(max_length=300, blank=True)
    total_price =   models.PositiveIntegerField(validators=[MinValueValidator(0)])

    order_status =          models.SmallIntegerField(choices=OrderStatuses, default=OrderStatuses.INITIATED)
    confirmation_code =     models.SmallIntegerField(default=random.randint(1000,9999))
    is_disputable =         models.BooleanField(default=True)
    created =               models.DateTimeField(auto_now_add=True)

    @property
    def lithuanian_date(self):
        MONTHS = ["Sausio",
        "Vasario",
        "Kovo",
        "Balandžio",
        "Gegužės",
        "Birželio",
        "Liepos",
        "Rugpjūčio",
        "Rugsėjo",
        "Spalio",
        "Lapkričio",
        "Gruodžio"]
    
        return f"{MONTHS[self.meeting_day.month-1]} {self.meeting_day.day} d. {self.meeting_day.year}m."
    
class Dispute(models.Model):
    """
    Skundų lentelė
    """
    order =             models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    user_comment =      models.TextField(max_length=2000, blank=True)
    friend_comment =    models.TextField(max_length=2000, blank=True)
    is_solved =         models.BooleanField(default=False)
    in_review =         models.BooleanField(default=False)
    created =           models.DateTimeField(auto_now_add=True)