from django.urls import path
from . import views

app_name = 'produkty'  # Dodaj to, aby ustawić namespace dla aplikacji

urlpatterns = [
    path('', views.home, name='home'),
    path('import/', views.import_excel, name='import_excel'),
    path('test/', views.test_template, name='test_template'),
    path('sprzedaz/', views.sprzedaz, name='sprzedaz'),
    path('sprzedaz/sukces/', views.sprzedaz_sukces, name='sprzedaz_sukces'),
    path('podsumowanie/', views.podsumowanie_sprzedazy, name='podsumowanie_sprzedazy'),
    path('wyciagnij_liste_modeli/', views.wyciagnij_liste_modeli, name='wyciagnij_liste_modeli'),  # Nowy widok wyciągania listy modeli

  # Nowe ścieżki do widoków związanych z zadaniówkami
    path('zadaniowki/', views.lista_zadaniowek, name='lista_zadaniowek'),
    path('zadaniowki/<int:task_id>/', views.szczegoly_zadaniowki, name='szczegoly_zadaniowki'),
    path('zadaniowka/<int:task_id>/postepy/', views.postepy_zadaniowki, name='postepy_zadaniowki'),
    path('ekspozycja/<int:grupa_id>/', views.ekspozycja_form, name='ekspozycja_form'),
    path('ekspozycja-summary/', views.ekspozycja_summary, name='ekspozycja_summary'),
]