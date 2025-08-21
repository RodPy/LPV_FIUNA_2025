zxc
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Eventos básicos")

    salida = tk.Text(root, height=8, width=40)
    salida.pack(padx=8, pady=8)

    # --- Button con command ---
    def saludar():
        salida.insert("end", "¡Hola desde command en Button!\n")
    tk.Button(root, text="Saludar", command=saludar).pack(pady=4)

    # --- Eventos de teclado ---
    def on_key(event):
        salida.insert("end", f"Tecla: {event.keysym} ({event.char!r})\n")
    root.bind("<Key>", on_key)

    # --- Eventos de mouse ---
    def on_click(event):
        salida.insert("end", f"Clic en ({event.x}, {event.y})\n")
    root.bind("<Button-1>", on_click)

    # --- Eventos de ventana ---
    def on_configure(event):
        salida.insert("end", f"Tamaño: {event.width}x{event.height}\n")
    root.bind("<Configure>", on_configure)

    root.mainloop()

if __name__ == "__main__":
    main()
