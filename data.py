import pandas as pd
import customtkinter as ctk
import re



registro = "registro.xlsx"

#---------- CARGAR ARCHIVO----------

def read_excel(registro):
        
        df = pd.read_excel(registro)
        if all(map(lambda x: x in df.columns, ["Nombre", "Telefono"])):  #Verifico que existan esas 2 columnas para poder enviar los mensajes 
            return True, df
        else: 
            return False, None
        
#------------ABRIR ARCHIVO CON TKINTER-----------
lista = False

def open_file():
    global lista
    status_file = "Cargado Exitosamente"
    try:
        file =ctk.filedialog.askopenfilename(title="Abrir planilla", initialdir="", filetypes=(("Archivos Excel","*.xlsx"),("Todos los archivos", "*.*")))
        success, dframe = read_excel(file)  
        if success:
            lista = dframe
        else:
            status_file = "Formato erroneo de columnas"
    except:
        status_file ="Error en la carga del archivo"

    return status_file, lista

def open_img():
    try:
        img =ctk.filedialog.askopenfilename(title="Abrir planilla", initialdir="", filetypes=(("Archivos de imagen","*.jpg; *.jpeg; *.png; *.gif"),("Todos los archivos", "*.*")))
    except:
        img =""

    return img
    


#---------- CORREGIR NÚMERO DE TELEFONO ------------

def comprobar(telefono):

    telefono = re.sub(r"\D","",str(telefono)) #Elimina todos los caracteres no numericos.

    if "54" in telefono[0:2]:
        if "9" not in telefono[2]:
            telefono = telefono[0:2]+"9"+telefono[2:]
    else:
        telefono = "549"+telefono

    if "0" in telefono[3]:# Saco el 0 de la caracteristica
        telefono = telefono[:3] + telefono[4:]
    if ("11" in telefono[3:5]) and ("15" in telefono[5:7]): #Borro el 15 de los números con caracteristica 011.
        telefono = telefono[0:5] + telefono[7:]
    if "15" in telefono[-8:-6]:#Elimino el 15
        telefono = telefono[0:-8] + telefono[-6:]
    if len(telefono) == 13:
        return ["Correcto",telefono] #Devuelvo lista para manejar error al enviar msj
    else: 
        return ["error",telefono]


# ---------- MENSAJE A ENVIAR -----------------

def msj_a_enviar(nombre,texto):
    return f'Hola {nombre}! {texto}'


#-----------Diccionario de Msj Enviados y No Enviados---------

msj_enviados = {}

def enviados(cel, status):
    global msj_enviados
    msj_enviados[cel] = status


registro = "registro.xlsx"

