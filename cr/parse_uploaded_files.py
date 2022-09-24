import pandas
from cr.models import *


def parse_excel_file(uploaded_file):
    sales_df = pandas.read_excel(uploaded_file, engine="openpyxl", sheet_name=2)
    prods_df = pandas.read_excel(uploaded_file,  engine="openpyxl",sheet_name=0)
    ingreso_df = pandas.read_excel(uploaded_file, engine="openpyxl", sheet_name=1)
    process_products(prods_df)
    process_sales(sales_df)
    process_ingreso(ingreso_df)
    return


def parse_csv_file(uploaded_file):
    sales_df = pandas.read_csv(uploaded_file)
    return process_sales(sales_df)


def process_sales(d_frame):
  for i, r in d_frame.iterrows():
    c = CatalogoProds.objects.filter(nombre_producto=r["Nombre de producto"]).order_by("-created_at").first()
    if not c:
        print("Objecto c no encontrado: ")
        print(r)
        continue
    v = VentaProds.objects.create(producto=c, cantidad_vendida = r["Unidades vendidas"], numero_semana=r["Numero de semana"])


def process_products(d_frame):
  for i, r in d_frame.iterrows():
    try:
      c = CatalogoProds.objects.get_or_create(nombre_producto=r["Nombre producto"],
                                         pais_producto=r["Pais"],
                                         tipo_producto=r["Tipo producto"],
                                         precio_unidad=r["Precio unitario"],
                                         created_at=r["Fecha precio"])
    except Exception as e:
        print(e)


def process_ingreso(d_frame):
    for i, r in d_frame.iterrows():
        try:
            p = CatalogoProds.objects.filter(nombre_producto=r["Nombre producto"]).order_by("-created_at").first()
            if not p:
                print("Objecto p no encontrado: " + r["Nombre producto"])
                continue
            i = IngresoProds.objects.create(producto=p,
                                            cantidad_ingresada=r["Cantidad ingresada a bodega"],
                                            fecha_ingreso=r["Fecha ingreso a bodega"],)
        except Exception as e:
            print(e)