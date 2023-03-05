from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Medicament
from .models import User
from .forms import MedicamentForm
from django.contrib import messages  # Le folosim pentru a arunca erori, etc
from django.contrib.auth.decorators import login_required  # Le folosim pentru a arunca erori, etc
from django.db.models import Q
from django.contrib.auth import authenticate, login, \
    logout  # Pt login, logoout useri; metode deja implmenetate de Django


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')  # Asa obtinem username ul
        password = request.POST.get('password')  # Asa obtinem parola
        try:
            client = User.objects.get(username=username)  # Daca nu exista nici un user, se arunca eroare
        except Exception:
            messages.error(request, "Nu exista nici un astfel de client!")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Dupa ce user ul se conecteaza, acesta merge la pagina de inceput
        else:
            messages.error(request, "Numele username ului sau parola sunt incorecte!")
        # autheticate-retunreaza eroare daca nu exista cest user sau User ul dorit in caz contrar
    context = {

    }
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)  # User ul curent se delogheaza
    return redirect('home')


def home(request):
    template = loader.get_template('home.html')
    medicamente = Medicament.objects.all().values()
    context = {'meds': medicamente}
    return render(request, 'home.html', context)


# def medicament(request, pk):  # URL DInamic; Numele parametrului "pk" trebuie sa fie acleasi cu cel din lista de
# parametrii medicament = Medicament.objects.get(id=pk) # for searched_medicament in medicamente: #     if
# searched_medicament['id'] == int(pk): #         medicament = searched_medicament context = { 'med': medicament }
# return render(request, 'medicamente.html', context) # Acest view NU se va apela  pentru pagina mare (medicament,
# nu este request catre ea), ci pentru paginile speciifce # pentru fiecare medicament Noi, pe o pafina specifica unui
# medicament, vrem sa afisam numele sau


def pageMedicamente(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ' '
    medicamente = Medicament.objects.all().values()
    if request.GET.get('q') != None:
        medicamente = Medicament.objects.filter(Q(nume__contains=q) |
                                                Q(producator__contains=q)).values()
    else:
        ''
    context = {
        'medicamente': medicamente
    }
    return render(request, 'medicamente.html', context)


# Vrem sa putem aduaga medicamente DOAR daca user ul e autentificat(presupunem ca e un admin)
#Ca si keyword argument, ii dam link catre pagina de login, PENTRU A SE LOGA NEAPARAT!!!
@login_required(login_url='login')
def createMedicament(request):
    if request.user.is_superuser:
        form = MedicamentForm()
        context = {'form': form}
        if request.method == "POST":
            # print(request.POST) #Datele trimise de utilizator le afisam in terminal, sa vedem ca merge
            form = MedicamentForm(request.POST)
            if form.is_valid():  # Datele sunt corecte(validate, tipul e corect pentru fiecare; toate restrictiile sunt
                # verificate!)
                form.save()
                return redirect('medicamente')  # Daca se face submitul, merge inapoi LA PAGINA DE INCEPUT!
                # La parametru, in loc de path ul de inceput putem da 'home' FIINDCA am folosit name='home' in path(...)
        return render(request, 'medicament_form.html', context)
    else:
        return redirect('home')

@login_required(login_url='login')
def updateMedicament(request, pk: str):
    if request.user.is_superuser: #E admin, ARE DREPTUL de a modifica medicamente din baza de date
        medicament = Medicament.objects.get(id=pk)
        form = MedicamentForm(instance=medicament)
        if request.method == 'POST':
            form = MedicamentForm(request.POST, instance=medicament)
            if form.is_valid():
                form.save()  # Salvam noua valoare in baza de date
                return redirect('medicamente')
        context = {'form': form,
                   'medicament': medicament}
        return render(request, 'medicament_form.html', context)
    else:
        return redirect('home')

@login_required(login_url='login')
def deleteMedicament(request, pk):
    if request.user.is_superuser: #E admin, ARE DREPTUL de a sterge medicamente din baza de date
        medicament = Medicament.objects.get(id=pk)
        if request.method == "POST":
            medicament.delete()
            return redirect('medicamente')
        return render(request, 'delete.html', {'obj': medicament})
    else:
        return redirect('home')
