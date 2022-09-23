from django.urls import re_path, path
from cr import views
from .views import CatalogProductListView, IngresosListView, datasource_sales, search_products, view_ventas_p_prod, detalle_producto_tipo, chart_sales


urlpatterns = [
    path('', views.index, name='index'),
    #path('productos', CatalogProductListView.as_view(), name="productos"),
    re_path(r'productos', CatalogProductListView.as_view(), name='product_list_view'),
    re_path(r'ventas', view_ventas_p_prod, name='ventas_view'),
    re_path('detalle_tipo', detalle_producto_tipo, name='detail_per_type'),
    re_path('ingresos', IngresosListView.as_view(), name='listado_ingresos'),
    re_path('search', search_products, name='search_product'),
    re_path('sales_prod.json', datasource_sales, name='sales_product'),
    re_path('chart_sales', chart_sales, name='chart_sales'),
    re_path('carga', views.display_upload_form, name='carga'),
    re_path('cargar_csv', views.upload_file_csv, name='uploaded_csv'),
]