from django.shortcuts import render, redirect, get_object_or_404
from .models import Produkt, Sprzedaz, Task, Ekspozycja, GrupaProduktowa, Marka 
import openpyxl
from decimal import Decimal, InvalidOperation
import logging
from django.utils import timezone
from django.db.models import Sum
from collections import defaultdict
from datetime import timedelta
from rapidfuzz import fuzz, process 
import re
from django.db import models
from django.http import HttpResponse

def test_template(request):
    try:
        template = get_template('produkty/import_form.html')
        return render(request, 'produkty/import_form.html')  # Jeśli działa, to powinno pokazać poprawny szablon
    except TemplateDoesNotExist:
        return render(request, 'produkty/home.html', {'error': 'Szablon nie istnieje'})

def home(request):
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)

    sprzedaz_tygodniowa = Sprzedaz.objects.filter(data_sprzedazy__gte=start_of_week)
    sprzedaz_miesieczna = Sprzedaz.objects.filter(data_sprzedazy__gte=start_of_month)

    tygodniowa_suma = sprzedaz_tygodniowa.aggregate(Sum('produkt__stawka'))['produkt__stawka__sum'] or 0
    miesieczna_suma = sprzedaz_miesieczna.aggregate(Sum('produkt__stawka'))['produkt__stawka__sum'] or 0

    najczesciej_sprzedawane = Sprzedaz.objects.values('produkt__model').annotate(
        liczba_sztuk=Sum('liczba_sztuk')
    ).order_by('-liczba_sztuk')[:5]

    context = {
        'najczesciej_sprzedawane': najczesciej_sprzedawane,
        'tygodniowa_suma': tygodniowa_suma,
        'miesieczna_suma': miesieczna_suma,
    }

    return render(request, 'produkty/home.html', context)
# Ustaw logger
logger = logging.getLogger(__name__)

def import_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']
        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active

        for idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            grupa_towarowa, marka, model, stawka, dystrybucja, *rest = row

            # Pomijamy wiersze, w których brakuje kluczowych danych
            if not model or not dystrybucja or dystrybucja != 'TERG':
                logger.warning(f"Wiersz {idx} pominięty - brak modelu lub nieodpowiednia dystrybucja.")
                continue

            try:
                # Obsługa stawki
                if stawka is None or stawka == '':
                    stawka = Decimal(0)
                else:
                    stawka = Decimal(stawka)
            except (TypeError, InvalidOperation) as e:
                logger.error(f"Błąd konwersji stawki w wierszu {idx}: {stawka}. Ustawiono 0. Błąd: {e}")
                stawka = Decimal(0)  # Domyślna wartość

            # Dodawanie produktu z marką
            try:
                Produkt.objects.update_or_create(
                    model=model,
                    defaults={
                        'stawka': stawka,
                        'grupa_towarowa': grupa_towarowa or 'Nieznana',
                        'marka': marka or 'Nieznana'  # Dodajemy nową markę
                    }
                )
            except Exception as e:
                logger.error(f"Błąd podczas tworzenia produktu w wierszu {idx}: {e}")
        
        return render(request, 'produkty/import_success.html')

    return render(request, 'produkty/import_form.html')

logger = logging.getLogger(__name__)

def sprzedaz(request):
    if request.method == 'POST':
        # Obsługa zatwierdzenia sugestii
        if 'sugestie_zatwierdzone' in request.POST:
            data_sprzedazy = request.POST.get('data_sprzedazy')

            # Przetwarzanie modeli, które użytkownik zatwierdził
            modele = []
            for key in request.POST:
                if key.startswith('model_'):
                    model = request.POST[key].strip().upper()
                    modele.append(model)

            for model in modele:
                produkt, created = Produkt.objects.get_or_create(
                    model=model,
                    defaults={'stawka': 0, 'grupa_towarowa': 'NIEZNANA'}
                )
                Sprzedaz.objects.create(produkt=produkt, data_sprzedazy=data_sprzedazy, liczba_sztuk=1)

            return redirect('produkty:sprzedaz_sukces')

        # Obsługa wprowadzenia nowych modeli sprzedaży
        data_sprzedazy = request.POST.get('data_sprzedazy')
        modele_sprzedazy = request.POST.get('modele_sprzedazy')

        if modele_sprzedazy:
            modele = [model.strip().upper() for model in modele_sprzedazy.split('\n') if model.strip()]
        else:
            modele = []

        wszystkie_modele = Produkt.objects.values_list('model', flat=True)

        sugestie = []
        zatwierdzone_modele = []

        for model in modele:
            if model in wszystkie_modele:
                # Jeśli model istnieje w bazie, zapisz sprzedaż
                produkt = Produkt.objects.get(model=model)
                Sprzedaz.objects.create(produkt=produkt, data_sprzedazy=data_sprzedazy, liczba_sztuk=1)
                zatwierdzone_modele.append(model)
            else:
                # Jeśli model nie istnieje, znajdź najbardziej podobny model
                najlepszy_wynik = process.extractOne(model, wszystkie_modele, scorer=fuzz.ratio)
                if najlepszy_wynik and najlepszy_wynik[1] > 80:  # Próg podobieństwa, który można dostosować
                    sugestie.append((model, najlepszy_wynik[0]))
                else:
                    # Jeśli nie znaleziono dobrego dopasowania, dodaj nowy produkt z domyślną stawką 0
                    produkt, created = Produkt.objects.get_or_create(
                        model=model,
                        defaults={'stawka': 0, 'grupa_towarowa': 'NIEZNANA'}
                    )
                    Sprzedaz.objects.create(produkt=produkt, data_sprzedazy=data_sprzedazy, liczba_sztuk=1)
                    zatwierdzone_modele.append(model)

        # Jeśli są sugestie, wyświetl je w formularzu
        if sugestie:
            context = {
                'sugestie': sugestie,
                'data_sprzedazy': data_sprzedazy,
                'zatwierdzone_modele': zatwierdzone_modele,
            }
            return render(request, 'produkty/sprzedaz_sugestie.html', context)

        return redirect('produkty:sprzedaz_sukces')

    return render(request, 'produkty/sprzedaz.html')

def sprzedaz_sukces(request):
    return render(request, 'produkty/sprzedaz_sukces.html')

def podsumowanie_sprzedazy(request):
    # Pobieranie wartości filtrów z GET
    data_od = request.GET.get('data_od')
    data_do = request.GET.get('data_do')
    produkt = request.GET.get('produkt')
    marka = request.GET.get('marka')  # Dodajemy nowy parametr do filtrowania

    # Tworzenie podstawowego zapytania do modelu Sprzedaz
    sprzedaz = Sprzedaz.objects.all()

    # Filtracja na podstawie daty, jeśli daty są podane
    if data_od:
        sprzedaz = sprzedaz.filter(data_sprzedazy__gte=data_od)
    if data_do:
        sprzedaz = sprzedaz.filter(data_sprzedazy__lte=data_do)

    # Filtracja na podstawie nazwy produktu, jeśli nazwa jest podana
    if produkt:
        sprzedaz = sprzedaz.filter(produkt__model__icontains=produkt)

    # Filtracja na podstawie marki, jeśli marka jest podana
    if marka:
        sprzedaz = sprzedaz.filter(produkt__marka__icontains=marka)

    # Grupowanie danych w Pythonie
    sprzedaz_podsumowanie = defaultdict(lambda: {'liczba_sztuk': 0, 'stawka': 0, 'suma_prowizji': 0, 'marka': ''})

    for item in sprzedaz:
        model = item.produkt.model
        marka = item.produkt.marka
        sprzedaz_podsumowanie[(marka, model)]['liczba_sztuk'] += item.liczba_sztuk
        sprzedaz_podsumowanie[(marka, model)]['stawka'] = item.produkt.stawka
        sprzedaz_podsumowanie[(marka, model)]['suma_prowizji'] += item.produkt.stawka * item.liczba_sztuk
        sprzedaz_podsumowanie[(marka, model)]['marka'] = marka

    # Przekształcenie defaultdict na zwykły słownik do renderowania
    sprzedaz_podsumowanie = dict(sprzedaz_podsumowanie)

    # Obliczanie sumarycznych wartości dla wszystkich sprzedaży
    liczba_sztuk = sum(item['liczba_sztuk'] for item in sprzedaz_podsumowanie.values())
    calkowita_prowizja = sum(item['suma_prowizji'] for item in sprzedaz_podsumowanie.values())

    context = {
        'sprzedaz': sprzedaz_podsumowanie,
        'liczba_sztuk': liczba_sztuk,
        'calkowita_prowizja': calkowita_prowizja,
    }

    return render(request, 'produkty/podsumowanie_sprzedazy.html', context)

def wyciagnij_liste_modeli(request):
    if request.method == 'POST':
        tekst = request.POST.get('tekst_sprzedazy', '')
        # Wyciągnięcie sekcji MOJE
        wzorzec_moje = re.compile(r'MOJE\s*(.*?)\s*(INNE|$)', re.S)
        wynik_moje = wzorzec_moje.search(tekst)
        if wynik_moje:
            lista_modeli = wynik_moje.group(1).split('\n')
            # Filtrowanie tylko rzeczywistych modeli (np. brak spacji, tylko duże litery i cyfry)
            lista_modeli = [
                model.strip() for model in lista_modeli
                if re.match(r'^[A-Z0-9]+$', model.strip())
            ]
        else:
            lista_modeli = []

        context = {'lista_modeli': lista_modeli}
        return render(request, 'produkty/wyciagnij_liste_modeli.html', context)
    else:
        return render(request, 'produkty/wyciagnij_liste_modeli.html')

def lista_zadaniowek(request):
    zadaniowki = Task.objects.all()
    return render(request, 'produkty/lista_zadaniowek.html', {'zadaniowki': zadaniowki})

def szczegoly_zadaniowki(request, task_id):
    zadaniowka = get_object_or_404(Task, pk=task_id)
    return render(request, 'produkty/szczegoly_zadaniowki.html', {'zadaniowka': zadaniowka})

def postepy_zadaniowki(request, task_id):
    zadaniowka = get_object_or_404(Task, id=task_id)
    produkty = zadaniowka.produkty.all()
    total_sprzedane_sztuki = Sprzedaz.objects.filter(produkt__in=produkty).aggregate(models.Sum('liczba_sztuk'))['liczba_sztuk__sum'] or 0
    pozostaly_cel = max(0, zadaniowka.minimalna_liczba_sztuk - total_sprzedane_sztuki)

    context = {
        'zadaniowka': zadaniowka,
        'produkty': produkty,
        'total_sprzedane_sztuki': total_sprzedane_sztuki,
        'pozostaly_cel': pozostaly_cel,
    }
    return render(request, 'produkty/postepy_zadaniowki.html', context)

def ekspozycja_form(request, grupa_id):
    grupa = get_object_or_404(GrupaProduktowa, id=grupa_id)
    marki = Marka.objects.all()

    if request.method == 'POST':
        # Usuń istniejące rekordy dla tej grupy, aby uniknąć duplikatów
        Ekspozycja.objects.filter(grupa=grupa).delete()

        for marka in marki:
            liczba = int(request.POST.get(f'marka_{marka.id}', 0))
            Ekspozycja.objects.create(
                grupa=grupa,
                marka=marka,
                liczba=liczba
            )
        
        # Przejdź do następnej grupy lub wyświetl podsumowanie
        ostatnia_grupa_id = GrupaProduktowa.objects.last().id
        if grupa_id >= ostatnia_grupa_id:
            return redirect('produkty:ekspozycja_summary')
        return redirect('produkty:ekspozycja_form', grupa_id=grupa_id + 1)

    return render(request, 'produkty/ekspozycja_form.html', {
        'grupa': grupa,
        'marki': marki,
    })
        
def ekspozycja_summary(request):
    # Pobierz wszystkie dane ekspozycji z bazy danych
    ekspozycje = Ekspozycja.objects.select_related('grupa', 'marka').all()

    # Przygotuj dane do wyświetlenia w podsumowaniu
    grupy = GrupaProduktowa.objects.all()

    dane_podsumowania = []
    for grupa in grupy:
        marki_ekspozycji = ekspozycje.filter(grupa=grupa)
        dane_podsumowania.append({
            'grupa': grupa.nazwa,
            'marki': marki_ekspozycji,
        })

    return render(request, 'produkty/ekspozycja_summary.html', {
        'dane_podsumowania': dane_podsumowania,
    })