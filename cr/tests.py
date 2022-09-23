from django.test import TestCase

# Create your tests here.

from cr.models import *

p = CatalogoProds.objects.get_or_create(nombre_producto = "Lucerna", pais_producto="El Salvador", tipo_producto="detergente", precio_unidad=12)
v = VentaProds.objects.get_or_create(nombre_producto_id = "Lucerna", cantidad_vendida=120, numero_semana='2021-08-31')
