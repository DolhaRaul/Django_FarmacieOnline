from django.urls import path
from . import views

urlpatterns = [path('', views.home, name='home'),
               #path('medicament_page/<str:pk>', views.medicament, name='medicament'),
               # Creem un URL dinamic-specific paginii fie med,
               path('medicamente/', views.pageMedicamente, name='medicamente'),
               path('create-medicament/', views.createMedicament, name='create-medicament'),
               path('update-medicament/<int:pk>', views.updateMedicament, name='update-medicament'),
               path('delete-medicament/<int:pk>', views.deleteMedicament, name='delete-medicament'),
               path('login/', views.loginPage, name='login'),
               path('logout/', views.logoutUser, name='logout'),
               path('register/', views.registerUser, name='register'),
               path('clienti/', views.pageClienti, name='clienti'),
               path('create-client/', views.createClient, name='create-client'),
               path('update-client/<int:pk>', views.updateClient, name='update-client'),
               path('delete-client/<int:pk>', views.deleteClient, name='delete-client'),
               path('tranzactii/', views.pageTranzactii, name='tranzactii'),
               path('create-tranzactie/<int:pk>', views.createTranzactie, name='create-tranzactie'),
               path('update-tranzactie/<int:pk>', views.updateTranzactie, name='update-tranzactie'),
               path('delete-tranzactie/<int:pk>', views.deleteTranzactie, name='delete-tranzactie')
               ]
# Acel name='medicament' ne permite sa inluim acel path cu 'medicament'; Asta e util pt ca se poate ca acel path
# Sa se modifice in diverse fisiere HTML(unde l am dat ca referinta), ci pur si simplu dam acel nume cu care
# identificam acest path; vezi in fisierul 'home.html' pt a vedea cum se foloseste
# In Python Django Course: 1:03:00
