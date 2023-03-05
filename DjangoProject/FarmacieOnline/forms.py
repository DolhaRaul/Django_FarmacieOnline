from django.forms import ModelForm
from .models import Medicament

class MedicamentForm(ModelForm):
    class Meta:
        model = Medicament
        fields='__all__'
