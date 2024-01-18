
import requests
import json
from data import comprobar, enviados, msj_a_enviar


#--------------- ENVIAR MENSAJE------------

def send_msj(cel, mensaje,img):
    url = "http://localhost:3001/lead" #URL de la API WHATSAPP JS

    data = {
        "message": mensaje,
        "phone": cel,
        "image": img
    }

    headers = {
        "Content-Type":"application/json"
    }
    response = requests.post(url, json = data, headers = headers)

    response_dict = json.loads(response.text)#Posible falla en text
    status = response_dict["id"] #["responseExSave"]["id"]
    return status


#---------- RECORRER LISTA Y ENVIAR MENSAJE----------

def iterar_msjs(texto,lista,ruta_img):

    if lista is not False: 
        for i in lista.index: #Leer por fila y enviar msj
            nombre = lista["Nombre"][i]
            cel = lista["Telefono"][i]
            cel = comprobar(cel)

            if cel[0] != "error":
                mensaje = msj_a_enviar(nombre,texto)
                status = send_msj(cel[1], mensaje,ruta_img)
                pass
            else: status = "Msj no enviado: Formato número incorrecto"

            enviados(cel[1], status)


#------------- VERIFICAR ESTADO CONEXIÓN WHATSAPP-------------

def estado():
    url = "http://localhost:3001/status" #URL de la API WHATSAPP JS

    data = {
    }

    headers = {
        "Content-Type":"application/json"
    }
    respuesta = ""
    try:
        response = requests.post(url)
        response_dict = json.loads(response.text)
        if response_dict["estado"] == "LOGIN_SUCCESS":
            respuesta = "CONECTADO"
        elif response_dict["estado"] == "ESCANEAR_QR":
            respuesta = "ESCANEAR QR"
        elif response_dict["estado"] == "DISCONNECT":
            respuesta = "DISCONNECT"
        else: respuesta = "Conectando..."

    except: 
        respuesta = "Iniciando Servidor...."
    
    return respuesta 





