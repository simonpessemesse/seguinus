from restaurant.models import Resa, Fournisseur, Fourniture, Plat, Menu, ResaResto
from django.contrib import admin


class ResaRestoAdmin(admin.ModelAdmin):
    exclude = ('reservationEcrasee', 'nbPassagers', 'nbPiquesNiques')


admin.site.register(Resa)
admin.site.register(Fournisseur)
admin.site.register(Fourniture)
admin.site.register(Plat)
admin.site.register(Menu)
admin.site.register(ResaResto, ResaRestoAdmin)
