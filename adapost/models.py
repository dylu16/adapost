from datetime import datetime

from dateutil import relativedelta
from django.core.exceptions import ValidationError
from django.db import models

from adapost.constants import TipSpecie, Dimensiune, Sex


class Animal(models.Model):
    class Meta:
        verbose_name_plural = "Animale"

    nume = models.CharField(max_length=30)
    specie = models.SmallIntegerField(choices=TipSpecie.CHOICES)
    luna = models.SmallIntegerField()  # 32767
    anul = models.SmallIntegerField()
    sex = models.SmallIntegerField(choices=Sex.CHOICES)
    talie = models.SmallIntegerField(choices=Dimensiune.CHOICES)
    observatie = models.TextField()
    este_adoptat = models.BooleanField()

    def __str__(self):
        return self.nume

    def clean(self):
        if self.luna < 1 or self.luna > 12:
            raise ValidationError('Luna trebuie sa fie intre 1 si 12!')

        if self.anul < 1900 or self.anul > 2020:
            raise ValidationError('Anul trebuie sa fie intre 1900 si 2020')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)

    @property
    def varsta(self) -> str:
        today = datetime.today()
        data_nasterii = datetime(year=self.anul, month=self.luna, day=1)
        diff = relativedelta.relativedelta(today, data_nasterii)
        if diff.years and diff.months:
            return f'{diff.years} ani si {diff.months} luni'
        elif diff.years and not diff.months:
            return f'{diff.years} ani'
        else:
            return f'{diff.months} luni'


class Rezerva(models.Model):
    class Meta:
        verbose_name_plural = "Rezerve"

    numar = models.SmallIntegerField()
    animal = models.ForeignKey(to=Animal, null=True, blank=True, on_delete=models.SET_NULL)
    dimensiune = models.SmallIntegerField(choices=Dimensiune.CHOICES)
    observatii = models.TextField()

    def __str__(self):
        return str(self.numar)

    def clean(self):
        if self.animal and self.dimensiune != self.animal.talie:
            raise ValidationError('Dimensiuna custii este nepotrivita')

        if self.animal and self.animal.este_adoptat is True:
            raise ValidationError('Animalul este adoptat. Rezerva este libera.')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)


class Ingrijitor(models.Model):
    class Meta:
        verbose_name_plural = "Ingrijitori"

    nume = models.CharField(max_length=60)
    nr_telefon = models.CharField('numar telefon', max_length=10)
    este_voluntar = models.BooleanField()
    data_angajarii = models.DateField()
    este_angajat = models.BooleanField(help_text='Marcheaza daca ingrijitorul este activ in companie')

    def __str__(self):
        return self.nume


class Eveniment(models.Model):
    class Meta:
        verbose_name_plural = "Evenimente"
    ingrijitor = models.ForeignKey(to=Ingrijitor, on_delete=models.DO_NOTHING)
    rezerva = models.ForeignKey(to=Rezerva, on_delete=models.DO_NOTHING)
    data = models.DateField()

    def clean(self):
        if Eveniment.objects.filter(rezerva=self.rezerva, data=self.data).count() >= 3:
            raise ValidationError('Animalul a fost deja hranit de 3 ori astazi.')

        if self.rezerva.animal is None:
            raise ValidationError('Rezerva este libera.')

        if self.ingrijitor.este_angajat is False:
            raise ValidationError('Ingrijitorul nu mai este angajat')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        super().save(force_insert, force_update, using, update_fields)
