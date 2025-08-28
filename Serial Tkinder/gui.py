# Importamos las librerías necesarias
import tkinter as tk                # Tkinter para la interfaz gráfica
import serial                       # pyserial para la comunicación con Arduino
import serial.tools.list_ports      # para listar los puertos disponibles

# --- Funciones ---

# def listar_puertos():
#     """Busca los puertos seriales disponibles y los muestra en el menú desplegable."""
#     puertos = [p.device for p in serial.tools.list_ports.comports()]  # Lista de dispositivos detectados
#     menu_puertos["menu"].delete(0, "end")  # Limpia el menú desplegable
#     for p in puertos:  # Agrega cada puerto como opción
#         menu_puertos["menu"].add_command(label=p, command=lambda v=p: puerto_var.set(v))
#     if puertos:  # Si hay puertos disponibles, selecciona el primero por defecto
#         puerto_var.set(puertos[0])

def conectar():
    """Intenta abrir la conexión serial con el puerto y baudrate seleccionados."""
    global ser  # usamos la variable global 'ser'
    try:
        # Abrimos el puerto serial con los parámetros elegidos
        ser = serial.Serial(puerto_var.get(), int(baud_var.get()), timeout=0)
        mostrar_datos()              # empezamos a leer datos
        estado.set("Conectado")      # cambiamos el estado
    except Exception as e:           # si algo falla, mostramos el error
        estado.set(f"Error: {e}")

def mostrar_datos():
    """Lee los datos del Arduino y los coloca en la caja de texto."""
    if ser and ser.is_open:                      # Verifica que el puerto esté abierto
        data = ser.read(ser.in_waiting or 1)     # Lee datos disponibles (o 1 byte si no hay nada)
        if data:                                 # Si hay datos recibidos
            texto.insert("end", data.decode(errors="ignore"))  # Los escribe en el área de texto
            texto.see("end")                     # Desplaza la vista hacia abajo
        root.after(100, mostrar_datos)           # Llama de nuevo a esta función cada 100 ms

# --- Interfaz gráfica ---

root = tk.Tk()                    # Crea la ventana principal
root.title("Arduino Serial Viewer")  # Título de la ventana

puerto_var = tk.StringVar()       # Variable para guardar el puerto seleccionado
baud_var = tk.StringVar(value="9600")  # Variable para guardar el baudrate (por defecto 9600)
estado = tk.StringVar(value="Desconectado")  # Variable para mostrar el estado
ser = None                        # Variable global para el objeto Serial

# Botón para actualizar la lista de puertos
# tk.Button(root, text="Actualizar puertos", command=listar_puertos).pack()

# Menú desplegable para seleccionar puerto
# menu_puertos = tk.OptionMenu(root, puerto_var, "")
# menu_puertos.pack()

menu_puertos=tk.Entry(root, textvariable=puerto_var).pack()


# Caja de texto para ingresar el baudrate
tk.Entry(root, textvariable=baud_var).pack()

# Botón para conectar
tk.Button(root, text="Conectar", command=conectar).pack()

# Caja de texto donde se mostrarán los datos recibidos
texto = tk.Text(root, height=15, width=60)
texto.pack()

# Etiqueta que muestra el estado (desconectado/conectado/error)
tk.Label(root, textvariable=estado).pack()

# Llenamos la lista de puertos al inicio
# listar_puertos()

# Bucle principal de la interfaz
root.mainloop()
