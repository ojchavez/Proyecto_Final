import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import base64
import wget
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format
import datetime

app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB])
server = app.server
app.title = 'resumen'

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
 #   <script>
 #   if (location.protocol !== 'https:') {
 #       location.replace(`https:${location.href.substring(location.protocol.length)}`);
 #   }
 #   </script>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-164720330-2"></script>
        <script>
          window.dataLayer = window.dataLayer || [];
          function gtag(){dataLayer.push(arguments);}
          gtag('js', new Date());

          gtag('config', 'UA-164720330-2');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
    {%app_entry%}
    <footer>
        {%config%}
        {%scripts%}
        {%renderer%}
    </footer>
    </body>
</html>
'''


################ GET DATA START ################
dfGT = pd.read_csv('COVID192.csv')
dfedad = pd.read_csv('edadysexo.csv')
df = pd.read_csv('owid-covid-data.csv')
#df = pd.read_csv(wget.download('https://covid.ourworldindata.org/data/owid-covid-data.csv'))
################ GET DATA END ################
df = df.sort_values(by=['date'])
dfdeps = pd.read_csv('departamentos2.csv')
dfmun = pd.read_csv('MUNICIPIOSTOTAL.csv')
dfdepsTOT = pd.read_csv('departamentosTOT.csv')

dfmun = dfmun.sort_values(by='CASOS', ascending=False)


image_filename4 = 'imagen.PNG' # replace with your own image
encoded_image4 = base64.b64encode(open(image_filename4, 'rb').read())

dfW = df[df['location'].isin(['World'])][['location','date','total_cases','new_cases','total_deaths','new_deaths','total_tests']]
dfW = dfW.sort_values(by=['date'])
dfW['days'] = range(1, len(dfW) + 1)
dfW['tasa_acumulados'] = (dfW.total_cases - dfW.total_cases.shift(1))/dfW.total_cases.shift(1)
dfW['doubling_time'] = 70 / (dfW['tasa_acumulados'] * 100)
dfW['tasa_nuevos_casos'] = (dfW.new_cases - dfW.new_cases.shift(1))/dfW.new_cases.shift(1)
dfW['tasa_nuevos_casos'] = (dfW.new_cases - dfW.new_cases.shift(1))/dfW.new_cases.shift(1)
dfW['MA7_new_cases'] = dfW.new_cases.rolling(window=7).mean()
dfW['MA7_Doubling'] = dfW.doubling_time.rolling(window=7).mean()



###### TABLE DATA ######
df2 = df.groupby('location').tail(10)
df3 = df2.groupby(['location'], as_index=False)['new_cases'].sum()
df4 = df2.groupby(['location'], as_index=False)['total_cases'].max()
df5 = df2.groupby(['location'], as_index=False)['new_deaths'].sum()
df6 = df2.groupby(['location'], as_index=False)['total_deaths'].max()
dfTOP = pd.merge(df3,df4)
dfTOP = pd.merge(dfTOP,df5)
dfTOP = pd.merge(dfTOP,df6)
dfTOP = dfTOP.sort_values(by=['new_cases'], ascending=False)
dfTOP.columns =['País', 'Casos nuevos', 'Total casos', 'Muertes nuevas','Total muertes']
###### TABLE DATA ######

dfMUND = df.query("location == ['World','United States','Canada','Mexico','Brazil', 'Peru', 'Chile', 'Argentina', 'Ecuador','Russia', 'United Kingdom', 'France', 'Spain', 'Italy', 'Germany', 'Norway', 'Finland', 'Sweden','Iran', 'Turkey', 'Saudi Arabia', 'Pakistan', 'Qatar','Bangladesh','India', 'China', 'South Korea', 'Japan', 'Taiwan', 'Australia']")
dfCA = df.query("location == ['Guatemala', 'El Salvador', 'Honduras', 'Costa Rica', 'Panama']")

dfMUND.date = pd.to_datetime(dfMUND.date, infer_datetime_format=True)
dfCA.date = pd.to_datetime(dfCA.date, infer_datetime_format=True)

# Drop world data
#df = df[df.location != 'World']
## Sort df by date

dfGT0 = df[df['location'].isin(['Guatemala'])][['location','date','total_cases','new_cases','total_deaths','new_deaths','total_tests']]
dfSLV = df[df['location'].isin(['El Salvador'])][['location','date','total_cases','new_cases','total_deaths','new_deaths','total_tests']]
dfHND = df[df['location'].isin(['Honduras'])][['location','date','total_cases','new_cases','total_deaths','new_deaths','total_tests']]
dfCR = df[df['location'].isin(['Costa Rica'])][['location','date','total_cases','new_cases','total_deaths','new_deaths','total_tests']]
dfPAN = df[df['location'].isin(['Panama'])][['location','date','total_cases','new_cases','total_deaths','new_deaths','total_tests']]
dfMX = df[df['location'].isin(['Mexico'])][['location','date','total_cases','new_cases','total_deaths','new_deaths','total_tests']]

dfGT0['days'] = range(1, len(dfGT0) + 1)
dfSLV['days'] = range(1, len(dfSLV) + 1)
dfHND['days'] = range(1, len(dfHND) + 1)
dfCR['days'] = range(1, len(dfCR) + 1)
dfPAN['days'] = range(1, len(dfPAN) + 1)
dfMX['days'] = range(1, len(dfMX) + 1)

dfGT0['tasa_acumulados'] = (dfGT0.total_cases - dfGT0.total_cases.shift(1))/dfGT0.total_cases.shift(1)
dfGT0['doubling_time'] = 70 / (dfGT0['tasa_acumulados'] * 100)
dfGT0['tasa_nuevos_casos'] = (dfGT0.new_cases - dfGT0.new_cases.shift(1))/dfGT0.new_cases.shift(1)
dfGT0['tasa_nuevos_casos'] = (dfGT0.new_cases - dfGT0.new_cases.shift(1))/dfGT0.new_cases.shift(1)
dfGT0['MA7_new_cases'] = dfGT0.new_cases.rolling(window=7).mean()
dfGT0['MA7_Doubling'] = dfGT0.doubling_time.rolling(window=7).mean()

dfSLV['tasa_acumulados'] = (dfSLV.total_cases - dfSLV.total_cases.shift(1))/dfSLV.total_cases.shift(1)
dfSLV['doubling_time'] = 70 / (dfSLV['tasa_acumulados'] * 100)
dfSLV['tasa_nuevos_casos'] = (dfSLV.new_cases - dfSLV.new_cases.shift(1))/dfSLV.new_cases.shift(1)
dfSLV['tasa_nuevos_casos'] = (dfSLV.new_cases - dfSLV.new_cases.shift(1))/dfSLV.new_cases.shift(1)
dfSLV['MA7_new_cases'] = dfSLV.new_cases.rolling(window=7).mean()
dfSLV['MA7_Doubling'] = dfSLV.doubling_time.rolling(window=7).mean()

dfHND['tasa_acumulados'] = (dfHND.total_cases - dfHND.total_cases.shift(1))/dfHND.total_cases.shift(1)
dfHND['doubling_time'] = 70 / (dfHND['tasa_acumulados'] * 100)
dfHND['tasa_nuevos_casos'] = (dfHND.new_cases - dfHND.new_cases.shift(1))/dfHND.new_cases.shift(1)
dfHND['tasa_nuevos_casos'] = (dfHND.new_cases - dfHND.new_cases.shift(1))/dfHND.new_cases.shift(1)
dfHND['MA7_new_cases'] = dfHND.new_cases.rolling(window=7).mean()
dfHND['MA7_Doubling'] = dfHND.doubling_time.rolling(window=7).mean()

dfCR['tasa_acumulados'] = (dfCR.total_cases - dfCR.total_cases.shift(1))/dfCR.total_cases.shift(1)
dfCR['doubling_time'] = 70 / (dfCR['tasa_acumulados'] * 100)
dfCR['tasa_nuevos_casos'] = (dfCR.new_cases - dfCR.new_cases.shift(1))/dfCR.new_cases.shift(1)
dfCR['tasa_nuevos_casos'] = (dfCR.new_cases - dfCR.new_cases.shift(1))/dfCR.new_cases.shift(1)
dfCR['MA7_new_cases'] = dfCR.new_cases.rolling(window=7).mean()
dfCR['MA7_Doubling'] = dfCR.doubling_time.rolling(window=7).mean()

dfPAN['tasa_acumulados'] = (dfPAN.total_cases - dfPAN.total_cases.shift(1))/dfPAN.total_cases.shift(1)
dfPAN['doubling_time'] = 70 / (dfPAN['tasa_acumulados'] * 100)
dfPAN['tasa_nuevos_casos'] = (dfPAN.new_cases - dfPAN.new_cases.shift(1))/dfPAN.new_cases.shift(1)
dfPAN['tasa_nuevos_casos'] = (dfPAN.new_cases - dfPAN.new_cases.shift(1))/dfPAN.new_cases.shift(1)
dfPAN['MA7_new_cases'] = dfPAN.new_cases.rolling(window=7).mean()
dfPAN['MA7_Doubling'] = dfPAN.doubling_time.rolling(window=7).mean()

dfMX['tasa_acumulados'] = (dfMX.total_cases - dfMX.total_cases.shift(1))/dfMX.total_cases.shift(1)
dfMX['doubling_time'] = 70 / (dfMX['tasa_acumulados'] * 100)
dfMX['tasa_nuevos_casos'] = (dfMX.new_cases - dfMX.new_cases.shift(1))/dfMX.new_cases.shift(1)
dfMX['tasa_nuevos_casos'] = (dfMX.new_cases - dfMX.new_cases.shift(1))/dfMX.new_cases.shift(1)
dfMX['MA7_new_cases'] = dfMX.new_cases.rolling(window=7).mean()
dfMX['MA7_Doubling'] = dfMX.doubling_time.rolling(window=7).mean()

################ CLEAN DATA END ################




################ PRUEBAS CA GRAPH START ################
# CR https://www.ministeriodesalud.go.cr/index.php/centro-de-prensa/noticias/741-noticias-2020/1532-lineamientos-nacionales-para-la-vigilancia-de-la-infeccion-por-coronavirus-2019-ncov
# SV https://covid19.gob.sv/
# PN https://geosocial.maps.arcgis.com/apps/opsdashboard/index.html#/2c6e932c690d467b85375af52b614472
# https://www.worldometers.info/coronavirus/
data_ca1 ={
    'pais':['Guatemala', 'El Salvador', 'Honduras', 'Costa Rica', 'Panama'],
    'pruebas':[dfGT.total_tests.sum()+98,113656, 21540, 29877, 80720],
    'tasa_por_millon_hab':[(dfGT.total_tests.sum()+(98))/16300000*1000000,
                           133151/6482286*1000000,
                           21540/9884814*1000000,
                           33282/5088445*1000000,
                           95299/4306239*1000000
                           ]
    }
data_ca = pd.DataFrame(data_ca1)
figE = px.bar(data_ca, x='pais', y='pruebas', text=data_ca.pruebas,
              hover_data=['pruebas', 'tasa_por_millon_hab'], color='tasa_por_millon_hab',
              labels={'pruebas':'Total de pruebas realizadas'}, height=400)
figE.update_layout(title_text='COVID-19 C.A.: Total de Pruebas realizadas por país al 17 de Junio',template="plotly_white",)
figE.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
################ PRUEBAS CA GRAPH END ################



################ GRAPH 1 RESUMEN GT START ################
index = list(dfGT['index'])
newcases = list(dfGT['new_cases'])

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=dfGT.date, y=dfGT.total_cases,
                    mode='lines+markers',
                    text = [f'Dias desde primer caso:{x}</br>Casos nuevos:{y}' for x,y in list(zip(index, newcases))],
                    name='Casos confirmados',
                    marker=dict(size=4+dfGT.new_cases/15, color='indianred')))
fig1.add_trace(go.Scatter(x=dfGT.date, y=dfGT.total_deaths,
                    mode='lines+markers',
                    name='Fallecidos',
                    marker=dict(color='orange')))
fig1.add_trace(go.Scatter(x=dfGT.date, y=dfGT.recovered,
                    mode='lines+markers',
                    name='Recuperados'))
fig1.add_trace(go.Scatter(x=dfGT.date, y=(dfGT.total_cases - 2 - (dfGT.recovered + dfGT.total_deaths)),
                    mode='lines+markers',
                    name='Casos activos'))
fig1.update_layout(title_text="COVID-19 Guatemala: total casos acumulados",
    hovermode="x unified",template="plotly_white",
    legend_orientation="h",legend=dict(y=-0.2, font=dict(size=14)),legend_title_text='Selección: ',
    updatemenus=[dict(type='buttons',
                      buttons=list([dict(label="Lineal",
                                         method="relayout",
                                         args=[{"yaxis.type": "linear"}]),
                                    dict(label="Log", method="relayout",
                                         args=[{"yaxis.type": "log"}]),
                                   ]),
                      direction="right", pad={"r": 10, "t": 10}, showactive=True,
                      x=0.4, xanchor="left", y=1.18, yanchor="top"
            )],
    annotations=[dict(text="ESCALA:", showarrow=False,font=dict(size=14),
                      x=0, y=1.0855, yref="paper", align="center")
    ],)
fig1.update_xaxes(nticks=20)
fig1.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
################ GRAPH 1 RESUMEN GT END ################

################ GRAPH 3 NEW CASES START ################
index3 = list(dfGT['index'])
totalcases3 = list(dfGT['total_cases'])

fig3 = go.Figure()
fig3.add_trace(go.Scatter(x=dfGT.date,y=dfGT.new_cases.rolling(window=7).mean(),mode='lines+markers',
                         name='Promedio móvil 7 dias',marker=dict(color='black',size=8),
                           text = [f'Dias desde primer caso:{x}</br>Acumulado casos:{y}' for x,y in list(zip(index3, totalcases3))]
    ))

fig3.add_trace(
    go.Bar(x=dfGT.date,y=dfGT.new_cases, name='Nuevos casos diarios',text=dfGT.new_cases,
            textposition='outside',
    ))
fig3.add_trace(go.Scatter(x=dfGT.date,y=dfGT.new_deaths.rolling(window=7).mean(),mode='lines+markers',
                         name='Promedio movil 7 dias',marker=dict(size=8),
    ))

fig3.add_trace(
    go.Bar(x=dfGT.date,y=dfGT.new_deaths, name='Nuevas muertes diarias',text=dfGT.new_deaths,
            textposition='outside',
    ))
fig3.update_layout(title_text="COVID-19 Guatemala: casos y fallecimientos nuevos diarios y su tendencia",
    hovermode="x unified",template="plotly_white",
    legend_orientation="h",legend=dict(y=-0.2, font=dict(size=14)),legend_title_text='Selección: ',
    updatemenus=[dict(type='buttons',
                      buttons=list([dict(label="Lineal",
                                         method="relayout",
                                         args=[{"yaxis.type": "linear"}]),
                                    dict(label="Log", method="relayout",
                                         args=[{"yaxis.type": "log"}]),
                                   ]),
                      direction="right", pad={"r": 10, "t": 10}, showactive=True,
                      x=0.4, xanchor="left", y=1.18, yanchor="top"
            )],
    annotations=[dict(text="ESCALA:", showarrow=False,font=dict(size=14),
                      x=0, y=1.0855, yref="paper", align="center")
    ],)
fig3.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
fig3.update_xaxes(nticks=20)
################ GRAPH 3 NEW CASES END ################

################ GRAPH 4 Tasa progresion START ################
index4 = list(dfGT['index'])
newcases4 = list(dfGT['new_cases'])
totalcases4 = list(dfGT['total_cases'])

fig4 = go.Figure()
fig4.add_trace(go.Scatter(x=dfGT.date, y=dfGT.rate_new_cases,
                    mode='lines+markers',
                    text = [f'Dias desde primer caso:{x}</br>Casos nuevos:{y}</br>Total casos:{z}' for x,y,z in list(zip(index4, newcases4, totalcases4))],
                    name='Tasa progresion casos nuevos',
                    marker=dict(size=4+dfGT.new_cases/15)))
fig4.add_trace(go.Scatter(x=dfGT.date,y=dfGT.rate_new_cases.rolling(window=7).mean(),mode='lines+markers',
                         name='Promedio movil 7 dias',marker=dict(color='red',size=8),
    ))
fig4.update_layout(title_text="COVID-19 Guatemala: tasa de crecimiento de casos nuevos",
    hovermode="x unified",template="plotly_white",
    legend_orientation="h",legend=dict(y=-0.2, font=dict(size=14)),legend_title_text='Selección: ',
    yaxis=dict(tickformat=".2%", range=[-1,1.5]))
fig4.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
fig4.update_xaxes(nticks=20)
################ GRAPH 4 Tasa progresion END ################

################ GRAPH 5 DUPLICACION START ################
index5 = list(dfGT['index'])
newcases5 = list(dfGT['new_cases'])
totalcases5 = list(dfGT['total_cases'])

fig5 = go.Figure()
fig5.add_trace(go.Scatter(x=dfGT.date, y=dfGT.doubling_time,
                    mode='lines+markers',
                    text = [f'Días desde primer caso:{x}</br>Casos nuevos:{y}</br>Total casos:{z}' for x,y,z in list(zip(index5, newcases5, totalcases5))],
                    name='Tiempo de duplicación',
                    marker=dict(size=4+dfGT.new_cases/15)))
fig5.add_trace(go.Scatter(x=dfGT.date,y=dfGT.MA7_doubling_time,mode='lines+markers',
                         name='Promedio móvil 7 días',marker=dict(color='red',size=8),
    ))
fig5.update_layout(yaxis=dict(title="Dias"), hovermode="x unified",template="plotly_white",title_text="COVID-19 Guatemala: tiempo de duplicación de casos",
                   legend_orientation="h",legend=dict(y=-0.2, font=dict(size=14)),legend_title_text='Selección: ',)
fig5.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
fig5.update_xaxes(nticks=20)
################ GRAPH 5 DUPLICACION END ################

################ GRAPH 6 PRUEBAS START ################
index6 = list(dfGT['index'])
totalcases6 = list(dfGT['total_cases'])

fig6 = go.Figure()
fig6.add_trace(
    go.Bar(x=dfGT.date,y=dfGT.new_cases/dfGT.total_tests*100, name='Positividad',
           text=round(dfGT.new_cases/dfGT.total_tests*100,2),
            textposition='auto',
    ),)
fig6.add_trace(go.Scatter(x=dfGT.date, y=dfGT.total_tests,
                    mode='lines+markers',
                    text = [f'Dias desde primer caso:{x}</br>Total casos:{z}' for x,z in list(zip(index6, totalcases6))],
                    name='Pruebas realizadas', yaxis="y2", marker=dict(size=8, color='#ff7f0e')))
fig6.add_trace(go.Scatter(x=dfGT.date,y=dfGT.new_cases,mode='lines+markers',
                         name='Casos nuevos',yaxis="y3",marker=dict(color='#d62728',size=8),
    ),)
fig6.update_layout(hovermode="x unified",template="plotly_white",title_text="COVID-19 Guatemala: pruebas realizadas, casos nuevos y positividad diaria",
                   legend_orientation="h",legend=dict(y=-0.2, font=dict(size=14)),legend_title_text='Selección: ',
                   yaxis=dict(title="Positividad",
                       titlefont=dict(color="#1f77b4"),
                       tickfont=dict(color="#1f77b4")
                   ),
                   yaxis2=dict(title="              Pruebas realizadas",
                               titlefont=dict(color="#ff7f0e"),
                       tickfont=dict(color="#ff7f0e"),
                       anchor="free", overlaying="y", side="left"
                   ),
                   yaxis3=dict(title="Casos nuevos",
                               titlefont=dict(color="#d62728"
                       ),
                       tickfont=dict(color="#d62728"),
                       anchor="x", overlaying="y", side="right"),
                   )
fig6.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
fig6.update_xaxes(nticks=20)
################ GRAPH 6 PRUEBAS END ################

################ GRAPH 66 PRUEBAS START ################
fig66 = go.Figure()
fig66.add_trace(go.Scatter(x=dfGT.date, y=dfGT.total_tests/16300000*100000,
                    mode='lines+markers',
                    text = [f'Dias desde primer caso:{x}</br>Total casos:{z}' for x,z in list(zip(index6, totalcases6))],
                    name='Pruebas realizadas', marker=dict(size=8, color='#ff7f0e')))
fig66.add_trace(go.Scatter(x=dfGT.date,y=dfGT.new_cases,mode='lines+markers',
                         name='Casos nuevos',yaxis="y2",marker=dict(color='#d62728',size=8),
    ),)
fig66.update_layout(hovermode="x unified",template="plotly_white",title_text="COVID-19 Guatemala: pruebas diarias por cada 100k hab",
                    legend_orientation="h",legend=dict(y=-0.2, font=dict(size=14)),legend_title_text='Selección: ',
                   yaxis=dict(title="Pruebas diarias por cada 100,000 habitantes",
                       titlefont=dict(color="#ff7f0e"),
                       tickfont=dict(color="#ff7f0e")),
                   yaxis2=dict(title="Nuevos casos",
                               titlefont=dict(color="#d62728"),
                       tickfont=dict(color="#d62728"),
                       anchor="x", overlaying="y", side="right"),)
fig66.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
fig66.update_xaxes(nticks=20)
################ GRAPH 66 PRUEBAS END ################

################ GRAPH 7 TESTS START ################
index7 = list(dfGT[dfGT['total_tests'] != 0]['index'])
totalcases7 = list(dfGT[dfGT['total_tests'] != 0]['total_cases'])

fig7 = go.Figure()
fig7.add_trace(go.Scatter(x=dfGT[dfGT['total_tests'] != 0]['total_tests'],
                          y=dfGT[dfGT['total_tests'] != 0]['new_cases'],
                          mode='markers',
                          name='Casos nuevos por cantidad de pruebas',
                          marker=dict(
                              color=dfGT['index'],
                              colorscale='Portland', # one of plotly colorscales
                              showscale=True,
                              size=10
                          ),
                          text = [f'Dias desde primer caso:{x}</br>Acumulado casos:{y}' for x,y in list(zip(index7, totalcases7))]
                         )
              )

fig7.update_layout(title_text="COVID-19 Guatemala: Casos nuevos diarios vs. Pruebas diarias ",template="plotly_white",
    yaxis=dict(title="Casos reportados diarios"),
                   xaxis=dict(title='Cantidad de pruebas diarias'),
                   annotations = [dict(text="El Color de los puntos representa los días desde el primer caso ", showarrow=False, font=dict(size=14),
                    x=0, y=1.0855, yref="paper", align="center")
               ],
                   xaxis_range=[0, 2800],
                   )
fig7.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
#fig7.update_xaxes(nticks=20)



index777 = list(dfGT['index'])
totalcases777 = list(dfGT['total_cases'])

fig777 = go.Figure()
fig777.add_trace(go.Scatter(x=dfGT['date'],
                          y=dfGT['new_cases']/dfGT['total_tests']*100,
                          mode='markers',
                          name='Casos nuevos por cantidad de pruebas',
                          marker=dict(
                              color=dfGT['new_cases']/dfGT['total_tests']*100,
                              colorscale='Portland', # one of plotly colorscales
                              showscale=True,
                              size=10
                          ),
                          text = [f'Dias desde primer caso:{x}</br>Acumulado casos:{y}' for x,y in list(zip(index7, totalcases7))]
                         )
              )
fig777.add_shape(type="line", x0=1, y0=10, x1=100, y1=10,opacity=0.5,
            line=dict(color="darkblue", width=2, dash="dashdot" ),)
fig777.add_shape(
            type="line", x0=1, y0=15, x1=100, y1=15,opacity=0.5,
            line=dict(color="green", width=2, dash="dashdot"),)
fig777.add_shape(
            type="line", x0=1, y0=20, x1=100, y1=20,opacity=0.5,
            line=dict(color="indianred", width=2, dash="dashdot"),)

fig777.update_layout(title_text="COVID-19 Guatemala: Índice de Positividad ",template="plotly_white",
    yaxis=dict(title="Positividad (%)"),
                   xaxis=dict(title='Fecha'),
                   legend_orientation="h", legend=dict(y=-0.2,font=dict(size=14)), legend_title_text='Selección: ')
fig777.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")],
)
fig777.update_xaxes(nticks=20)
################ GRAPH 7 TESTS END ################

################ GRAPH 8 SEXO START ################
fig8 = go.Figure()
fig8.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['men'])==False]['date'],
    y=dfGT[np.isnan(dfGT['men'])==False]['men'],
  #  hovertemplate="Dias desde primer caso:{x}</br>Acumulado casos:{y}" for x,y in list(zip(index3, totalcases3))]
    mode='lines',name='Hombres',
    line=dict(width=0.5, color='rgb(131, 90, 241)'),
    stackgroup='one', groupnorm='percent' # define stack group
))
fig8.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['women'])==False]['date'],
    y=dfGT[np.isnan(dfGT['women'])==False]['women'],
    hoverinfo='text+x+y',
    mode='lines',name='Mujeres',
    line=dict(width=0.5, color='rgb(111, 231, 219)'),
    stackgroup='one'
))
fig8.update_layout(hovermode="x unified",template="plotly_white",title_text="COVID-19 Guatemala: distribución de casos por sexo",
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
        range=[1, 100],
        ticksuffix='%'))
fig8.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])

################ GRAPH 8 SEXO START ################

################ GRAPH 8 EDAD START ################
fig9 = go.Figure()
fig9.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['0-20'])==False]['date'],
    y=dfGT[np.isnan(dfGT['0-20'])==False]['0-20'],
  #  hovertemplate="Dias desde primer caso:{x}</br>Acumulado casos:{y}" for x,y in list(zip(index3, totalcases3))]
    mode='lines',name='0-20',
    line=dict(width=0.5),
    stackgroup='one',# groupnorm='percent' # define stack group
))
fig9.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['21-40'])==False]['date'],
    y=dfGT[np.isnan(dfGT['21-40'])==False]['21-40'],
    hoverinfo='text+x+y',
    mode='lines',name='21-40',
    line=dict(width=0.5),
    stackgroup='one'
))
fig9.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['41-60'])==False]['date'],
    y=dfGT[np.isnan(dfGT['41-60'])==False]['41-60'],
    hoverinfo='text+x+y',
    mode='lines',name='41-60',
    line=dict(width=0.5),
    stackgroup='one'
))
fig9.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['61-80'])==False]['date'],
    y=dfGT[np.isnan(dfGT['61-80'])==False]['61-80'],
    hoverinfo='text+x+y',
    mode='lines',name='61-80',
    line=dict(width=0.5),
    stackgroup='one'
))
fig9.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['81+'])==False]['date'],
    y=dfGT[np.isnan(dfGT['81+'])==False]['81+'],
    hoverinfo='text+x+y',
    mode='lines',name='81+',
    line=dict(width=0.5),
    stackgroup='one'
))
fig9.update_layout(showlegend=True,hovermode="x unified",template="plotly_white",title_text="COVID-19 Guatemala: distribución de casos por edad",
    xaxis_type='category',
    yaxis=dict(type='linear',
#        range=[1, 100],
#        ticksuffix='%'
               )
                   )
fig9.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])

################ GRAPH 8 EDAD START ################
################ GRAPH 8 REGION START ################
fig10 = go.Figure()
fig10.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['region1'])==False]['date'],
    y=dfGT[np.isnan(dfGT['region1'])==False]['region1'],
  #  hovertemplate="Dias desde primer caso:{x}</br>Acumulado casos:{y}" for x,y in list(zip(index3, totalcases3))]
    mode='lines',name='región 1',
    line=dict(width=0.5),
    stackgroup='one',# groupnorm='percent' # define stack group
))
fig10.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['region2'])==False]['date'],
    y=dfGT[np.isnan(dfGT['region2'])==False]['region2'],
  #  hovertemplate="Dias desde primer caso:{x}</br>Acumulado casos:{y}" for x,y in list(zip(index3, totalcases3))]
    mode='lines',name='región 2',
    line=dict(width=0.5),
    stackgroup='one',# groupnorm='percent' # define stack group
))
fig10.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['region3'])==False]['date'],
    y=dfGT[np.isnan(dfGT['region3'])==False]['region3'],
  #  hovertemplate="Dias desde primer caso:{x}</br>Acumulado casos:{y}" for x,y in list(zip(index3, totalcases3))]
    mode='lines',name='región 3',
    line=dict(width=0.5),
    stackgroup='one',# groupnorm='percent' # define stack group
))
fig10.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['region4'])==False]['date'],
    y=dfGT[np.isnan(dfGT['region4'])==False]['region4'],
  #  hovertemplate="Dias desde primer caso:{x}</br>Acumulado casos:{y}" for x,y in list(zip(index3, totalcases3))]
    mode='lines',name='región 4',
    line=dict(width=0.5),
    stackgroup='one',# groupnorm='percent' # define stack group
))
fig10.add_trace(go.Scatter(
    x=dfGT[np.isnan(dfGT['region5'])==False]['date'],
    y=dfGT[np.isnan(dfGT['region5'])==False]['region5'],
  #  hovertemplate="Dias desde primer caso:{x}</br>Acumulado casos:{y}" for x,y in list(zip(index3, totalcases3))]
    mode='lines',name='región 5',
    line=dict(width=0.5),
    stackgroup='one',# groupnorm='percent' # define stack group
))
fig10.update_layout(hovermode="x unified",template="plotly_white",title_text="COVID-19 Guatemala: distribución de casos por región",
    showlegend=True,
    xaxis_type='category',
    yaxis=dict(
        type='linear',
    )
                    )
fig10.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])


################ WORLD NEW CASES  START ################
figCOMP = go.Figure()
for name1, group in dfCA.groupby('location'):
    figCOMP.add_trace(go.Scatter(x=dfCA[dfCA['location']==name1]['date'], y=dfCA[dfCA['location']==name1].new_cases.rolling(window=7).mean(),
                        mode='lines+markers',name=name1,
                        marker=dict(size=3)))
for name0, group in dfMUND.groupby('location'):
    figCOMP.add_trace(go.Scatter(x=dfMUND[dfMUND['location']==name0]['date'], y=dfMUND[dfMUND['location']==name0].new_cases.rolling(window=7).mean(),
                        mode='lines+markers', visible='legendonly',
                        name=name0,
                        marker=dict(size=3)))

figCOMP.update_layout(
    xaxis_range=[datetime.datetime(2020, 1, 1), datetime.datetime(2020, 6, 30)],
    title_text="COVID-19 MUNDIAL: casos nuevos diarios (promedio móvil 7-días)",template="plotly_white",
    updatemenus=[dict(type='buttons',
                      buttons=list([dict(label="Linear",
                                         method="relayout",
                                         args=[{"yaxis.type": "linear"}]),
                                    dict(label="Log", method="relayout",
                                         args=[{"yaxis.type": "log"}]),
                                   ]),
                      direction="right", pad={"r": 10, "t": 10}, showactive=True,
                      x=0.1, xanchor="left", y=1.18, yanchor="top"
            )],
    annotations=[dict(text="ESCALA:", showarrow=False,font=dict(size=14),
                      x=0, y=1.085, yref="paper", align="center")
    ],)
figCOMP.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
################ WORLD NEW CASES  END ################

################ WORLD NEW DEATHS START ################
figCOMP2 = go.Figure()
for name1, group in dfCA.groupby('location'):
    figCOMP2.add_trace(go.Scatter(x=dfCA[dfCA['location']==name1]['date'],
                                  y=dfCA[dfCA['location']==name1].new_deaths.rolling(window=7).mean(),
                        mode='lines+markers',name=name1,
                        marker=dict(size=3)))
for name0, group in dfMUND.groupby('location'):
    figCOMP2.add_trace(go.Scatter(x=dfMUND[dfMUND['location']==name0]['date'],
                                  y=dfMUND[dfMUND['location']==name0].new_deaths.rolling(window=7).mean(),
                        mode='lines+markers', visible='legendonly',
                        name=name0,
                        marker=dict(size=3)))

figCOMP2.update_layout(
    xaxis_range=[datetime.datetime(2020, 1, 1), datetime.datetime(2020, 6, 30)],
    title_text="COVID-19 MUNDIAL: Muertes diarias (promedio móvil 7-días)",template="plotly_white",
    updatemenus=[dict(type='buttons',
                      buttons=list([dict(label="Linear",
                                         method="relayout",
                                         args=[{"yaxis.type": "linear"}]),
                                    dict(label="Log", method="relayout",
                                         args=[{"yaxis.type": "log"}]),
                                   ]),
                      direction="right", pad={"r": 10, "t": 10}, showactive=True,
                      x=0.1, xanchor="left", y=1.18, yanchor="top"
            )],
    annotations=[dict(text="ESCALA:", showarrow=False,font=dict(size=14),
                      x=0, y=1.085, yref="paper", align="center")
    ],)
figCOMP2.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
################ WORLD NEW DEATHS END ################


################ WORLD TOTAL CASES  START ################
figCOMP3 = go.Figure()
for name1, group in dfCA.groupby('location'):
    figCOMP3.add_trace(go.Scatter(x=dfCA[dfCA['location']==name1]['date'], y=dfCA[dfCA['location']==name1]['total_cases'],
                        mode='lines+markers',name=name1,
                        marker=dict(size=3)))
for name0, group in dfMUND.groupby('location'):
    figCOMP3.add_trace(go.Scatter(x=dfMUND[dfMUND['location']==name0]['date'], y=dfMUND[dfMUND['location']==name0]['total_cases'],
                        mode='lines+markers', visible='legendonly',
                        name=name0,
                        marker=dict(size=3)))

figCOMP3.update_layout(
    xaxis_range=[datetime.datetime(2020, 1, 1), datetime.datetime(2020, 6, 30)],
    title_text="COVID-19 MUNDIAL: total de casos detectados",template="plotly_white",
    updatemenus=[dict(type='buttons',
                      buttons=list([dict(label="Linear",
                                         method="relayout",
                                         args=[{"yaxis.type": "linear"}]),
                                    dict(label="Log", method="relayout",
                                         args=[{"yaxis.type": "log"}]),
                                   ]),
                      direction="right", pad={"r": 10, "t": 10}, showactive=True,
                      x=0.1, xanchor="left", y=1.18, yanchor="top"
            )],
    annotations=[dict(text="ESCALA:", showarrow=False,font=dict(size=14),
                      x=0, y=1.085, yref="paper", align="center")
    ],)
figCOMP3.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
################ WORLD TOTAL CASES  END ################

################ WORLD TOTAL DEATHS START ################
figCOMP4 = go.Figure()
for name1, group in dfCA.groupby('location'):
    figCOMP4.add_trace(go.Scatter(x=dfCA[dfCA['location']==name1]['date'],
                                  y=dfCA[dfCA['location']==name1]['total_deaths'],
                        mode='lines+markers',name=name1,
                        marker=dict(size=3)))
for name0, group in dfMUND.groupby('location'):
    figCOMP4.add_trace(go.Scatter(x=dfMUND[dfMUND['location']==name0]['date'],
                                  y=dfMUND[dfMUND['location']==name0]['total_deaths'],
                        mode='lines+markers', visible='legendonly',
                        name=name0,
                        marker=dict(size=3)))

figCOMP4.update_layout(
    xaxis_range=[datetime.datetime(2020, 1, 1), datetime.datetime(2020, 6, 30)],
    title_text="COVID-19 MUNDIAL: total fallecimientos ",template="plotly_white",
    updatemenus=[dict(type='buttons',
                      buttons=list([dict(label="Linear",
                                         method="relayout",
                                         args=[{"yaxis.type": "linear"}]),
                                    dict(label="Log", method="relayout",
                                         args=[{"yaxis.type": "log"}]),
                                   ]),
                      direction="right", pad={"r": 10, "t": 10}, showactive=True,
                      x=0.1, xanchor="left", y=1.18, yanchor="top"
            )],
    annotations=[dict(text="ESCALA:", showarrow=False,font=dict(size=14),
                      x=0, y=1.085, yref="paper", align="center")
    ],)
figCOMP4.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])
################ WORLD TOTAL DEATHS END ################

fig999 = go.Figure()
fig999.add_trace(
    go.Bar(x=dfedad['GRUPOS DE EDAD'],
           y=round(dfedad['Tfallecidos12']/dfedad['Tpruebas12']*100,2),
           name='Letalidad',
           text=round(dfedad.Tfallecidos12/dfedad.Tpruebas12*100,2),
            textposition='auto',
    ),)
fig999.add_trace(go.Scatter(x=dfedad['GRUPOS DE EDAD'], y=dfedad["Tpruebas12"],
                        mode='lines+markers', name="Pruebas realizadas",yaxis="y2",
                        marker=dict(size=3)))
fig999.add_trace(go.Scatter(x=dfedad['GRUPOS DE EDAD'], y=dfedad["Tfallecidos12"],
                        mode='lines+markers', name="Fallecidos",
                        marker=dict(size=3)))
fig999.add_trace(go.Scatter(x=dfedad['GRUPOS DE EDAD'], y=dfedad["Tpositivos12"],
                        mode='lines+markers', name="Positivos",yaxis="y2",
                        marker=dict(size=3)))

fig999.update_layout(hovermode="x unified",
                  title_text="COVID-19 GUATEMALA: CASOS POR GRUPO DE EDAD AL 12 DE JUNIO",
                  legend_title_text='Selección: ',legend_orientation="h",legend=dict(y=-.2, font=dict(size=16)),
                  yaxis=dict(title="FALLECIDOS Y LETALIDAD"),template="plotly_white",
                  yaxis2=dict(title="TOTAL DE PRUEBAS Y CASOS", anchor="x", overlaying="y", side="right")
                 )
fig999.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])


dfdeps = dfdeps.sort_values(by='tasa por 100k hab', ascending=False)

figDEPS = px.bar(
    dfdeps, x='departamento',
    y='cantidad', text='cantidad',
    color='tasa por 100k hab',color_continuous_scale='Portland',
             )
figDEPS.update_layout(title_text='COVID-19 GUATEMALA: Casos por departamento',template="plotly_white",)
figDEPS.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0.3, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])

figdfdepsTOT = go.Figure()
for i in ('GUATEMALA','SAN MARCOS','QUETZALTENANGO','SUCHITEPEQUEZ','SOLOLA','ESCUINTLA',
          'SACATEPEQUEZ','CHIMALTENANGO','SANTA ROSA','CHIQUIMULA','IZABAL','HUEHUETENANGO',
          'ALTA VERAPAZ','PROGRESO','TOTONICAPAN','JUTIAPA','QUICHE','RETALHULEU','PETEN',
          'BAJA VERAPAZ','ZACAPA','JALAPA'):
    figdfdepsTOT.add_trace(go.Scatter(x=dfdepsTOT['FECHA'], y=dfdepsTOT[i],
                        mode='lines+markers', name=i,
                        marker=dict(size=3)))


figdfdepsTOT.update_layout(
    xaxis_range=[datetime.datetime(2020, 1, 1), datetime.datetime(2020, 6, 30)],
    title_text="COVID-19 GUATEMALA: CASOS POR DEPARTAMENTO",template="plotly_white",
    updatemenus=[dict(buttons=list([dict(label="Linear",
                                         method="relayout",
                                         args=[{"yaxis.type": "linear"}]),
                                    dict(label="Log", method="relayout",
                                         args=[{"yaxis.type": "log"}]),
                                   ]),
                      direction="down", pad={"r": 10, "t": 10}, showactive=True,
                      x=0.1, xanchor="left", y=1.18, yanchor="top"
            )],
    annotations=[dict(text="ESCALA:", showarrow=False,font=dict(size=14),
                      x=0, y=1.085, yref="paper", align="center")
    ],)
figdfdepsTOT.update_layout(images= [dict(source='data:image/png;base64,{}'.format(encoded_image4.decode()),
                                 xref="paper", yref="paper", x=0, y=1, sizex=0.4, sizey=0.4,xanchor="left",
                                 yanchor="top",opacity=0.25, layer="above")])

image_filename1 = 'logo.PNG' # replace with your own image
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())


temp = round(dfGT['doubling_time'].tail(7).mean(), 2)
temp2 = round(dfGT.drop(dfGT.tail(7).index)['doubling_time'].tail(7).mean(), 2)
temp3 =  '{0:,}'.format(round(dfGT['new_cases'].tail(7).sum(), 2))
temp4 = '{0:,}'.format(round(dfGT.drop(dfGT.tail(7).index)['new_cases'].tail(7).sum(), 2))
temp5 = '{0:,}'.format(round(dfGT['new_deaths'].tail(7).sum(), 2))
temp6 = '{0:,}'.format(round(dfGT.drop(dfGT.tail(7).index)['new_deaths'].tail(7).sum(), 2))
temp00 = dfGT.iloc[len(dfGT) - 1, 2]
temp01 = dfGT.iloc[len(dfGT) - 7, 2]
temp02 = dfGT.drop(dfGT.tail(12).index).iloc[len(dfGT) - 14, 2]
temp03 = dfGT.iloc[len(dfGT) - 8, 2]
aux1 = '{0:,}'.format(dfGT.total_deaths.max())
aux2 = '{0:,}'.format(round(dfGT.total_deaths.max()/dfGT.total_cases.max()*100,2))
################ APP ################
########### LAYOUT ###########
app.layout = html.Div([
########### INDICADORES
            html.Div([
                html.Hr(),
                html.H3("RESUMEN DE CASOS COVID-19 DETECTADOS EN GUATEMALA AL: {}".format(dfGT.iloc[len(dfGT) - 1, 1]),style={'textAlign': 'Left'}),
            ], className="container"),
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.Br(),
                        html.H5("TOTAL DE CASOS",style={'textAlign': 'center'}),
                        html.H2("{0:,}".format(dfGT.total_cases.max()),style={'textAlign': 'center',"font-weight": "bold","color":"red"}),
                        html.H5("TOTAL FALLECIDOS Y LETALIDAD", style={'textAlign': 'center'}),
                        html.H2("{} - {}%".format(aux1, aux2),
                                style={'textAlign': 'center', "font-weight": "bold", "color": "red"}),
                    ]), width=5),
                    dbc.Col(html.Div([
                        html.Br(),
                        html.H6("COMPARACIÓN INDICADORES:",style={'textAlign': 'center',"font-weight": "bold"}),
                        html.H6("últimos 7 días ({}-{} Junio)".format(temp01,temp00),style={'textAlign': 'center'}),
                        html.H6("vs. 7 días antes ({}-{} Junio)".format(temp02, temp03),style={'textAlign': 'center'}),
                        #html.H6("ÚLTIMOS 7 DÍAS vs. 7 DÍAS ANTERIORES",style={'textAlign': 'center',"font-weight": "bold"}),
                        html.Br(),
                        html.H6("TIEMPO DUPLICACIÓN (DÍAS)",style={'textAlign': 'center'}),
                        html.H3("{} vs. {}".format(temp,temp2),style={'textAlign': 'center',"font-weight": "bold","color":"indianred"}),
                    ]), width=5),
                ],justify="center",),
            ], className="container"),
            html.Div([
                dbc.Row([
                    dbc.Col(html.Div([
                        html.H5("CASOS NUEVOS ESTE DÍA",style={'textAlign': 'center'}),
                        html.H2("{0:,}".format(dfGT.iloc[len(dfGT) - 1, 7]),style={'textAlign': 'center', "font-weight": "bold", "color": "red"}),
                        html.H5("FALLECIDOS ESTE DÍA", style={'textAlign': 'center'}),
                        html.H2("{0:,}".format(dfGT.iloc[len(dfGT) - 1, 9]),style={'textAlign': 'center', "font-weight": "bold", "color": "red"}),
                    ]), width=5),
                    dbc.Col(html.Div([
                       # html.Br(),
                        html.H6("CASOS NUEVOS", style={'textAlign': 'center'}),
                        html.H3("{} vs. {}".format(temp3, temp4),style={'textAlign': 'center', "font-weight": "bold", "color": "indianred"}),
                        html.H6("FALLECIDOS", style={'textAlign': 'center'}),
                        html.H3("{} vs. {}".format(temp5, temp6   ),style={'textAlign': 'center', "font-weight": "bold", "color": "indianred"}),

                    ]), width=5),
                ], justify="center", ),
            ], className="container"),
########### INTRO
            html.Div([
                html.Hr(),
                html.H3("INSTRUCCIONES", style={'textAlign': 'Left'}),
                    ], className="container"),
            html.Div(
                [
                    dbc.Row(
                        dbc.Col(
                            html.Div("Este tablero se crea a partir de los datos reportados por el Gobierno de Guatemala y otras fuentes oficiales. "
                                     "En ese sentido, presenta información sobre casos detectados, sujeto a la limitaciones "
                                     "de la cantidad de muestras realizadas. Para conocer más sobre los indicadores utilizados, visita la sección de SOBRE EL DASHBOARD."),
                            width={"size": 8, "offset": 2},
                        ),
                    ),
                    html.Br(),
                    dbc.Row(
                        dbc.Col(
                            html.Div(
                                "En las gráficas, usando el menú puedes cambiar entre escala lineal y logarítmica. "
                                "Con la leyenda, puedes seleccionar las gráficas a desplegar u ocultar. "
                                "Usando el mouse, puedes hacer zoom en un área o seleccionar el periodo a desplegar y "
                                "con el menú en la esquina superior derecha de cada gráfica, puedes descargar la gráfica como imagen, o regresar a la escala original (Autoscale)"),
                            width={"size": 8, "offset": 2},
                        ),
                    ),
                ]
            ),
            html.Div([
                html.Br(),
                html.Img(
                    src='data:image/png;base64,{}'.format(encoded_image1.decode()),title='menú',
                    style={'border': 'thin grey solid'
                           }),html.Br()
            ],style={'textAlign':'center'}),
########### GRAPH 1
            html.Div([
                html.Hr(),
                html.H3("TOTAL DE CASOS ACUMULADOS", style={'textAlign': 'Left'}),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Casos activos = total de casos - fallecidos - recuperados",html.Br(),
                                "El tamaño de los círculos representa la cantidad de casos diarios. Mientras más grande el círculo, más casos hubo ese día."]),
                    ],body=True,)),
                ],align="center",),
                dbc.Col(dcc.Graph(figure=fig1)),
            ], className="container"),
########### GRAPH 2
            html.Div([
                html.Hr(),
                html.H3("CASOS NUEVOS DIARIOS", style={'textAlign': 'Left'}),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Casos y fallecimientos nuevos confirmados cada día",html.Br(),
                                "Ya que este número varía bastante día a día, la línea roja representa la tendencia "
                                "general utilizando promedio móvil de 7 días. Más información sobre promedios móviles en la sección de SOBRE EL DASHBOARD"]),
                    ],body=True,)),
                ],align="center",),
                dbc.Col(dcc.Graph(figure=fig3)),
            ], className="container"),
########### GRAPH 3
            html.Div([
                html.Hr(),
                html.H3("TASA DE PROGRESIÓN DE CASOS NUEVOS DIARIOS", style={'textAlign': 'Left'}),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Este indicador responde a la pregunta: ¿la cantidad de casos "
                                "nuevos está accelerando o ralentizando? en rojo la tendencia general con promedio móvil de 7 días. "
                                "El tamaño de los círculos representa la cantidad de casos diarios.",html.Br(),
                               "Cómo leer la gráfica: el 17 de mayo, hubo 24% más casos "
                               "que el día anterior, y en promedio los casos crecen un 13% diario"]),
                    ],body=True,)),
                ],align="center",),
                dbc.Col(dcc.Graph(figure=fig4)),
            ], className="container"),
########### GRAPH 4
            html.Div([
                html.Hr(),
                html.H3("TIEMPO DE DUPLICACIÓN", style={'textAlign': 'Left'}),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Este indicador indica la cantidad de días que toma duplicar los casos. En rojo, "
                                "la tendencia general con promedio móvil de 7 días.",html.Br(),
                                "Mientras más bajo sea el tiempo de duplicación más rapido está creciendo la epidemia. "
                                "Las medidas de distanciamiento social buscan aumentar el tiempo duplicación. Más información sobre este indicador en la sección de SOBRE EL DASHBOARD"]),
                    ],body=True,)),
                ],align="center",),
                dbc.Col(dcc.Graph(figure=fig5)),
            ], className="container"),
########### GRAPH 5
            html.Div([
                html.Hr(),
                html.H3("POSITIVIDAD (CASOS NUEVOS / PRUEBAS REALIZADAS)", style={'textAlign': 'Left'}),
                html.Div([
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.Br(),
                            html.H5("TOTAL PRUEBAS A LA FECHA", style={'textAlign': 'center'}),
                            html.H2("{0:,}".format(dfGT.total_tests.sum() + 98),
                                    style={'textAlign': 'center', "font-weight": "bold", "color": "indianred"}),
                            html.H5("PRUEBAS REALIZADAS EL: {}".format(dfGT.iloc[len(dfGT) - 1, 1]), style={'textAlign': 'center'}),
                            html.H3("{0:,}".format(dfGT.iloc[len(dfGT) - 1, 21]),
                                    style={'textAlign': 'center', "font-weight": "bold", "color": "red"}),
                        ]), width=5),
                        dbc.Col(html.Div([
                            html.Br(),
                            html.H5("TOTAL PRUEBAS POR 1Millón hab", style={'textAlign': 'center'}),
                            html.H2("{0:,}".format(round(((dfGT.total_tests.sum() + 98)/16300000*1000000), 2)),
                                    style={'textAlign': 'center', "font-weight": "bold", "color": "indianred"}),
                            html.H5("PRUEBAS DIARIAS POR /100k hab", style={'textAlign': 'center'}),
                            html.H3("{0:,}".format(round((dfGT.iloc[len(dfGT) - 1, 21]/16300000*100000), 2)),
                                    style={'textAlign': 'center', "font-weight": "bold", "color": "red"}),
                        ]), width=5),
                    ], justify="center", ),
                ], className="container"),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["En esta sección, presentamos la cantidad de pruebas diarias realizadas tal y como el Gobierno de Guatemala "
                                "las reporta en las conferencias de prensa.",html.Br(),
                                "La positividad es la relación entre cantidad de casos nuevos detectados y cantidad de pruebas realizadas: "
                                "Positividad = casos nuevos diarios detectados / total diario de pruebas realizadas.  "
                                "Es decir el porcentaje de pruebas positivas entre el total de pruebas realizadas.",html.Br(),
                                ]),
                    ],body=True,)),
                ],align="center",),
                dbc.Col(dcc.Graph(figure=fig6)),
            ], className="container"),
########### GRAPH 66
            html.Div([
                html.Hr(),
                html.H3("PRUEBAS DIARIAS POR CADA 100,000 HABITANTES", style={'textAlign': 'Left'}),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Cantidad de pruebas realizadas a diario por cada 100,000 habitantes "
                                "según información del total de pruebas diarias de las conferencias de prensa.", html.Br(),
                                "Como marco de referencia, hasta principios de Junio, "
                                "Estados Unidos realiza en promedio, 161 pruebas diarias por cada 100k habitantes; "
                                "Alemania 65 pruebas diarias por cada 100k habitantes; "
                                "El Salvador 37 pruebas diarias por cada 100k habitantes; "
                                "Panamá 29 pruebas diarias por cada 100k habitantes.  ",
                                html.A("FUENTE ",
                                       href='https://ourworldindata.org/grapher/daily-tests-per-thousand-people-smoothed-7-day?tab=chart&time=2020-04-17..&country=SLV~CRI~PAN~MEX~USA~DEU',target='_blank'),
                                ]),
                    ],body=True,)),
                ],align="center",),
                dbc.Col(dcc.Graph(figure=fig66)),
            ], className="container"),
########### GRAPH 7
            html.Div([
                html.Hr(),
                html.H3("CASOS NUEVOS POR PRUEBAS REALIZADAS", style={'textAlign': 'Left'}),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Casos confirmados diarios vs. pruebas realizadas diarias anunciadas en conferencia de prensa. "
                                "A más pruebas, más casos identificados. ",html.Br(),html.Br(),
                                "En la gráfica, el color representa los días que han pasado desde el primer caso."
                                ]),
                    ],body=True,),md=3),
                    dbc.Col(dcc.Graph(figure=fig7),md=9),
                ],align="center",),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P([
                            "Índice de positividad diaria: casos confirmados/pruebas realizadas anunciadas en conferencia de prensa.", html.Br(),
                            "Según el acuerdo 146-2020 del Ministerio de Salud, la positividad es uno de los indicadores para ir abriendo la economía:", html.Br(),
                            " fase 0: menos del veinte por ciento", html.Br(),
                            " fase I: menos del quince por ciento", html.Br(),
                            " fase II y III: menos del 10", html.Br(),

                                   ]),
                    ], body=True, ), md=3),
                    dbc.Col(dcc.Graph(figure=fig777), md=9),
                ], align="center", )
            ], className="container"),
########### GRAPH 10
            html.Div([
                html.Hr(),
                html.H3("DISTRIBUCIÓN DE CASOS POR REGIÓN", style={'textAlign': 'Left'}),
                html.P(["región 1: Guatemala, Chimaltenango y Sacatepéquez",html.Br(),
                        "región 2: Quetzaltenango, Huehuetenango, Totonicapán y San Marcos",html.Br(),
                        "región 3: Izabal, Zacapa, Chiquimula, Jalapa y El Progreso",html.Br(),
                        "región 4: Jutiapa, Santa Rosa, Escuintla, Suchitepéquez y Retalhuleu",html.Br(),
                        "región 5: Alta y Baja Verapaz, Petén, Quiché y Sololá)"]),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Ojo:"]),
                        html.A('La información oficial no refleja la realidad',href='https://ojoconmipisto.com/covid-19-la-informacion-oficial-no-refleja-la-realidad/',target='_blank'),
                    ],body=True,),md=3),
                    dbc.Col(dcc.Graph(figure=fig10),md=9),
                ],align="center",),

                html.H3("DISTRIBUCIÓN DE CASOS POR DEPARTAMENTO", style={'textAlign': 'Left'}),
                dbc.Col(dcc.Graph(figure=figDEPS)),
                dbc.Col(dcc.Graph(figure=figdfdepsTOT)),
                html.Div([
                    html.Hr(),
                    html.H3("Distribución de casos por municipio", style={'textAlign': 'Left'}),
                    dbc.Row([
                        dbc.Col(dbc.Card([
                            html.P([
                                "La siguiente tabla presenta la cantidad total de casos detectados para cada "
                                "municipio según fuentes oficiales hasta el 12 de Junio. ", html.A('Ojo, ',href='https://ojoconmipisto.com/covid-19-la-informacion-oficial-no-refleja-la-realidad/',target='_blank'),
                                "esta tabla se crea a partir de la información oficial que recopila lugar de residencia, no lugar de contagio. ", html.Br(),html.Br(),
                                "Cómo usar la tabla: Para buscar por DEPARTAMENTO o MUNICIPIO, busca con el nombre en MAYUSCULAS y SIN TILDES. Usando las flechas, "
                                "puedes ordenar de mayor a menos por cantidad de casos. "
                                       ]),
                            #4739 - 3337
                        ], body=True, ), md=12),
                    ], align="center", )
                ], className="container"),
                html.Div([
                    dbc.Row([
                        dbc.Col(
                            dash_table.DataTable(
                                id='DISTRIBUCIÓN DE CASOS POR MUNICIPIO',
                                style_as_list_view=True,
                                # columns=[{"name":i, "id":i,"selectable": True,} for i in dfTOP.columns],
                                columns=[{"name": i, "id": i} for i in dfmun.columns],
                                data=dfmun.to_dict('records'),
                                style_cell={'textAlign': 'left'},
                                style_header={'fontWeight': 'bold','backgroundColor': 'rgb(200, 200, 200)'},
                                style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': 'rgb(230, 230, 230)'},],
                                style_cell_conditional=[
                                    {'if': {'column_id': 'DEPARTAMENTO'}, 'textAlign': 'center'},
                                  #  {'if': {'filter_query': '{DEPARTAMENTO} = {Date}','column_id': 'DEPARTAMENTO'},'backgroundColor': 'tomato','color': 'white'},
                                ],
                                filter_action="native",
                                sort_action="native",
                               page_action="native",
                                style_table={'height': '500px', 'overflowY': 'auto'}
                            ),
                            width=12,
                        ),
                    ], justify="center"),
                ], className="container"),
            ], className="container"),
########### GRAPH 9
            html.Div([
                html.Hr(),
                html.H3("DISTRIBUCIÓN DE CASOS POR EDAD", style={'textAlign': 'Left'}),
                html.Br(),
                html.Div([
                    dcc.Graph(figure=fig999),
                    dcc.Graph(figure=fig9),
                ], style={'width': '100%', 'display': 'inline-block'})
            ], className="container", ),
########### GRAPH 8
            html.Div([
                html.Hr(),
                html.H3("DISTRIBUCIÓN DE CASOS POR SEXO", style={'textAlign': 'Left'}),
                dbc.Row([
                    dbc.Col(dbc.Card([
                        html.P(["Esta gráfica muestra la proporcio de casos que son Hombres o Mujeres en el total de casos acumulados cada día. "]),
                    ],body=True,),md=3),
                    dbc.Col(dcc.Graph(figure=fig8),md=9),
                ],align="center",)
            ], className="container"),
])

if __name__ == '__main__':
    app.run_server(debug=True)