from django.db import models

class Produkt(models.Model):
    model = models.CharField(max_length=100, unique=True)
    stawka = models.DecimalField(max_digits=10, decimal_places=2)
    grupa_towarowa = models.CharField(max_length=100)
    marka = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.marka} - {self.model}"

class Task(models.Model):
    nazwa = models.CharField(max_length=255)
    opis = models.TextField()
    minimalna_liczba_sztuk = models.IntegerField()
    premia_za_minimalna_liczbe = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    premia_za_dodatkowa_liczbe = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    produkty = models.ManyToManyField(Produkt)  # Produkty, które są częścią zadaniówki
    data_rozpoczecia = models.DateField()
    data_zakonczenia = models.DateField()

    def __str__(self):
        return f"{self.nazwa} ({self.data_rozpoczecia} - {self.data_zakonczenia})"

class Sprzedaz(models.Model):
    produkt = models.ForeignKey(Produkt, on_delete=models.CASCADE)
    liczba_sztuk = models.IntegerField()
    data_sprzedazy = models.DateField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True, blank=True)  # Dodajemy powiązanie z taskiem

    def __str__(self):
        return f"{self.produkt.model} - {self.liczba_sztuk} sztuk - {self.data_sprzedazy}"

class GrupaProduktowa(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa

class Marka(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa

class Ekspozycja(models.Model):
    grupa = models.ForeignKey(GrupaProduktowa, on_delete=models.CASCADE)
    marka = models.ForeignKey(Marka, on_delete=models.CASCADE)
    liczba = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.grupa.nazwa} - {self.marka.nazwa}: {self.liczba_sztuk}"