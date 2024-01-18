import customtkinter as ctk
from tkinter import ttk
import subprocess
from data import open_file, msj_enviados,lista, open_img
from api_request import estado, iterar_msjs
from PIL import Image, ImageDraw, ImageFont
from instalacion import run_node, kill_node
from tkinter import messagebox
import atexit

# ---------------- CONFIGURACIONES GENERALES----------

ctk.set_appearance_mode("dark") # Modes: system (default), light, dark
ctk.set_default_color_theme("dark-blue") #themes: blue (default), dark-blue, green


# ----------------- FUNCIONES DE LA INTERFAZ------------

#Logica botones según estado de conexión
def actualizar_interfaz():
    respuesta = estado()    
    
    estado_resultado.configure(text = respuesta)    

    if respuesta == "CONECTADO":
        escanear_qr.grid_forget()
        charge_btn.configure( state = "normal" )
        enviar_msj.grid(row = 5,column = 0, columnspan= 2, pady = 15)
        estado_resultado.configure(text_color="#38EB5C")

    elif respuesta == "DISCONNECT":
        enviar_msj.grid_forget()
        resultado.grid_forget()
        charge_btn.configure( state = "disabled" )
        estado_resultado.configure(text =respuesta)
        estado_resultado.configure(text_color="#FF0000")

    elif respuesta == "ESCANEAR QR":
        enviar_msj.grid_forget()
        charge_btn.configure( state = "disabled" )
        escanear_qr.grid(row = 5,column = 0, columnspan= 2, pady = 15)
        estado_resultado.configure(text =respuesta, text_color="#FFFFFF")

    else: 
        enviar_msj.grid_forget()
        escanear_qr.grid_forget()
        charge_btn.configure( state = "disabled" )
        estado_resultado.configure(text =respuesta, text_color="#FFFFFF")


    app.after(3000, actualizar_interfaz)


#Abrir imagen QR
def ver_imagen():

    archivo = ".\\api-ws\\qr.svg"
    subprocess.run(["start", archivo], shell = True)


#Mostrar estado de mensajes enviados
def mostrar_resultado():
    #cerrar Toplevel y reiniciar Treeview
    def close():
        tabla.delete(*tabla.get_children())
        nueva_ventana.destroy()
    
    nueva_ventana = ctk.CTkToplevel()
    nueva_ventana.geometry("750x800")
    nueva_ventana.title("Estado de envio")
    nueva_ventana.grab_set() #Envio el toplevel al frente

    tabla = ttk.Treeview(nueva_ventana, columns=("Teléfono", "Estado"), show="headings")
    style = ttk.Style()
    style.configure("Treeview", font=("",18),rowheight = 28)
    tabla.heading("Teléfono", text="Teléfono")
    tabla.heading("Estado", text="Estado")
    tabla.column("Teléfono",width=400)
    tabla.column("Estado",width=600)
    for telefono, estado in msj_enviados.items():
        tabla.insert("", "end", values=(telefono, estado))
    tabla.pack(fill="both",expand=True)
    nueva_ventana.protocol("WM_DELETE_WINDOW",close)

#Envio mensajes Y habilito botón para ver resultados
def ejecutar():
    global msj_enviados
    enviar_msj.grid_forget()
    resultado.grid_forget()
    msj_espera.grid(row = 5,column = 0, columnspan= 2, pady = 15)
    app.update()
    msj_enviados.clear()
    texto = text_box.get("1.0", "end-1c")#??????
    try:    
        iterar_msjs(texto,lista,path_img)
    
    except Exception as e:
        messagebox.showerror("Mensaje de error","A ocurrido un error, cierre el programa y vuelva a abrirlo")

    else:
        msj_espera.grid_forget()
        messagebox.showinfo("Aviso!","Mensajes enviados!!") #Muestro Pop Up de que los mensajes fueron enviados. 
    finally:
        msj_espera.grid_forget()
        enviar_msj.grid(row = 5,column = 0, columnspan= 2, pady = 15)
        resultado.grid(row = 6,column = 0, columnspan= 2, pady = 5)

#Cargo archivo y muestro estado
def charge_file():
    global lista
    status_file,lista= open_file()
    if status_file == "Cargado Exitosamente":
        charge_btn.configure(text = "Buscar Planilla ✅", fg_color = "#008f39", hover_color = "#0B6730")
        enviar_msj.configure( state = "normal" )
    else:
        charge_btn.configure(text = "Buscar Planilla ❎", fg_color="#DB3E39", hover_color = "#821d14")
        enviar_msj.configure( state = "disabled" )

path_img = ""
def charge_img():
    global path_img
    path_img = open_img()
    if path_img != "":
        cargar_img.configure(text = "Imagen ✅", fg_color = "#008f39", hover_color = "#0B6730")
    else: 
        cargar_img.configure(text = "Imagen ❎", fg_color="#DB3E39", hover_color = "#821d14")


#----------------- Manejo Emojis--------------------
emojis=["😀","😊","🤩","😍","🥳","👾","🤖","🌱","    ☀️","✨","🔶","🔷","✅","💡","📌","📍","    ❤️","    🖥️","💻","❗","❓","💭","💬","🔺","🏳️","🏴","👍","📢","🍄","🎇"]

#Convertir emoji a imagen
def emoji(emoji, size=32):
    # convert emoji to CTkImage
    font = ImageFont.truetype("seguiemj.ttf", size=int(size/2))
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((int(size/2), int(size/2)), emoji,
              embedded_color=True, font=font, anchor="mm")
    img = ctk.CTkImage(img, size=(size, size))
    return img


def insert_emoji(icono):
         position = text_box.index(ctk.INSERT)
         text_box.insert(position, icono)

#Ventana con emojis
def despl_emojis():

    x_app , y_app = app.winfo_x(), app.winfo_y() #Tomo la posicion del root, para posicionar el toplevel sobre el costado derecho
    x_toplevel = x_app + 820
    y_toplevel = y_app
    ventana_emojis = ctk.CTkToplevel()
    ventana_emojis.geometry(f"150x400+{x_toplevel}+{y_toplevel}")
    ventana_emojis.title("Emojis")
    ventana_emojis.resizable(False, False)
    ventana_emojis.grab_set() #Envio el toplevel al frente

    i = 0
    j = 0

    for icono in emojis: #Cargo lista emojis
        label = ctk.CTkButton(ventana_emojis, text=None, image=emoji(icono),width=30,command=lambda e =icono:insert_emoji(e))
        label.grid(row = j,column= i)
        i = i+1
        if i == 3:
            j = j+1
            i = 0



#----------------- CREACION INTERFAZ------------------

#Comando que cierra el servidor al cerrar la app
atexit.register(kill_node)
run_node()
app = ctk.CTk()
app.geometry("650x600")
app.title("Envio de Whatsapp")
app.resizable(False, False)
app.iconbitmap(".\\statics\\whatsapp-polo-2.ico")

app.columnconfigure(0, weight=1, minsize = 270 )
app.columnconfigure(1, weight=1, minsize= 270 )

estado_coneccion = ctk.CTkLabel(app, text = "Estado Conexión:",font=("",20))
estado_coneccion.grid(row = 0, column = 0)  
estado_resultado = ctk.CTkLabel(app, text = "",font=("",20))
estado_resultado.grid(row = 0, column = 1, pady=10)


charge_btn = ctk.CTkButton(app, text="Buscar Planilla ❎", fg_color="#DB3E39", hover_color = "#821d14", command=charge_file,font=("",15),width=40,height=40,state = "disabled")
charge_btn.grid(row = 1, pady=10)

inicio_texto = ctk.CTkLabel(app, text = "Hola, Nombre!",font=("",15)).grid(row = 2, column = 0, pady=10)

text_box = ctk.CTkTextbox(app,width=550,font=("",14))
text_box.grid(row = 3, column = 0, columnspan = 2)

enviar_msj = ctk.CTkButton(app, text="Enviar Mensaje", font=("",16), width = 200, height=50, state="disabled", command=ejecutar) #Aparece si se conecta la api
msj_espera = ctk.CTkLabel(app, text="ENVIANDO MENSAJES....", font=("",16))

cargar_img = ctk.CTkButton(app, text="Imagen ❎",font=("",15), fg_color="#DB3E39", hover_color = "#821d14", height= 35,command=charge_img)
cargar_img.grid(row = 4, column = 0, pady = 10)
btn_emojis = ctk.CTkButton(app, text="Emojis",font=("",15), height= 35,command=despl_emojis)
btn_emojis.grid(row = 4, column = 1, pady = 10)

escanear_qr = ctk.CTkButton(app, text="ESCANEAR QR", font=("",16), width = 200, height=50, command=ver_imagen) 

resultado = ctk.CTkButton(app, text="VER ESTADO", font=("",16), width = 200, height=50, command=mostrar_resultado) 

actualizar_interfaz()

app.mainloop()

