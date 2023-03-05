from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from .models import Medicament, Tranzactie
from .models import User
from .forms import MedicamentForm, UserForm, TranzactieForm
from django.contrib import messages  # Le folosim pentru a arunca erori, etc
from django.contrib.auth.decorators import login_required  # Le folosim pentru a arunca erori, etc
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, \
    logout  # Pt login, logoout useri; metode deja implmenetate de Django


def loginPage(request):
    page = 'login'
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
        # autheticate-returneaza eroare daca nu exista cest user sau User ul dorit in caz contrar
    context = {
        'page':page
    }
    return render(request, 'login_register.html', context)


def logoutUser(request):
    logout(request)  # User ul curent se delogheaza
    return redirect('home')

def registerUser(request):
    page='register'
    form = UserCreationForm()#Formularul initial, cu datele(in inputuri) necompletate
    if request.method == "POST":
        form = UserCreationForm(request.POST)  # NOUL FORMULAR, CU DATELE(din input) completate
        if form.is_valid():
            user = form.save(commit=False) #Daca vreau eventual sa fac validari
            user.save()
            login(request, user) #Can ne facem cont, NE si logam automat!
            return redirect('home')
        else:
            messages.error(request, "A aparut o eroare in timpul inregistrarii!")
    return render(request, 'login_register.html', {'form':form})


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
# Ca si keyword argument, ii dam link catre pagina de login, PENTRU A SE LOGA NEAPARAT!!!
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
    if request.user.is_superuser:  # E admin, ARE DREPTUL de a modifica medicamente din baza de date
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
    medicament = Medicament.objects.get(id=pk)
    if request.method == "POST":
        medicament.delete()
        return redirect('medicamente')
    return render(request, 'delete.html', {'obj': medicament})


def pageClienti(request):
    clienti = User.objects.all().values()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if q != None:
        clienti = User.objects.filter(Q(first_name__contains=q) |
                                      Q(last_name__contains=q) |
                                      Q(email__contains=q))

    context = {
        'clienti': clienti
    }
    return render(request, 'clienti.html', context)


def createClient(request):
    form = UserForm()
    context = {'form': form}
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clienti')  # Daca se face submitul, merge inapoi LA PAGINA DE INCEPUT!
            # La parametru, in loc de path ul de inceput putem da 'home' FIINDCA am folosit name='home' in path(...)
    return render(request, 'clienti_form.html', context)  # Daca form ul nu e valid, ne intoarcem si introducem iar date


def updateClient(request, pk):
    client = User.objects.get(id=pk)  # Obtinem clientul curent
    form = UserForm(instance=client)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=client)
        if form.is_valid():
            form.save()  # Salvam noua valoare in baza de date
            return redirect('clienti')
    context = {'form': form,
               'client': client}
    return render(request, 'medicament_form.html', context)


def deleteClient(request, pk):
    client = User.objects.get(id=pk)
    if request.method == "POST":
        client.delete()
        return redirect('clienti')
    return render(request, 'delete.html', {'obj': client})


def pageTranzactii(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    tranzactii = Tranzactie.objects.filter(client=request.user.pk)  # tranzactiile utilizatorului curent
    if q is not None:
        tranzactii = tranzactii.filter(Q(client__username__contains=q) |
                                       Q(medicament__nume__contains=q))
    else:
        ' '
    context = {
        'tranzactii': tranzactii
    }
    return render(request, 'tranzactii.html', context)


def createTranzactie(request, pk):
    form = TranzactieForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = TranzactieForm(request.POST)
        try:
            if form.is_valid():
                tranzactie = form.save(commit=False)  # Obtinem tranzactia, care inca nu e salvata!!!
                if tranzactie.client.id != request.user.id:
                    messages.error(request,
                                   'Client ul pentru care incercati sa adaugati tranzactia nu este dumneavoastra!')
                else:
                    tranzactie.save()
                    return redirect('tranzactii')
        except:
            return redirect('tranzactii_form.html')

    return render(request, 'tranzactii_form.html', context)


def updateTranzactie(request, pk):
    tranzactie = Tranzactie.objects.get(id=pk)
    form = TranzactieForm(instance=tranzactie)
    context = {
        'form': form
    }
    if request.method == "POST":
        form = TranzactieForm(request.POST, instance=tranzactie)
        try:
            if form.is_valid():
                tranzactie = form.save(commit=False)  # Obtinem tranzactia, care inca nu e salvata!!!
                if tranzactie.client.id != request.user.id:
                    messages.error(request,
                                   'Client ul pentru care incercati sa adaugati tranzactia nu este dumneavoastra!')
                else:
                    form.save(commit=True)
                    return redirect('tranzactii')
        except Exception:
            return redirect('tranzactii_form.html')
    return render(request, 'tranzactii_form.html', context)

def deleteTranzactie(request, pk):
    tranzactie = Tranzactie.objects.get(id=pk)
    if request.method == "POST":
        tranzactie.delete()
        return redirect('tranzactii')
    return render(request, 'delete.html', {'obj': tranzactie})