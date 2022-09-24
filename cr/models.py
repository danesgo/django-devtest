from django.db import models
from datetime import timedelta


# Create your models here.
class DateWeekTruncated(models.DateField):

    def truncate_week(self, dt):
        return dt - timedelta(days=dt.weekday())

    def to_python(self, value):
        value = super().to_python(value)
        if value:
            return self.truncate_week(value)
        return value




class CatalogoProds(models.Model):
    """Representa la Tabla 1, con los productos y su informacion.

    Debido a que el indice de catalog en realidad es una version desnormalizada
    de una tabla producto y una tabla precio-fecha, se genera un ID por cada combinacion
    producto-fecha para guardar el historial de precios (y los demas atributos).
    """

    # crea un campo implicito con _id
    nombre_producto = models.CharField(max_length=127)

    pais_producto = models.CharField(max_length=127)
    tipo_producto = models.CharField(max_length=127)
    precio_unidad = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return f"Producto: {self.nombre_producto}({self.created_at.strftime('%b %d %Y')}) - {self.tipo_producto}"


class IngresoProds(models.Model):
    producto = models.ForeignKey(CatalogoProds, on_delete=models.CASCADE)
    cantidad_ingresada = models.IntegerField()
    fecha_ingreso = models.DateField()

    class Meta:
        verbose_name = "Ingreso"
        verbose_name_plural = "Ingresos"


# Tabla 3
class VentaProds(models.Model):
    producto = models.ForeignKey(CatalogoProds, on_delete=models.CASCADE)
    cantidad_vendida = models.IntegerField()
    numero_semana = models.CharField(max_length=20) #DateWeekTruncated()

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def calcular_precio_a_fecha_venta(self):
        precio_a_fecha_de_venta = self.producto.precio_unidad  # obtener objeto producto y extraer precio

        return self.cantidad_vendida * precio_a_fecha_de_venta

