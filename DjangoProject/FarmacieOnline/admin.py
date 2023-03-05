from django.contrib import admin

# Register your models here.
from. models import Medicament
from. models import Tranzactie

admin.site.register(Medicament)
admin.site.register(Tranzactie)
