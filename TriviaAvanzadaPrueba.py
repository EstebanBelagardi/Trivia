import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkFont
import mysql.connector
import random

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="GAMETECH",
    port=3305,
    database="bdtrivia"
)


temporizador_reloj = None
cursor = conexion.cursor()
indice_pregunta_actual = 0

preguntas = []
pregunta_actual = None
respuestas_correctas = 0

def cargar_preguntas():
    if not preguntas:  # Solo carga preguntas si la lista está vacía
        cursor.execute("SELECT * FROM Preguntas")
        for pregunta in cursor.fetchall():
            preguntas.append(pregunta)

def cargar_usuario():
    tree.delete(*tree.get_children())
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM Usuarios")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row) 

def mostrar_alerta(mensaje):
    messagebox.showwarning("Alerta", mensaje)

def dejar_jugar():
    global indice_pregunta_actual, respuestas_correctas
    if usuario_entry.get() and instagram_entry.get():
        cargar_preguntas()
        indice_pregunta_actual = 0  # Inicializar la variable
        respuestas_correctas = 0  # Reiniciar el contador de respuestas correctas
        abrir_ventana_secundaria()
        mostrar_siguiente_pregunta()
        iniciar_reloj()
        usuario_entry.delete(0, tk.END)
        instagram_entry.delete(0, tk.END)
    else:
        mostrar_alerta("Para jugar, debes ingresar tu nombre de usuario e Instagram")

def guardar_usuario():
    cursor = conexion.cursor()
    nombre = usuario_entry.get().upper()
    instagram = instagram_entry.get()
    cursor.execute("INSERT INTO Usuarios (Nombre, Instagram) VALUES (%s,%s)", (nombre, instagram))
    conexion.commit()
    if nombre and instagram:
        mostrar_alerta("Estos datos son suficientes para hackearte")
    else:
        mostrar_alerta("Los campos son obligatorios. Debes completarlos")

reloj = None  # Agrega esta línea fuera de cualquier función para definir reloj

def abrir_ventana_secundaria():
    ventana_secundaria.deiconify()  # Mostrar la ventana secundaria
    global reloj  # Debes usar global para modificar la variable en la función

def iniciar_reloj():
    global tiempo_segundos, temporizador_reloj
    tiempo_segundos = 0
    if temporizador_reloj is not None:
        ventana.after_cancel(temporizador_reloj)
    actualizar_reloj()

def actualizar_reloj():
    global tiempo_segundos, temporizador_reloj
    horas = tiempo_segundos // 3600
    minutos = (tiempo_segundos % 3600) // 60
    segundos = tiempo_segundos % 60
    tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    if reloj is not None:  # Verifica que reloj no sea None antes de configurarlo
        reloj.config(text=tiempo_formateado)  # Configurar el texto del reloj
        tiempo_segundos += 1
        temporizador_reloj = ventana.after(1000, actualizar_reloj)

def verificar_respuesta():
    global respuestas_correctas, indice_pregunta_actual, respuesta_seleccionada
    pregunta_actual = preguntas[indice_pregunta_actual - 1]
    respuesta_correcta = pregunta_actual[2]

    if respuesta_seleccionada == respuesta_correcta:
        respuestas_correctas += 1

    indice_pregunta_actual -= 1  # Restar 1 al índice de la pregunta actual
    mostrar_siguiente_pregunta()

def finalizar_juego():
    ventana_secundaria.withdraw()
    mostrar_alerta(f"Juego terminado. Respuestas correctas: {respuestas_correctas}/{len(preguntas)}")

def mostrar_siguiente_pregunta():
    global pregunta_actual, indice_pregunta_actual, respuesta_seleccionada

    if indice_pregunta_actual < len(preguntas):
        pregunta_actual = preguntas[indice_pregunta_actual]
        pregunta_label.config(text=pregunta_actual[1])

        opciones = [pregunta_actual[2], pregunta_actual[3], pregunta_actual[4], pregunta_actual[5]]
        opciones_incorrectas = [opcion for opcion in opciones if opcion != pregunta_actual[2]]  # Obtener las respuestas incorrectas

        random.shuffle(opciones_incorrectas)  # Barajar las respuestas incorrectas
        opciones.insert(random.randint(0, 3), opciones_incorrectas[0])  # Colocar la primera respuesta incorrecta en una posición aleatoria
        opciones.insert(random.randint(0, 4), opciones_incorrectas[1])  # Colocar la segunda respuesta incorrecta en una posición aleatoria
        opciones.insert(random.randint(0, 5), opciones_incorrectas[2])  # Colocar la tercera respuesta incorrecta en una posición aleatoria

        for i in range(4):
            labels_respuesta[i].config(text=opciones[i])

        respuesta_seleccionada = None  # Reiniciar la respuesta seleccionada
        indice_pregunta_actual += 1
    else:
        finalizar_juego()


def seleccionar_respuesta(respuesta):
    global respuesta_seleccionada
    respuesta_seleccionada = labels_respuesta[respuesta - 1].cget("text")
    verificar_respuesta()
    mostrar_siguiente_pregunta()

def abrir_ventana_logros():
    ventana_logros.deiconify()

ventana = tk.Tk()
ventana.title("Trivia Game")
fontStyle = tkFont.Font(family="Lucida Grande", size=20)
ventana.wm_state("zoomed")
ventana.config(bg="#ffff00")

ancho_pantalla = ventana.winfo_screenwidth()
alto_pantalla = ventana.winfo_screenheight()

style = ttk.Style()
style.configure("BW.TLabel", background="#0b4f64",foreground="white")

image = tk.PhotoImage(file="aniversario.png")
label_Imag = ttk.Label(ventana, image=image)
label_Imag.pack(side=tk.TOP) 

label_usuario = ttk.Label(ventana, text="Usuario", style="BW.TLabel",font=("Lucida Grande", 15))
label_usuario.place(x=150, y=400, width=75, height=50)
usuario_entry = tk.Entry(ventana, font=("Lucida Grande", 12))
usuario_entry.place(x=250, y=405, width=300, height=40)
label_instagram = ttk.Label(ventana, text="Instagram", style="BW.TLabel",font=("Lucida Grande", 15))
label_instagram.place(x=120, y=525, width=100, height=50)
instagram_entry = tk.Entry(ventana, font=("Lucida Grande", 12))
instagram_entry.place(x=250, y=530, width=300, height=40)

jugar_boton = tk.Button(ventana, text="Jugar", command=dejar_jugar, padx=10, pady=15, font=fontStyle)
jugar_boton.place(relx=0.5, rely=0.5, width=270, anchor='c')
jugar_boton.config(fg="black", bg="#ffffff",relief="sunken")

ventana_secundaria = tk.Toplevel()
ventana_secundaria.geometry(f"{ventana.winfo_screenwidth()}x{ventana.winfo_screenheight()}")
ventana_secundaria.title("Juego")
ventana_secundaria.withdraw()
ventana_secundaria.config(bg="#0b4f64")
ventana_secundaria.overrideredirect(True)

boton_cerrar = tk.Button(
    ventana_secundaria,
    text="Cerrar ventana", 
    command=ventana_secundaria.withdraw,
    font=fontStyle)
boton_cerrar.place(x=1000, y=650)    

reloj = tk.Label(ventana_secundaria, font=("Arial", 20), bg="#0b4f64", fg="#ffffff")
reloj.place(x=1100, y=200, width=150, height=100)

pregunta_label = tk.Label(ventana_secundaria, text="", padx=10, pady=40, font=fontStyle)
pregunta_label.config(bg="#0b4f64", fg="#ffffff")
pregunta_label.pack()

labels_respuesta = []
for i in range(4):
    label = tk.Label(ventana_secundaria, text="", padx=10, pady=10, font=fontStyle)
    label.config(bg="#0b4f64", fg="white")
    label.pack()
    labels_respuesta.append(label)

for i in range(4):
    label_numero = tk.Label(ventana_secundaria, text=str(i+1), font=fontStyle)
    label_numero.config(bg="#0b4f64", fg="white")
    label_numero.place(x=40, y=180 + i * 50)

for i in range(1, 5):
    boton = tk.Button(ventana_secundaria, text=str(i), command=lambda i=i: seleccionar_respuesta(i), padx=10, pady=10, font=fontStyle)
    boton.config(bg="white", fg="black")
    boton.place(x=400 if i < 3 else 750, y=400 if i % 2 == 1 else 550, width=130, height=80)

respuesta_seleccionada = None

ventana_logros = tk.Toplevel()
ancho_pantalla_logros = ventana_logros.winfo_screenwidth()
alto_pantalla_logros = ventana_logros.winfo_screenheight()
ventana_logros.geometry(f"{ancho_pantalla}x{alto_pantalla}")
ventana_logros.title("Logros")
ventana_logros.withdraw()

# Crear Treeview para mostrar la información
tree = ttk.Treeview(ventana_logros, columns=("Id","Nombre", "Instagram", "Puntaje", "Tiempo"))
tree.heading("#1", text="Id")
tree.heading("#2", text="Nombre")
tree.heading("#3", text="Instagram")
tree.heading("#4", text="Puntaje")
tree.heading("#5", text="Tiempo")

tree.column("#0", width=0, stretch=tk.NO)  # Ocultar la columna #0 que habitualmente muestra las primary key de los objetos

tree.pack(padx=10, pady=10)

signos = tk.PhotoImage(file="signos.png")
boton_signos = tk.Button(ventana, text="signos", image=signos, command=abrir_ventana_logros)
boton_signos.place(x=1350, y=680, width=230, height=140)
boton_signos.config(relief="sunken")  
ventana_logros.overrideredirect(True)

boton_cerrar = tk.Button(
    ventana_logros,
    text="Cerrar ventana", 
    command=ventana_logros.withdraw,
    font=fontStyle)
boton_cerrar.place(x=1000, y=650)    

ventana.mainloop()

conexion.close()
