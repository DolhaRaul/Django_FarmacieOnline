import datetime

import django.utils.timezone
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Medicament(models.Model):
    id = models.BigAutoField(primary_key=True)
    nume = models.CharField(max_length=50)
    producator = models.CharField(max_length=50)
    pret = models.FloatField(null=True, blank=True)
    necesita_reteta = models.BooleanField(default=False)

    class Meta:
        ordering = ['-nume']  # CLASA ASTA AJUTA PENTRU A SORTA ITEMELE DIN BAZA DE DATE DUPA ANUMITE CAMPURI ALE EI!!!

    def __str__(self):
        return f'{self.nume}'


class Tranzactie(models.Model):
    id = models.BigAutoField(primary_key=True)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    numar_bucati = models.IntegerField()
    data_tranzactie = models.DateTimeField(auto_now_add=django.utils.timezone.now)

    def __str__(self):
        return f'Tranzactie facuta de clientul de id {self.client}, ' \
               f'ce doreste medicamente de id {self.medicament}'
