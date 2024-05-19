from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime as dt
from django.core.files.storage import FileSystemStorage

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
    NUOTOLINIU =        "Nuotoliniu"

class Genders(models.TextChoices):
    VYRAS = "Vyras"
    MOTERIS = "Moteris"

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name
    
    def _save(self, name, content):
        self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

def upload_img_one(instance, filename):
    extension = filename.split(".")[-1]
    return f"user_uploads/user_{instance.pk}/1.{extension}"

def user_img_upload_path(instance, filename):
    return f"user_uploads/user_{instance.pk}/{filename}"

class User(AbstractUser):
    """
    Vartotojo modelis
    """
    class ProfileTypes(models.TextChoices):
        # vartotojų tipai (vartotojas arba draugas)
        USER =      "User"
        FRIEND =    "Friend"
    
    class PersonalityTypes(models.TextChoices):
        INTRAVERT =     "Intravert"
        EKSTRAVERT =    "Ekstravert"

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

        
    # ID verifikavimui
    is_id_verified =    models.BooleanField(default=False)
    id_img =            models.ImageField(upload_to=user_img_upload_path, blank=True, null=True)

    # vartotojo duomenys
    profile_type =      models.CharField(max_length=6, choices=ProfileTypes, default=ProfileTypes.USER)
    birthday =          models.DateField()
    city =              models.CharField(max_length=15,choices=CityOfService,null=True,blank=True)
    job =               models.CharField(max_length=40, blank=True)
    description =       models.TextField(max_length=5000, blank=True)
    personality_type =  models.CharField(max_length=10, choices=PersonalityTypes, null=True, blank=True)
    gender =            models.CharField(max_length=10, choices=Genders, blank=True, null=True)
    education =         models.CharField(max_length=15, choices=EducationChoices, blank=True, null=True)
    height_cm =         models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(300)])

    img_one =           models.ImageField(upload_to=upload_img_one, default="/user-no-avatar.png", storage=OverwriteStorage())
    img_two =           models.ImageField(upload_to=user_img_upload_path, blank=True, null=True)
    img_three =         models.ImageField(upload_to=user_img_upload_path, blank=True, null=True)

    interest_one =      models.CharField(max_length=50, blank=True)
    interest_two =      models.CharField(max_length=50, blank=True)
    interest_three =    models.CharField(max_length=50, blank=True)
    interest_four =     models.CharField(max_length=50, blank=True)

    interest_color_one =    models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_two =    models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_three =  models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_four =   models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)

    def __str__(self):
        return str(self.email)
    
    @property
    def age(self):
        return int((dt.datetime.now().date() - self.birthday).days / 365.25)

class FriendSetting(models.Model):
    """
    Vartotojai, kurie tampa draugais, įgyja papildomų parametrų
    """
    friend =            models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # 20% (17% + 3% už pavedimą)
    price_per_hour =    models.PositiveIntegerField(default=0)
    orders_completed =  models.PositiveIntegerField(default=0)
    is_public =         models.BooleanField(default=False)
    
    account_number =            models.CharField(max_length=20, blank=True)
    account_holder_details =    models.CharField(max_length=200, blank=True)

    class LvlOfExperience(models.IntegerChoices):
        NEWBIE      = 1, "Naujokas"       # pradinis lygis
        EXPERIENCED = 2, "Patyręs"  # po 2 sėkmingų užsakymų
        VETERAN     = 3, "Veteranas"      # po 10 sėkmingų užsakymų
        EXPERT      = 4, "Ekspertas"       # specialus lygis psichologams
    
    level =     models.SmallIntegerField(choices=LvlOfExperience, default=LvlOfExperience.NEWBIE)
    created =   models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.friend.email)

class Order(models.Model):
    """
    Susitikimo užsakymas
    """
    class OrderStatuses(models.IntegerChoices):
        INITIATED   = 1, 'Initiated'     # sukuriamas užsakymas
        CONFIRMED   = 2, 'Confirmed'     # patvirtinamas užsakymas
        COMPLETE    = 3, "Complete"      # įvykdytas užsakymas
        CANCELLED   = 4, 'Cancelled'     # atšauktas užsakymas
        ABANDONED   = 5, "Abandoned"     # apleistas užsakymas
        DISPUTED    = 6, "Disputed"      # skundžiamas užsakymas
    
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

    user =          models.ForeignKey(User, on_delete=models.DO_NOTHING)
    friend =        models.ForeignKey(FriendSetting, on_delete=models.DO_NOTHING)
    meeting_day =   models.DateField(validators=[MinValueValidator(dt.date.today() + dt.timedelta(days=1))])
    meeting_hour =  models.CharField(max_length=6, choices=MeetingHours)
    no_of_hours =   models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(72)])
    meeting_place = models.CharField(max_length=300)
    comment =       models.TextField(max_length=1500)
    cancel_reason = models.TextField(max_length=300, blank=True)
    total_price =   models.PositiveIntegerField(validators=[MinValueValidator(0)])

    order_status =          models.SmallIntegerField(choices=OrderStatuses, default=OrderStatuses.INITIATED)
    created =               models.DateTimeField(auto_now_add=True)


class Dispute(models.Model):
    """
    Skundų lentelė
    """
    order =             models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    user_comment =      models.TextField(max_length=2000, blank=True, null=True)
    friend_comment =    models.TextField(max_length=2000, blank=True, null=True)
    is_solved =         models.BooleanField(default=False)
    in_review =         models.BooleanField(default=False)
    created =           models.DateTimeField(auto_now_add=True)