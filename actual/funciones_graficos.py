#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 18:28:16 2023

@author: anavelyz
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

layout = go.Layout

violencias_names = {
    "identidad": "Duplicación de identidad",
    "ciberacoso": "Ciberacoso",
    "doxxing": "Doxxing",
    "mobbing": "Mobbing",
    "ciberdifamacion": "Ciberdifamación",
    "stalking": "Cibervigilancia (stalking)",
    "ciberextorsion": "Ciberextorsión",
    "grooming": "Grooming",
    "phishing_vs": "Phishing/Vishing/Smishing",
    "trata": "Trata de personas en línea",
    "explotacion": "Captación con fines de explotación sexual",
    "exclusion": "Exclusión digital",
    "cyberflashing": "Cyberflashing",
    "deepfake": "Deepfake",
    "clonacion": "Clonación de aplicaciones",
    "phishing": "Phishing/Vishing/Smishing",
}

medios_nombres = {
    "twitter": "Twitter",
    "facebook": "Facebook",
    "whatsapp": "WhatsApp",
    "telegram": "Telegram",
    "correo": "Correo",
    "tiktok": "TikTok",
    "sms": "SMS",
    "citas": "Apps de citas Tinder, Grindr, Bumble, etc" "Twitter",
    "videojuegos": "Videojuegos en línea",
    "estudio": "Plataformas de estudio: Teams, Zoom, Google Classroom, aulas virtuales, etc",
    "trabajo": "Plataformas de trabajo: Teams, Zoom, Meet, Slack, etc",
    "red": "Red interna del trabajo",
    "otra": "Otra",
    "instagram": "Instagram",
    "llamadas": "Llamadas telefónicas",
}


def grafico_edad(df: pd.DataFrame, sexo: str = "Mujer"):
    if sexo == "Mujer":
        yaxis = "% de mujeres"
        color = "rgb(7, 171, 157)"
    else:
        yaxis = "% de hombres"
        color = "rgb(157, 178, 191)"
    variable = [s for s in df.columns if "edad_" in s]
    data = (
        pd.cut(
            df[variable[0]],
            bins=[0, 10, 15, 18, 25, 30, 40, 50, 60, 75],
            right=False,
        )
        .value_counts()
        .sort_index()
    )
    df_ = data / df.iloc[:, 0].sum() * 100
    x = df_.index.astype("string")
    y = df_.values
    i = variable[0].split("_")[1]
    fig = px.bar(df_, x, y, text_auto=True)
    fig.update_layout(
        title="".join(
            [
                "Rangos de edad en que las víctimas sufrieron <br>",
                violencias_names[i].casefold(),
                " por primera vez"
            ]
        ),
        xaxis_title="Edades",
        yaxis_title=yaxis,
        font=dict(
            family="Arial",
            size=15,
            color="black",
        ),
        width=1500,
        height=800,
    )
    fig.update_traces(
        textfont_size=18,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
        showlegend=False,
        marker_color=color,
        marker_line_color="white",
        texttemplate="%{value: .4} %",
    )
    fig.update_xaxes(labelalias={
                                "[0, 10)": "0-9",
                                "[10, 15)": "10-14",
                                "[15, 18)": "15-17",
                                "[18, 25)": "18-24",
                                "[25, 30)": "24-29",
                                "[30, 40)": "30-39",
                                "[40, 50)": "40-49",
                                "[50, 60)": "50-59",
                                "[60, 75)": "60 y más",
                            })
    fig.write_image("".join(["img/", variable[0], ".png"]))
    fig.show()
    return [fig, data, df_]


def grafico_frecuencia(df: pd.DataFrame, sexo: str = "Mujer"):
    if sexo == "Mujer":
        yaxis = "% de mujeres"
        color = "rgb(149, 27, 129)"
    else:
        yaxis = "% de hombres"
        color = "rgb(39, 55, 77)"
    variable = [s for s in df.columns if "veces_" in s]
    df_ = pd.DataFrame(df[variable[0]].value_counts())
    frecuencia = round(df_ / df_.sum() * 100, 2)
    i = variable[0].split("_")[1]
    fig = px.bar(frecuencia, text_auto=True)
    fig.update_layout(
        title=" ".join(["Incidencia de", violencias_names[i].casefold()]),
        xaxis_title="Frecuencia",
        yaxis_title=yaxis,
        font=dict(
            family="Arial",
            size=18,
            color="black",
        ),
        width=1500,
        height=800,
    )
    fig.update_traces(
        textfont_size=18,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
        showlegend=False,
        marker_color=color,
        marker_line_color="white",
        texttemplate="%{value:} %",
    )
    fig.write_image("".join(["img/", variable[0], ".png"]))
    fig.show()
    return [fig, df_, frecuencia]


def grafico_temporalidad(df: pd.DataFrame, sexo: str = "Mujer"):
    variable = [s for s in df.columns if "6_" in s]
    df_ = pd.DataFrame(df[variable[0]].value_counts())
    i = variable[0].split("_")[1]
    if sexo == "Mujer":
        color = {"Sí": "rgb(149, 27, 129)", "No": "rgb(57, 105, 172)"}
    else:
        color = {"Sí": "rgb(39, 55, 77)", "No": "rgb(82, 109, 130)"}
    if len(df_) <=1:
        print(f"Las personas que sufrieron de {i}, manifiestan que {df_.index[0].lower()} ocurrió durante los últimos 6 meses")
    else:
        fig = px.pie(
            df_,
            names=df_.index,
            values=df_["count"],
            color=df_.index,
            color_discrete_map=color,
        )
        fig.update_layout(
            title_text=" ".join(
                ["Porcentaje de víctimas de", violencias_names[i].casefold(),
                 "en los últimos 6 meses"],
            ),
            legend_title="¿Ocurrió en los últimos seis meses?",
            font=dict(family="Arial", size=18, color="black"),
            width=1500,
            height=800,
        )
        fig.update_traces(
            marker=dict(
                line=dict(color="white", width=1),
            )
        )
        fig.show()
        fig.write_image("".join(["img/", variable[0], ".png"]))
        return [fig, df_]


def grafico_parentesco(df: pd.DataFrame, sexo: str = "Mujer"):
    if sexo == "Mujer":
        yaxis = "las mujeres"
        color = "rgb(57, 105, 172)"
    else:
        yaxis = "los hombres"
        color = "rgb(82, 109, 130)"

    variable = [s for s in df.columns if "parentesco_" in s or "identificacion_" in s]
    i = variable[0].split("_")[1]
    data = pd.DataFrame(df[variable[0]].value_counts())

    if len(data)<=1:
        df_ = data
        print("Las personas que sufrieron de {i} manifiestan que su parentesco con su agresor es: {data.index[0]}.lower()}")
    if i not in ["grooming", "phishing_vs", "trata", "phishing", "mobbing"]:
        data.rename_axis(index="parentesco", inplace=True)
        data.reset_index(inplace=True)
        df_ = data
        df_["count"] = df_["count"] / df.iloc[:, 0].sum() * 100

        fig = px.bar(df_, x="parentesco", y="count", text_auto=True)
        fig.update_layout(
            title=" ".join(
                [
                    "Parentesco de la persona agresora con",
                    yaxis,
                    "que <br> han sufrido",
                    violencias_names[i].casefold(),
                ]
            ),
            title_x=0.5,
            xaxis_title="Parentesco",
            yaxis_title="% de agresiones",
            font=dict(
                family="Arial",
                size=16,
                color="black",
            ),
            width=1500,
            height=800,
        )
        fig.update_traces(
            textfont_size=18,
            textangle=0,
            textposition="outside",
            cliponaxis=False,
            showlegend=False,
            marker_color=color,
            marker_line_color="white",
            texttemplate="%{value: .4} %",
        )

    elif i == "mobbing":
        if sexo == "Mujer":
            color = ["rgb(149, 27, 129)", "rgb(57, 105, 172)", "rgb(7, 171, 157)"]
        else:
            color = ["rgb(39, 55, 77)", "rgb(82, 109, 130)", "rgb(157, 178, 191)"]
        df_ = data
        fig = go.Figure(data=[go.Pie(labels=df_.index, values=df_["count"])])
        fig.update_layout(
            title_text="Relación laboral con el agresor",
            legend_title="El agresor era:",
            font=dict(family="Arial", size=18, color="black"),
            width=1500,
            height=1000,
        )
        fig.update_traces(
            marker=dict(
                colors=color,
                line=dict(color="white", width=1),
            )
        )

        fig.write_image(
            "".join(
                [
                    "img/parentesco",
                    variable[0],
                    ".png",
                ]
            )
        )
    else:
        if sexo == "Mujer":
            color = ["rgb(149, 27, 129)", "rgb(57, 105, 172)"]
        else:
            color = ["rgb(39, 55, 77)", "rgb(82, 109, 130)", "rgb(157, 178, 191)"]
        df_ = data
        fig = go.Figure(data=[go.Pie(labels=df_.index, values=df_["count"])])
        fig.update_layout(
            title_text=" ".join(
                [
                    "Identificación de la persona agresora por parte <br> de la víctima de",
                    violencias_names[i].casefold(),
                ]
            ),
            legend_title="¿Identificaste al agresor(a)?",
            width=1500,
            height=800,
            font=dict(family="Arial", size=18, color="black")
        )
        fig.update_traces(
            marker=dict(
                colors=color,
                line=dict(color="white", width=1),
            )
        )
    fig.show()
    return [fig, data, df_]


def grafico_sexo_parentesco(df: pd.DataFrame, sexo: str = "Mujer"):
    variable = [s for s in df.columns if "sexo_" in s]
    df_ = pd.DataFrame(df[variable[0]].value_counts())
    i = variable[0].split("_")[1]
    if sexo == "Mujer":
        color = {"Mujer": "rgb(149, 27, 129)", "Hombre": "rgb(57, 105, 172)"}
    else:
        color = {"Mujer": "rgb(39, 55, 77)", 
                 "Hombre": "rgb(82, 109, 130)",
                "Un grupo de personas": "rgb(157, 178, 191)"}
    
    fig = px.pie(
        df_,
        names=df_.index,
        values=df_["count"],
        color=df_.index,
        color_discrete_map=color,
    )
    fig.update_layout(
        title_text=" ".join(
            [
                "Sexo de la persona agresora para",
                violencias_names[i].casefold(),
            ]
        ),
        legend_title="Sexo del agresor(a)",
        font=dict(family="Arial", size=18, color="black"),
        width=1500,
        height=800,
    )
    fig.update_traces(
        marker=dict(
            line=dict(color="white", width=1),
        )
    )
    fig.write_image("".join(["img/", df_.index.name, ".png"]))
    if len(df_) <= 1:
        print(f"Para {violencias_names[i].casefold()} todas las personas agresoras son de sexo {df_.index[0]}")
    else:
        fig.show()
    return [fig, df_]


def grafico_medios(df: pd.DataFrame, sex: str = "Mujer"):
    if sex == "Mujer":
        yaxes = "% de mujeres"
        color = "rgb(149, 27, 129)"
    else:
        yaxes = "% de hombres"
        color = "rgb(39, 55, 77)"

    variable = [s for s in df.columns if "medio_" in s]
    data = df.iloc[:, df.columns.get_loc(variable[0]) + 1:-1].sum()
    i = variable[0].split("_")[1]
    new_index = []
    for medio in list(data.index.values):
        if medio.split("_")[0] in medios_nombres.keys():
            new_index.append(medios_nombres[medio.split("_")[0]])
    data.index = new_index
    df_ = data / df.iloc[:, 0].sum() * 100
    fig = px.bar(
        df_,
        x=df_.index,
        y=df_.values,
        title=" ".join(
            [
                "Aplicación o red social por la cual la victima sufrió",
                violencias_names[i].casefold(),
            ]
        ),
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        width=1500,
        height=800,
    )
    fig.update_xaxes(title="App/red social")
    fig.update_yaxes(title=yaxes)
    fig.update_traces(
        textfont_size=18,
        textangle=0,
        textposition="outside",
        cliponaxis=False,
        showlegend=False,
        marker_color=color,
        marker_line_color="white",
        texttemplate="%{value: .4} %",
    )
    fig.update_layout(font=dict(family="Arial", size=18, color="black"))
    fig.show()
    fig.write_image("".join(["img/", variable[0].casefold(), ".png"]))
    return [fig, data, df_]


def grafico_piramide():
    lista = []
    for j, k in zip(tbl_identidad[variables[0]], tbl_identidad[variables[1]]):
        if j != "No le pude identificar" and j != "No":
            lista.append((j, k))
            df = pd.DataFrame(lista,
                              columns=["Parentesco", "Sexo"]
                              ).value_counts()
