from django.contrib import admin

from adapost.models import Ingrijitor, Animal, Rezerva, Eveniment


class IngrijitorAdmin(admin.ModelAdmin):
    list_display = ['nume', 'nr_telefon', 'este_angajat', 'este_voluntar']
    list_filter = ['este_angajat', 'este_voluntar']


class AnimalAdmin (admin.ModelAdmin):
    list_display = ['nume', 'specie', 'luna', 'anul', 'sex', 'talie', 'observatie', 'este_adoptat']
    list_filter = ['este_adoptat', 'specie', 'talie']


class RezervaAdmin (admin.ModelAdmin):
    list_display = ['numar', 'animal', 'dimensiune', 'observatii']
    list_filter = ['dimensiune']

class EvenimentAdmin(admin.ModelAdmin):
    list_display = ['ingrijitor', 'rezerva', 'data']
    list_filter = ['data', 'ingrijitor']


# This is how we tell Django to use the class TaskAdmin as the UI configuration
# for the UI
admin.site.register(Ingrijitor, IngrijitorAdmin)
admin.site.register(Animal, AnimalAdmin)
admin.site.register(Rezerva, RezervaAdmin)
admin.site.register(Eveniment, EvenimentAdmin)
