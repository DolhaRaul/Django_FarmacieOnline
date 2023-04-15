from django.forms import ModelForm
from .models import Medicament, Tranzactie
from .models import User


class MedicamentForm(ModelForm):
    class Meta:
        model = Medicament
        fields = '__all__'


class UserForm(ModelForm):
    class Meta:
        model = User
        ordering = ['first_name', 'last_name']
        fields = ['username', 'password', 'first_name', 'last_name', 'email']


class TranzactieForm(ModelForm):
    class Meta:
        model = Tranzactie
        ordering = ['medicament.nume']
        fields = '__all__'
