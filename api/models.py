from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import  datetime as datetime

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not password:
            raise ValueError("Le mot de passe est obligatoire pour un superuser")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    telephone = models.CharField(max_length=17)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telephone']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
# Model pour type de Depense
class TypeDepense(models.Model):
    nom = models.CharField(max_length=255, unique=True, verbose_name="Nom du type de depense")

    def __str__(self):
        return self.nom

# Model pour les Depenses
class Depense(models.Model):
    MOYENS_PAIEMENT = [
        ('OR', 'Orange Money'),
        ('WAV', 'Wave'),
        ("FM", 'Free Money'),
        ('CB', 'Carte Bancaire'),
        ('ESP', 'Espèces'),
        ('CHQ', 'Chèque'),
        ('VIR', 'Virement'),
    ]
    nom = models.CharField(max_length=255, verbose_name="Nom de la dépense")
    montant = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Montant de la dépense")
    type_depense = models.ForeignKey(TypeDepense, on_delete=models.CASCADE, null=True, blank=True, verbose_name="type de dépense")
    moyen_paiement = models.CharField(max_length=10, choices=MOYENS_PAIEMENT, null=True, verbose_name="Moyen de paiement")
    piece_justificative = models.FileField(upload_to='justificatifs/', null=True, blank=True, verbose_name="Pièce justificative")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de creation")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Utlisateur")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Date de modification")
    
