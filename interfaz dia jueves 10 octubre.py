import sqlite3 
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os

#  para conectarse a la base de datos SQLite
def conectar_bd():
    conexion = sqlite3.connect("C:/Users/yorle/Downloads/proyecto/hotela_nuevo.db")
    cursor = conexion.cursor()

    # Crear la tabla cliente si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS cliente (
        id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT NOT NULL,
        correo TEXT NOT NULL,
        telefono TEXT NOT NULL,
        direccion TEXT NOT NULL
    )''')

    # Crear la tabla recamara si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS recamara (
        id_recamara INTEGER PRIMARY KEY AUTOINCREMENT,
        tipo_recamara TEXT NOT NULL,
        precio REAL NOT NULL
    )''')

    # Crear la tabla pago si no existe
    cursor.execute('''CREATE TABLE IF NOT EXISTS pago (
        id_pago INTEGER PRIMARY KEY AUTOINCREMENT,
        id_cliente INTEGER NOT NULL,
        monto REAL NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente)
    )''')

    conexion.commit()
    conexion.close()

# agregar un cliente
def agregar_cliente():
    conexion = sqlite3.connect("C:/Users/yorle/Downloads/proyecto/hotela_nuevo.db")
    cursor = conexion.cursor()
    
    # Validar campos vacios
    if nombre_var.get() == "" or apellido_var.get() == "" or correo_var.get() == "" or telefono_var.get() == "" or direccion_var.get() == "" or tipo_recamara_var.get() == "" or monto_pago_var.get() == "":
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return
    
    # Insertar el cliente en la base de datos
    cursor.execute("INSERT INTO cliente (nombre, apellido, correo, telefono, direccion) VALUES (?, ?, ?, ?, ?)", 
                   (nombre_var.get(), apellido_var.get(), correo_var.get(), telefono_var.get(), direccion_var.get()))
    id_cliente = cursor.lastrowid  # Obtener el id del cliente recién insertado
    
    # Insertar el pago EN LA TABLA PAGO
    cursor.execute("INSERT INTO pago (id_cliente, monto, fecha) VALUES (?, ?, ?)", 
                   (id_cliente, monto_pago_var.get(), fecha_pago_var.get()))

    # Insertar la recamara EN LA TABLA RECAMARA
    cursor.execute("INSERT INTO recamara (tipo_recamara, precio) VALUES (?, ?)", 
                   (tipo_recamara_var.get(), precio_recamara_var.get()))
    
    conexion.commit()
    conexion.close()
    messagebox.showinfo("Éxito", "Cliente y detalles registrados correctamente")
    limpiar_campos()

#  limpiar los campos después de agregar UN CLIENTE////////
def limpiar_campos():
    nombre_var.set("")
    apellido_var.set("")
    correo_var.set("")
    telefono_var.set("")
    direccion_var.set("")
    tipo_recamara_var.set("")
    precio_recamara_var.set("")
    monto_pago_var.set("")
    fecha_pago_var.set("")

# Interfaz gráfica con Tkinter
ventana = Tk()
ventana.title("Gestión de Clientes del Hotel")

# Ruta del archivo de fondo
bg_image_path = "C:/Users/yorle/Downloads/proyecto/image.png"
logo_image_path = "C:/Users/yorle/Downloads/proyecto/LOGO.PNG"

# Verifica si el archivo de fondo existe
if os.path.isfile(bg_image_path):
    bg_image = Image.open(bg_image_path)
    bg_photo = ImageTk.PhotoImage(bg_image)
else:
    print("El archivo de fondo no se encuentra en la ruta especificada.")

# Verifica si el logo existe
if os.path.isfile(logo_image_path):
    logo_image = Image.open(logo_image_path)
    logo_photo = ImageTk.PhotoImage(logo_image)
else:
    print("El logo no se encuentra en la ruta especificada.")

# Crear un canvas para la imagen de fondo
canvas = Canvas(ventana, width=800, height=600)
canvas.pack(fill="both", expand=True)

# Colocar la imagen de fondo en el canvas
canvas.create_image(0, 0, anchor="nw", image=bg_photo)

# Colocar el logo en la esquina superior derecha
if 'logo_photo' in locals():  # Verificar si se ha cargado el logo
    canvas.create_image(00, 10, anchor="ne", image=logo_photo)  # Ajusta las coordenadas según sea necesario

# Variables
nombre_var = StringVar()
apellido_var = StringVar()
correo_var = StringVar()
telefono_var = StringVar()
direccion_var = StringVar()
tipo_recamara_var = StringVar()
precio_recamara_var = DoubleVar()
monto_pago_var = DoubleVar()
fecha_pago_var = StringVar()

# Etiquetas y campos de entrada
Label(ventana, text="Nombre", bg="#FFFFFF").place(x=50, y=50)
Entry(ventana, textvariable=nombre_var).place(x=250, y=50)

Label(ventana, text="Apellido", bg="#FFFFFF").place(x=50, y=90)
Entry(ventana, textvariable=apellido_var).place(x=250, y=90)

Label(ventana, text="Correo", bg="#FFFFFF").place(x=50, y=130)
Entry(ventana, textvariable=correo_var).place(x=250, y=130)

Label(ventana, text="Teléfono", bg="#FFFFFF").place(x=50, y=170)
Entry(ventana, textvariable=telefono_var).place(x=250, y=170)

Label(ventana, text="Dirección", bg="#FFFFFF").place(x=50, y=210)
Entry(ventana, textvariable=direccion_var).place(x=250, y=210)

Label(ventana, text="Tipo de Recámara", bg="#FFFFFF" ).place(x=50, y=250)
Entry(ventana, textvariable=tipo_recamara_var).place(x=250, y=250)

Label(ventana, text="Precio de Recámara", bg="#FFFFFF").place(x=50, y=290)
Entry(ventana, textvariable=precio_recamara_var).place(x=250, y=290)

Label(ventana, text="Monto del Pago", bg="#FFFFFF").place(x=50, y=330)
Entry(ventana, textvariable=monto_pago_var).place(x=250, y=330)

Label(ventana, text="Fecha del Pago", bg="#FFFFFF").place(x=50, y=370)
Entry(ventana, textvariable=fecha_pago_var).place(x=250, y=370)

# Botón  agregar cliente
Button(ventana, text="Agregar Cliente", command=agregar_cliente, bg="#4CAF50", fg="white").place(x=350, y=410)

# Ejecutar la función para conectar la base de datos y crear la tabla si no existe
conectar_bd()

# Iniciar el loop de la ventana
ventana.mainloop()

