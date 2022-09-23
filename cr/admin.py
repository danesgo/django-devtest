from django.contrib import admin
from cr.models import *


# Register your models here.
class ProdAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', )

admin.site.register(CatalogoProds, ProdAdmin)
admin.site.register(IngresoProds)
admin.site.register(VentaProds)