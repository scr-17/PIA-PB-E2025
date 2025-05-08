#IMPORTANTE
#Este código es un modulo del script principal PIA_script.py, asegurese de estar en posesión de el, a su vez de tener descargadas las librerías de requests, pandas, datetime, y matplotlib

import requests
import json
import pandas
#Se importan los modulos principales con los que se trabajará, requests para solicitar información, json para convertir los datos y pandas para manejarlos

from datetime import datetime
#Importamos datetime para poder trabajar con las fechas en vez de tomarlo como valor str

def leer_llave(ruta):
	with open(ruta, "r") as archivo:
		llave = archivo.read()
	return llave 
	

def conexion_banxico(serie, fecha_inicio, fecha_fin, key):
#Definimos una función para la solicitud, donde se ingresan la serie que se quiere obtener, las fechas, y la llave

	url = f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie}/datos/{fecha_inicio}/{fecha_fin}?token={key}"
	#Definimos la url como f strings para poder ser reutilizable en el código principal

	try:
	#utilizamos try-except para evitar errores de solicitud

		respuesta = requests.get(url)
		respuesta = respuesta.json()
		#Solicitamos la información de la url y lo convertimos en un archivo json, que funciona como un diccionario

		archivo = open("inflación.txt", "w")
		archivo.write(str(respuesta))
		archivo.close()
		#Creamos un archivo de texto para visualizar la respuesta y poder trabajar en base a eso

		return respuesta

	except requests.exceptions.RequestException:

		print(f"Error de conexión")

		return None

def procesar_datos(json):
#Definimos una función para convertir los datos del json a un dataframe de pandas para poder trabajar de manera más facil

	datos = json["bmx"]["series"][0]["datos"]
	#Se selecciona de la respuesta el valor de datos, que es una lista de diccionarios anidados, y se asignan a la variable "datos"

	dataframe = pandas.DataFrame(datos)
	#Creamos el dataframe con esta lista de diccionarios para modificarlos más facilmente

	dataframe["fecha"] = pandas.to_datetime(dataframe["fecha"], format="%d/%m/%Y")
	dataframe["dato"] = dataframe["dato"].str.replace(",", "").astype(float)
	#Realizamos modificaciones a los dos valores de los diccionarios, en ambos convertimos de un string a un tipo más facil de manejar
	#Para fecha, utilizamos datetime para convertir de string a datetime, y le damos formato, de esta manera lo podemos ordenar de mas antiguo a más reciente
	#Para dato, utilizamos astype(float) para convertir los valores que se presentan como string a valores flotantes para poder hacer calculos con ellos

	dataframe = dataframe.sort_values("fecha")
	#Ordenamos por fecha de más antiguo a más reciente
	
	return dataframe

def guardar_excel(dataframe):
#Definimos una función para exportar los resultados como documento .xlsx, o un documento de Excel, donde utilizamos try-except para evitar errores

	try:

		dataframe.to_excel("Inflación.xlsx")
		print(f"Datos guardados con éxito, se encontrarán en la carpeta donde encuentra el código como 'Inflación.xlsx'")

	except Exception:

		print(f"Error al guardar Excel")