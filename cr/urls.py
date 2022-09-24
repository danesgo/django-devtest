from django.urls import re_path, path
from cr import views
from .views import CatalogProductListView, IngresosListView, \
    datasource_sales, search_products, view_ventas_p_prod, \
    detalle_producto_tipo, chart_sales, \
    display_upload_form, upload_file_csv, upload_file_xls, \
    estimator_result, display_forecast, producto_individual

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
    re_path('uploads', display_upload_form, name='uploads'),
    re_path('csv_upload', upload_file_csv, name='upload_csv'),
    re_path('excel_upload', upload_file_xls, name='upload_xls'),

    path('display_forecast', display_forecast, name='forecast'),
    path('generate_forecast', estimator_result, name='gen_forecast'),

    path('products/<int:pid>', producto_individual, name = 'view_products')
]