from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

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
    birthday =          models.DateField(null=True, blank=True)
    city =              models.CharField(max_length=15,choices=CityOfService,null=True,blank=True)
    job =               models.CharField(max_length=40, null=True, blank=True)
    description =       models.TextField(max_length=5000, null=True, blank=True)
    personality_type =  models.CharField(max_length=10, choices=PersonalityTypes, null=True, blank=True)
    gender =            models.CharField(max_length=10, choices=Genders, blank=True, null=True)
    education =         models.CharField(max_length=15, choices=EducationChoices, blank=True, null=True)
    height_cm =         models.PositiveIntegerField(blank=True, null=True, validators=[MinValueValidator(0), MaxValueValidator(300)])

    img_one =           models.ImageField(upload_to=user_img_upload_path, blank=True, null=True)
    img_two =           models.ImageField(upload_to=user_img_upload_path, blank=True, null=True)
    img_three =         models.ImageField(upload_to=user_img_upload_path, blank=True, null=True)

    interest_one =      models.CharField(max_length=50, blank=True, null=True)
    interest_two =      models.CharField(max_length=50, blank=True, null=True)
    interest_three =    models.CharField(max_length=50, blank=True, null=True)
    interest_four =     models.CharField(max_length=50, blank=True, null=True)

    interest_color_one =    models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_two =    models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_three =  models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)
    interest_color_four =   models.CharField(max_length=7, choices=InterestColorHexes, default=InterestColorHexes.GRAY)

    def __str__(self):
        return str(self.email)
    
    @property
    def age(self):
        return int((datetime.now().date() - self.birthday).days / 365.25)
    
    @property
    def short_description(self):
        return self.description

class FriendSetting(models.Model):
    """
    Vartotojai, kurie tampa draugais, įgyja papildomų parametrų
    """
    friend =            models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    price_per_hour =    models.PositiveIntegerField(default=0)
    orders_completed =  models.PositiveIntegerField(default=0)
    is_public =         models.BooleanField(default=False)
    
    account_number =            models.CharField(max_length=20, blank=True, null=True)
    account_holder_details =    models.CharField(max_length=200, blank=True, null=True)

    class LvlOfExperience(models.IntegerChoices):
        NEWBIE      = 1, "Naujokas"       # pradinis lygis
        EXPERIENCED = 2, "Patyręs"  # po 2 sėkmingų užsakymų
        VETERAN     = 3, "Veteranas"      # po 10 sėkmingų užsakymų
        EXPERT      = 4, "Ekspertas"       # specialus lygis psichologams
    
    level =     models.SmallIntegerField(choices=LvlOfExperience, default=LvlOfExperience.NEWBIE)
    created =   models.DateTimeField(auto_now_add=True)

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

    user =          models.ForeignKey(User, on_delete=models.DO_NOTHING)
    friend =        models.ForeignKey(FriendSetting, on_delete=models.DO_NOTHING)
    meeting_time =  models.DateTimeField()
    no_of_hours =   models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)])
    meeting_place = models.CharField(max_length=300)
    comment =       models.TextField(max_length=1500)
    total_price =   models.DecimalField(max_digits=6, decimal_places=2)

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