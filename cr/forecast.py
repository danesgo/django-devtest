from sklearn import linear_model


def load_data_est():
    from cici.models import CatalogoProds, VentaProds

    Datos_Ventas = VentaProds.objects.\
        values("numero_semana", "cantidad_vendida").\
        filter(NombreProducto_id=idproductooo)
    #TODO: hay que filtrar por el id de producto


    estimacion_de_producto_por_fecha(1, Datos_Ventas)
    pass


def estimacion_de_producto_por_fecha(fecha_prediccion, lista_ventas):
    """Estima la venta para una semana dada en base a una lista de datos de ventas y fechas de ingreso.

    Args:
        lista_ventas: un list-like con tuplas con numero_semana y cantidad_vendida.
        fecha_prediccion: un numero con la semana de fecha a estimar.
    """

    datas = list()
    for dato in range(0, len(lista_ventas)):
        semana = int(lista_ventas[dato]['numero_semana'].split('-')[-1])
        datas.append([lista_ventas[dato]['cantidad_vendida'], semana])

    datas = sorted(datas, key=lambda x: x[1])

    X_data = list()
    Y_data = list()

    for dato in range(0, len(datas)):
        X_data.append([datas[dato][1]])
        Y_data.append(datas[dato][0])

    regr = linear_model.LinearRegression()
    regr.fit(X_data, Y_data)
    regr_values = {"coef": regr.coef_, "inter": regr.intercept_}

    Y_Pred = regr.predict([[fecha_prediccion]])

    print(f"Predicho: {Y_Pred}")

    ret = {"predicto": [fecha_prediccion, Y_Pred],"valores_reg": regr_values, "data": datas}
    return ret
