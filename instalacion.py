import os
import subprocess
import signal
import re

#---------- SUBPROCESOS ENCARGADOS DE INSTALAR Y EJECUTAR SERVIDOR EN NODE JS PARA UTILIZAR CON API WHATSAPP --------

ruta = os.getcwd() #Obtengo la ruta donde estoy parado
pid_padre = os.getpid()

#Compruebo si hay espacios en los nombres de los directorios
expresion_regular = r"([^\\]*\s+[^\\]*)" 

ruta_api = os.path.join(ruta , "api-ws") 

#Reemplazar espacios en blanco con comillas en la ruta
ubicar = re.sub(expresion_regular, r'"\1"', ruta)

ruta_api = ruta + "\\api-ws"

instalar =r''+os.path.join(ubicar ,"nodePortable","npm install")
ruta_node1 = r''+os.path.join(ubicar ,"nodePortable\\node app.js")


def run_node():

    instalacion = subprocess.Popen(instalar, shell=True, cwd= ruta_api) #Instalo dependencias
    instalacion.wait()

    if instalacion:
        resultado = subprocess.Popen(ruta_node1, shell=True, cwd= ruta_api) #Ejecuto run build
        #resultado.wait()

#Función para detener los procesos    
def kill_node(): 
    subprocess.run("taskkill /F /IM node.exe", shell=True)
    os.kill(pid_padre, signal.SIGINT)





