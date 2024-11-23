# App de Escritorio usando Tkinter, bootstrap, sqlite3 y python.
# Desarrollada por Fernando Dastugue y Mauro Piñeyro.
# Técnicas de Programación - CFP N°23 

import sqlite3
from tkinter import Tk, StringVar, DoubleVar, messagebox
from tkinter import ttk
from ttkbootstrap import Style


# Base de datos
def inicializar_db():
    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alumnos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        calificacion REAL NOT NULL
    )
    ''')
    conexion.commit()
    conexion.close()
    

# Operaciones CRUD
def insertar_alumno(nombre, apellido, email, calificacion):
    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()
    try:
        cursor.execute('''
        INSERT INTO alumnos (nombre, apellido, email, calificacion)
        VALUES (?, ?, ?, ?)
        ''', (nombre, apellido, email, calificacion))
        conexion.commit()
        messagebox.showinfo("Éxito", "Alumno agregado correctamente.")
    except sqlite3.IntegrityError as e:
        messagebox.showerror("Error", f"Error al agregar alumno: {e}")
    finally:
        conexion.close()

def obtener_alumnos():
    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM alumnos')
    alumnos = cursor.fetchall()
    conexion.close()
    return alumnos

def actualizar_alumno(id, nombre, apellido, email, calificacion):
    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()
    cursor.execute('''
    UPDATE alumnos
    SET nombre = ?, apellido = ?, email = ?, calificacion = ?
    WHERE id = ?
    ''', (nombre, apellido, email, calificacion, id))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Alumno actualizado. Click en aceptar para ver los cambios")

def eliminar_alumno(id):
    conexion = sqlite3.connect('alumnos.db')
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM alumnos WHERE id = ?', (id,))
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Alumno eliminado correctamente.")

# Variable para rastrear el estado de la tabla
datos_visibles = False  # Comienza como oculto

# Función para alternar entre cargar y ocultar datos
def alternar_datos():
    global datos_visibles
    if datos_visibles:
        # Ocultar datos
        for row in tree.get_children():
            tree.delete(row)
        label_mensaje.config(text="Presionar cargar datos para ver el listado de alumnos")
        boton_cargar.config(text="Cargar Alumnos")
        datos_visibles = False
    else:
        # Cargar datos
        alumnos = obtener_alumnos()
        for alumno in alumnos:
            tree.insert('', 'end', values=alumno)
        label_mensaje.config(text="Presionar -Ocultar Alumnos- para dejar de ver el listado")
        boton_cargar.config(text="Ocultar Alumnos")
        datos_visibles = True


# Interfaz gráfica
def interfaz_grafica():
    global boton_cargar, label_mensaje, tree  # Declarar como globales para acceder desde otras funciones

    # Función para mostrar el tutorial en una ventana emergente
    def mostrar_tutorial():
        instrucciones = (
        "1. **Agregar**: Completa el formulario con el nombre, apellido, email y calificación del alumno. "
        "Luego, presiona el botón 'Agregar'.\n\n"
        "2. **Actualizar**: Selecciona el alumno que deseas actualizar en la tabla. "
        "Modifica los datos en el formulario y presiona el botón 'Actualizar'.\n\n"
        "3. **Eliminar**: Selecciona el alumno que deseas eliminar en la tabla y presiona el botón 'Eliminar'.\n\n"
        "Nota: El botón 'Cargar/Ocultar Datos' alterna la visibilidad del listado de alumnos."
        )
        messagebox.showinfo("Tutorial de Uso", instrucciones)

    
    
    def cargar_datos():
        # Deshabilitar el botón mientras carga
        boton_cargar.config(state="disabled")
        root.update()  # Refrescar la interfaz gráfica
        # Limpiar la tabla y recargar
        for row in tree.get_children():
            tree.delete(row)
        alumnos = obtener_alumnos()
        # Obtener datos y mostrarlos
        for alumno in obtener_alumnos():
            tree.insert('', 'end', values=alumno)
        # Mostrar mensaje opcional
        messagebox.showinfo("Datos Cargados", f"Se han cargado {len(alumnos)} alumnos hasta el momento.")
        # Habilitar el botón nuevamente
        boton_cargar.config(state="normal")

    def agregar():
        insertar_alumno(
            nombre_var.get(), apellido_var.get(), email_var.get(), calificacion_var.get()
        )
        cargar_datos()

    def cargar_datos_seleccionados(event):
    # Obtener la selección actual
        seleccion = tree.selection()  # Selección en el Treeview
        if seleccion:
            item = tree.item(seleccion[0])  # Datos de la fila seleccionada
            valores = item['values']  # Lista de valores en la fila
        
        # Cargar valores en las variables del formulario
            nombre_var.set(valores[1])       # Nombre
            apellido_var.set(valores[2])    # Apellido
            email_var.set(valores[3])       # Email
            calificacion_var.set(valores[4])  # Calificación
    
    
    def actualizar():
        try:
            selected_item = tree.selection()[0]
            valores = tree.item(selected_item, 'values')
            actualizar_alumno(
                valores[0], nombre_var.get(), apellido_var.get(), email_var.get(), calificacion_var.get()
            )
            cargar_datos()
        except IndexError:
            messagebox.showerror("Error", "Selecciona un alumno para actualizar.")

    def eliminar():
        try:
            selected_item = tree.selection()[0]
            valores = tree.item(selected_item, 'values')
            eliminar_alumno(valores[0])
            cargar_datos()
        except IndexError:
            messagebox.showerror("Error", "Selecciona un alumno para eliminar.")

    # Crear ventana principal
    root = Tk()
    root.title("Gestión de Alumnos v1.0 - Dastugue & Piñeyro")
    root.geometry("800x600")
    style = Style(theme="darkly")
    
    style.configure(
    "Treeview",
    rowheight=25,  # Altura de las filas
    bordercolor="blue",  # Color de los bordes
    relief="flat",
    font=("Helvetica", 10),
    )
    style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), foreground="white")
    style.map("Treeview", background=[("selected", "black")])

    # Agregar líneas divisorias entre columnas
    style.layout("Treeview", [
    ("Treeview.treearea", {"sticky": "nswe"})  # Espacio para las celdas
])


    # Variables
    nombre_var = StringVar()
    apellido_var = StringVar()
    email_var = StringVar()
    calificacion_var = DoubleVar()

   # Frame para el formulario (centrado)
    frame_formulario = ttk.Frame(root, padding=20)
    frame_formulario.pack(pady=10)

    # Etiquetas y campos del formulario
    ttk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, padx=5, pady=5)
    entry_nombre = ttk.Entry(frame_formulario, textvariable=nombre_var, width=30)
    entry_nombre.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Apellido:").grid(row=1, column=0, padx=5, pady=5)
    entry_apellido = ttk.Entry(frame_formulario, textvariable=apellido_var, width=30)
    entry_apellido.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Email:").grid(row=2, column=0, padx=5, pady=5)
    entry_email = ttk.Entry(frame_formulario, textvariable=email_var, width=30)
    entry_email.grid(row=2, column=1, padx=5, pady=5)

    ttk.Label(frame_formulario, text="Calificación:").grid(row=3, column=0, padx=5, pady=5)
    entry_calificacion = ttk.Entry(frame_formulario, textvariable=calificacion_var, width=30)
    entry_calificacion.grid(row=3, column=1, padx=5, pady=5)


    # Botones
    frame_botones = ttk.Frame(root, padding=10)
    frame_botones.pack()
    
    ttk.Button(frame_botones, text="Agregar", command=agregar).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Actualizar", command=actualizar).grid(row=0, column=1, padx=5)
    
    ttk.Button(frame_botones, text="Eliminar", command=eliminar).grid(row=0, column=2, padx=5)
    # Botón dinámico para cargar/ocultar datos
    boton_cargar = ttk.Button(frame_botones, text="Cargar Alumnos", command=alternar_datos, style="info.TButton")
    boton_cargar.grid(row=0, column=3, padx=5)
    # Botón Tutorial
    ttk.Button(frame_botones, text="Tutorial", command=mostrar_tutorial, style="success.TButton").grid(row=0, column=4, padx=5)

    
    # Mensaje dinámico
    label_mensaje = ttk.Label(root, text="Presionar -Cargar Alumnos- para ver el listado de alumnos", font=("Helvetica", 12))
    label_mensaje.pack(pady=10)
    

    # Tabla (Treeview)
    tree = ttk.Treeview(root, columns=("ID", "Nombre", "Apellido", "Email", "Calificación"), show="headings")
    tree.heading("ID", text="ID", anchor="center")
    tree.column("ID", width=50, anchor="center")
    tree.heading("Nombre", text="Nombre", anchor="center")
    tree.column("Nombre", width=150, anchor="center")
    tree.heading("Apellido", text="Apellido", anchor="center")
    tree.column("Apellido", width=150, anchor="center")
    tree.heading("Email", text="Email", anchor="center")
    tree.column("Email", width=250, anchor="center")
    tree.heading("Calificación", text="Calificación", anchor="center")
    tree.column("Calificación", width=150, stretch=True, anchor="center")
    tree.bind("<<TreeviewSelect>>", cargar_datos_seleccionados)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    #cargar_datos()
    root.mainloop()

# Inicializar la base de datos y lanzar la interfaz
if __name__ == "__main__":
    inicializar_db()
    interfaz_grafica()
