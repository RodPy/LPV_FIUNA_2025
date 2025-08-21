import tkinter as tk

# Función que hace la operación
def calcular(op):
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        if op == "+":
            resultado.set(num1 + num2)
        elif op == "-":
            resultado.set(num1 - num2)
    except ValueError:
        resultado.set("Error")

# Crear ventana
ventana = tk.Tk()
ventana.title("Calculadora simple")

# Entradas
entry1 = tk.Entry(ventana)
entry1.pack(pady=5)

entry2 = tk.Entry(ventana)
entry2.pack(pady=5)

# Botones
tk.Button(ventana, text="Sumar", command=lambda: calcular("+")).pack(pady=5)
tk.Button(ventana, text="Restar", command=lambda: calcular("-")).pack(pady=5)

# Resultado
resultado = tk.StringVar()
tk.Label(ventana, textvariable=resultado).pack(pady=5)

ventana.mainloop()
