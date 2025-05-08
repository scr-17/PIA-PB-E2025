#IMPORTANTE
#Antes de ejecutar el código, asegurarse de tener instaladas las librerías de requests, pandas, datetime, y matplotlib y poseer el archivo PIA_modulo.py

from PIA_modulo import conexion_banxico, procesar_datos, guardar_excel, leer_llave
#Desde el código de los modulos, importamos las funciones

import matplotlib.pyplot as plt
#Importamos matplotlib para graficar

serie = "SP30578"
fecha_inicio = "2000-01-01"
fecha_fin = "2024-12-31"
#Designamos los parametros que irán en la solicitud a la API

ruta_llave = input("Ingrese la ruta de la llave")
#Solicitamos la ruta a la llave para el uso del API

key = str(leer_llave(ruta_llave))

datos_json = conexion_banxico(serie, fecha_inicio, fecha_fin, key)
#Con los datos antes definidos, se mandan en la función para recuperar datos de la API del Banco de México

if datos_json:
#Realizamos un if-else para verificar que se encuentran los datos, si la función no regresó nada, se imprime un mensaje de error

	dataframe = procesar_datos(datos_json)
	#Con los datos recuperados, los convertimos a un dataframe de pandas

	guardar_excel(dataframe)
	#Con el dataframe de pandas, exportamos a un documento de excel

	media = dataframe["dato"].mean()
	mediana = dataframe["dato"].median()
	desviacion = dataframe["dato"].std()
	#Realizamos los calculos estadísticos con los valores recuperados

	print("\nCalculos estadísticos\n")
	print(f"Media: {media:.4f}%")
	print(f"Mediana: {mediana:.4f}%")
	print(f"Desviación estándar: {desviacion:.4f}%")
	#Imprimimos el resultado de los calculos

	plt.figure(figsize=(10, 6))
	plt.plot(dataframe["fecha"], dataframe["dato"], marker="o", linestyle="-", color="orange")
	plt.title("Evolución de la Inflación en México en el periodo de 2000-2024\n", fontsize=16, color="blue")
	plt.xlabel("\nAño", fontsize=9)
	plt.ylabel("Indice de Precios al Consumidor (%)\n", fontsize=9)
	plt.grid(True, linestyle="-")
	plt.savefig("inflacion.png")
	plt.show()
	#Utilizamos funciones de matplotlib para crear la gráfica, figure para definir el tamaño, plot para designar los valores y estilos...
	#x/ylabel para darle título a los ejes, grid para la cuadrícula que se muestra debajo la lónea, savefig para guardar como foto y show para mostrar 
	
else:

	print("Error, no se pudieron recuperar los datos")
