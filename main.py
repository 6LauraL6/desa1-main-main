import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium

df=pd.read_csv('DESA.csv')

"""Explicación del contexto:
    CSV, el cual registra los Desfibriladores semiautomáticos externos situados fuera del ámbito sanitario en la comunidad de galicia.

    Explicar las columnas:
    vcodequipo(Número del dispositivo), solicitante(El establecimiento que lo solicita), ubicacion(Nombre de establecimiento donde se encuentra el dispositivo), 
    municipio(Donde se encuentra el dispositivo), provincia(Donde se encuentra el dispositivo), lat(Latitud de la ubicación del dispositivo), 
    lon(Longitud de la ubicación del dispositivo), tipoInstalacion(Tipo de establecimiento donde se encuentra el dispositivo)
"""
#Cuántas filas hay
num_filas = len(df)
print(f'Número de filas en el dataset: {num_filas}')
#Se muestra la cantidad de filas en el conjunto de datos.

nas_por_columna = df.isna().sum()
print('Valores faltantes por columna:')
print(nas_por_columna)
#Se analizan los valores faltantes en cada columna del conjunto de datos.

#Outliers e inconsistencias

df_interes=df[df['provincia']== 'PONTEVEDRA']
print(df_interes)
#Se filtran los datos para la provincia de Pontevedra y se muestra el DataFrame resultante.

#Guarda el dataframe arreglado en un archivo CSV nuevo
df_interes.to_csv('equipos_pontevedra.csv',index=False)
#Se guarda el DataFrame filtrado en un archivo CSV llamado 'equipos_pontevedra.csv'.


# Preguntas
#1 ¿Cuál es la distribución geográfica de los equipos en la provincia de Pontevedra?

# Graficar la distribución geográfica
plt.scatter(df['lon'],df['lat'], color='#48bfe3')
plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Distribució Geográfica de Equipos')
plt.savefig('distribusion_geografica.png')
#Se genera un gráfico de dispersión para visualizar la distribución geográfica de los equipos en Pontevedra y se guarda como 'distribucion_geografica.png'.

#2 ¿Cuál es la cantidad de equipos por tipo de instalación?

# Graficar la cantidad de equipos por tipo de instalación
# Reemplazar el gráfico de barras por un gráfico de líneas para la cantidad de equipos por tipo de instalación
plt.figure(figsize=(10, 6))
equipos_por_tipo = df['tipoInstalacion'].value_counts().sort_index()
equipos_por_tipo.plot(kind='line', marker='o', color='#72efdd', linestyle='-')
plt.xlabel('Tipo de Instalación')
plt.ylabel('Cantidad de Equipos')
plt.title('Cantidad de Equipos por Tipo de Instalación')
plt.xticks(rotation=90)
plt.savefig('equipos_por_tipo_line.png')



#3 ¿Cuál es la ubicación con mayor concentración de equipos?

# Encontrar la ubicación con mayor concentración de equipos
ubicacion_con_mas_equipos = df['ubicacion'].value_counts().idxmax()
print(f'Ubicación con más equipos: {ubicacion_con_mas_equipos}')
#Se identifica la ubicación con la mayor concentración de equipos y se muestra en la salida.

#4  ¿Cuál es la distribución de los equipos por municipio en la provincia de Pontevedra?

# Contar la cantidad de equipos por provincia
equipos_por_provincia = df['provincia'].value_counts()

# Graficar la distribución de equipos por provincia
plt.figure(figsize=(10, 6))
equipos_por_provincia.plot(kind='bar',color='#5e60ce')
plt.xlabel('Provincia')
plt.ylabel('Cantidad de Equipos')
plt.title('Distribución de Equipos por Provincia')
plt.xticks(rotation=45)
plt.savefig('equipos_por_provincia.png')


# Crear un mapa centrado en la provincia de Pontevedra
mapa = folium.Map(location=[42.431, -8.644], zoom_start=10)

# Iterar a través de los datos y agregar marcadores al mapa con letras más grandes en el popup
for index, row in df_interes.iterrows():
    ubicacion = (row['lat'], row['lon'])
    texto_popup = f"<div style='font-size: 20px;'><b>{row['ubicacion']}</b></div>"  # Establece el tamaño de fuente en 20px y el texto en negrita
    folium.Marker(location=ubicacion, popup=texto_popup).add_to(mapa)

# Guardar el mapa en un archivo HTML
mapa.save('mapa_dispositivos_pontevedra.html')
