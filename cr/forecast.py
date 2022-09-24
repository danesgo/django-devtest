from sklearn import linear_model


def estimar_con_semana_y_product_id(semana_num, pid):
    from cr.models import CatalogoProds, VentaProds
    datos_ventas = VentaProds.objects. \
        values("numero_semana", "cantidad_vendida"). \
        filter(producto_id=pid)

    return predecir_con_fecha_lista_ventas(int(semana_num), datos_ventas)


def predecir_con_fecha_lista_ventas(fecha_prediccion, lista_ventas):
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

    #Inicializa regresor
    regr = linear_model.LinearRegression()
    #Genera el fit
    regr.fit(X_data, Y_data)
    regr_values = {"inter": regr.intercept_, "coef": regr.coef_}

    #Calcula la prediccion con un valor de semana-fecha.
    Y_Pred = regr.predict([[fecha_prediccion]])[0]

    print(f"Predicho: {Y_Pred}")

    ret = {"predicto": [Y_Pred, fecha_prediccion],"valores_reg": regr_values, "data": datas}
    vals, semana  = list(zip(*ret["data"]))
    ret["semanas"] = semana
    ret["vals"] = vals

    return ret


def render_d_graph(ret_vals):
    from json import dumps as jsonify
    base_str = """
    <img src='https://quickchart.io/chart?bkg=white&c={}' />
    """
    dataz = {
        "type": "line",
        "data": {
            "datasets": [
                {
                    "fill": False,
                    "spanGaps": False,
                    "pointStyle": "circle",
                    "data":
                        ret_vals['vals'] , ## Object Semanas lista de indices de semana
                    "type": "line",
                    "label": "ventas",
                    "borderColor": "red",
                    "borderWidth": 1,
                    "hidden": False
                },
                {
                    "fill": False,
                    "pointStyle": "rect",
                    "data": [
                        {
                            "x": ret_vals['predicto'][1],
                            "y": ret_vals['predicto'][0]
                        }
                    ],
                    "type": "scatter",
                    "label": "estimacion",
                    "borderColor": "blue",
                    "backgroundColor": "blue",
                    "borderWidth": 3,
                    "hidden": False,
                    "yAxisID": "Y1"
                }
            ],
            "labels": ret_vals['semanas'] #### semanas as labels
        },
        "options": {
            "title": {
                "display": False,
                "position": "top",
                "fontSize": 12,
                "fontFamily": "sans-serif",
                "fontColor": "grey",
                "fontStyle": "bold",
                "padding": 10,
                "lineHeight": 1.2,
                "text": "Chart title"
            },
            "legend": {
                "display": True,
                "position": "top",
                "align": "center",
                "fullWidth": True,
                "reverse": False,
                "labels": {
                    "fontSize": 12,
                    "fontFamily": "sans-serif",
                    "fontColor": "grey",
                    "fontStyle": "normal",
                    "padding": 10
                }
            },
            "scales": {
                "xAxes": [
                    {
                        "id": "X1",
                        "display": True,
                        "position": "bottom",
                        "type": "category",
                        "stacked": False,
                        "time": {
                            "unit": False,
                            "stepSize": 1,
                        },
                        "distribution": "linear",
                        "gridLines": {
                            "display": True,
                            "color": "rgba(0, 0, 0, 0.1)",
                            "borderDash": [
                                0,
                                0
                            ],
                            "lineWidth": 1,
                            "drawBorder": True,
                            "drawOnChartArea": True,
                            "drawTicks": True,
                            "tickMarkLength": 10,
                            "zeroLineWidth": 1,
                            "zeroLineColor": "rgba(0, 0, 0, 0.25)",
                            "zeroLineBorderDash": [
                                0,
                                0
                            ]
                        },
                        "angleLines": {
                            "display": True,
                            "color": "rgba(0, 0, 0, 0.1)",
                            "borderDash": [
                                0,
                                0
                            ],
                            "lineWidth": 1
                        },
                        "pointLabels": {
                            "display": True,
                            "fontColor": "grey",
                            "fontSize": 10,
                            "fontStyle": "normal"
                        },
                        "ticks": {
                            "display": True,
                            "fontSize": 12,
                            "fontFamily": "sans-serif",
                            "fontColor": "grey",
                            "fontStyle": "normal",
                            "padding": 0,
                            "stepSize": None,
                            "minRotation": 0,
                            "maxRotation": 50,
                            "mirror": False,
                            "reverse": False
                        },
                        "scaleLabel": {
                            "display": False,
                            "labelString": "Axis label",
                            "lineHeight": 1.2,
                            "fontColor": "grey",
                            "fontFamily": "sans-serif",
                            "fontSize": 12,
                            "fontStyle": "normal",
                            "padding": 4
                        }
                    }
                ],
                "yAxes": [
                    {
                        "id": "Y1",
                        "display": True,
                        "position": "left",
                        "type": "linear",
                        "stacked": False,
                        "time": {
                            "unit": False,
                            "stepSize": 1,
                        },
                        "distribution": "linear",
                        "gridLines": {
                            "display": True,
                            "color": "rgba(0, 0, 0, 0.1)",
                            "borderDash": [
                                0,
                                0
                            ],
                            "lineWidth": 1,
                            "drawBorder": True,
                            "drawOnChartArea": True,
                            "drawTicks": True,
                            "tickMarkLength": 10,
                        },
                        "angleLines": {
                            "display": True,
                            "color": "rgba(0, 0, 0, 0.1)",
                        },
                        "pointLabels": {
                            "display": True,
                            "fontColor": "gray",
                            "fontSize": 10,
                            "fontStyle": "normal"
                        },
                        "ticks": {
                            "display": True,
                            "fontSize": 12,
                            "fontFamily": "sans-serif",
                            "fontColor": "gray",
                            "fontStyle": "normal",
                            "minRotation": 0,
                            "maxRotation": 50,
                            "mirror": False,
                            "reverse": False
                        },
                        "scaleLabel": {
                            "display": False,
                            "labelString": "Axis label",
                            "lineHeight": 1.2,
                            "fontColor": "gray",
                            "fontFamily": "sans-serif",
                            "fontSize": 12,
                            "fontStyle": "normal",
                            "padding": 4
                        }
                    }
                ]
            },
            "cutoutPercentage": 50,
        }
    }
    return base_str.format(jsonify(dataz))