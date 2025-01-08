from django.contrib import admin
from .models import Produkt, Sprzedaz, Task, GrupaProduktowa, Marka, Ekspozycja
from .forms import TaskForm  # Importujemy formularz

# Rejestracja modelu Produkt w panelu admina
admin.site.register(Produkt)

# Rejestracja modelu Sprzedaz w panelu admina
admin.site.register(Sprzedaz)

# Rejestracja modelu Task z niestandardowym formularzem w panelu admina
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    form = TaskForm  # Użycie niestandardowego formularza
    list_display = ('nazwa', 'data_rozpoczecia', 'data_zakonczenia', 'minimalna_liczba_sztuk', 'premia_za_minimalna_liczbe')
    search_fields = ('nazwa',)
    list_filter = ('data_rozpoczecia', 'data_zakonczenia',)
    filter_horizontal = ('produkty',)

admin.site.register(GrupaProduktowa)
admin.site.register(Marka)
admin.site.register(Ekspozycja)  # Opcjonalnie, jeśli chcesz podglądać dane ekspozycji