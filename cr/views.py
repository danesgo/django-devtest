from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q

from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import VentaProds, IngresoProds, CatalogoProds
from .forecast import estimar_con_semana_y_product_id, render_d_graph

# Create your views here.
#def index(request):
 #   return HttpResponse("Hello World!")

def index(request):
    return render(request, "index.html")

class CatalogProductListView(ListView):
    """Listado de Catalogo de  Productos"""
    model = CatalogoProds


class IngresosListView(ListView):
    """Listado de ingresos de productos"""
    model = IngresoProds


def view_ventas_p_prod(request):
    """Ventas de Productos"""
    ventas = VentaProds.objects.all()
    return render(request, "vista_ventas.html", context={"ventas": ventas})


def detalle_producto_tipo(request):
    """Productos por tipo   """
    ptype = request.GET.get("product_type", "")
    productos_por_tipo = CatalogoProds.objects.filter(tipo_producto=ptype)

    return render(request, "vista_por_tipo.html", context={"tipo_producto": ptype, "productos": productos_por_tipo})


@csrf_exempt
def search_products(request):
    pname = request.POST.get("product_name", "")
    search_string = f" Buscando que contengan {pname} en el nombre."
    products = CatalogoProds.objects.filter((Q(nombre_producto__search=pname) | Q(tipo_producto__search=pname)))
    return render(request, "cici/catalogoprods_list.html", context={"object_list":products, "search":search_string})


def display_upload_form(request):
    return render(request, "up_form.html")


def upload_file_csv(request):
    from .parse_uploaded_files import parse_csv_file
    if request.method == "GET":
        return render(request, "up_form.html")

    csv_file = request.FILES['csv_file']
    parse_csv_file(csv_file)
    return HttpResponse("Archivo CSV cargdado exitosamente! <a href='/index'>Volver</a>")


def upload_file_xls(request):
    from .parse_uploaded_files import parse_excel_file
    if request.method == "GET":
        return render(request, "up_form.html")

    excel_file = request.FILES['excel_file']
    parse_excel_file(excel_file)
    return HttpResponse("Archivo Excel cargado exitosamente! <a href='/index'>Volver</a>")


def sales_chart_string(product_id, render_img=False):

    from django.db.models import Sum
    ventas_semana = VentaProds.objects.filter(producto_id=product_id)
    venta_values = ventas_semana.values('numero_semana').annotate(total_sales=Sum('cantidad_vendida'))

    venta_dates = []
    venta_vals = []
    for item in venta_values:
        venta_dates.append(str(item["numero_semana"])) #TODO: format date
        venta_vals.append(item["total_sales"])

    data = {
        'type': 'bar',
        'data': {
            'labels': venta_dates,
            'datasets': [{
                'label': 'Unidade Vendidas',
                'data': venta_vals
            }]
        }
    }

    if render_img:
        raw_img = f"""
            <img src="https://quickchart.io/chart?bkg=white&c={data}" />
            """
        return raw_img
    return data


def datasource_sales(request):
    product_id = request.GET.get("producto", "")
    json_data = sales_chart_string(product_id)
    return JsonResponse(json_data)


def chart_sales(request):
    from django.http import HttpResponse
    product_id = request.GET.get("producto")
    json_data = sales_chart_string(product_id)
    raw_img = f"""
    <img src="https://quickchart.io/chart?bkg=white&c={json_data}" />
    """
    return HttpResponse(raw_img)


def display_forecast(request):
    prods = CatalogoProds.objects.all()
    return render(request, "estima_form.html", context={"products": prods})


def estimator_result(request):
    semana_fecha = request.GET.get("semana")
    product_id = request.GET.get("product_id")

    predictioN_result = estimar_con_semana_y_product_id(semana_fecha, product_id)

    predictioN_result['chart'] = render_d_graph(predictioN_result)
    return render(request,"show_prediction.html", context=predictioN_result)

def producto_individual(request, pid):
    p = get_object_or_404(CatalogoProds, id=pid)
    json_data = sales_chart_string(p.id)
    chart_tag = f"""
    <img src="https://quickchart.io/chart?bkg=white&c={json_data}" />
    """
    return render(request, "producto_individual.html", context={"p": p, "chart": chart_tag})
