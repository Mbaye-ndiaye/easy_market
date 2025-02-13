from django.db import models

class TypeDepense(models.Model):
    nom = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.nom


class Depense(models.Model):
    nom = models.CharField(max_length=255)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    type_depense = models.ForeignKey(TypeDepense, on_delete=models.CASCADE, null=True, blank=True)
    moyen_paiement = models.CharField(max_length=100, default='Cash')  # Valeur par défaut
    piece_justificative = models.FileField(upload_to='depenses/', null=True, blank=True)

    def __str__(self):
        return f"{self.nom} - {self.montant} {self.type_depense.nom}"
