
import tkinter as tk
from tkinter import ttk

def main():
    root = tk.Tk()
    root.title("Ejemplo completo: Widgets + Layouts + Eventos")
    root.geometry("520x420")

    # ---- Layout principal con grid ----
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=2)
    root.rowconfigure(3, weight=1)

    # ---- Sección formulario (grid) ----
    ttk.Label(root, text="Nombre:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
    nombre = ttk.Entry(root)
    nombre.grid(row=0, column=1, sticky="ew", padx=6, pady=6)

    ttk.Label(root, text="Edad:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
    edad = ttk.Spinbox(root, from_=0, to=120, width=10)
    edad.grid(row=1, column=1, sticky="w", padx=6, pady=6)

    acepta = tk.BooleanVar()
    ttk.Checkbutton(root, text="Acepto términos", variable=acepta).grid(row=2, column=1, sticky="w", padx=6, pady=6)

    # ---- Listbox dentro de un Frame (pack) ----
    frame_lista = ttk.LabelFrame(root, text="Intereses")
    frame_lista.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
    frame_lista.columnconfigure(0, weight=1)
    frame_lista.rowconfigure(0, weight=1)

    lista = tk.Listbox(frame_lista, height=5)
    for item in ["Python", "Robótica", "Electrónica", "IA", "Ciencia de Datos"]:
        lista.insert("end", item)
    lista.pack(fill="both", expand=True, padx=6, pady=6)

    # ---- Canvas con place ----
    lienzo = tk.Canvas(root, width=180, height=120, bg="white", highlightthickness=1, highlightbackground="#ccc")
    lienzo.grid(row=4, column=0, columnspan=2, pady=6)
    # Dibujos simples
    lienzo.create_oval(20, 20, 80, 80, fill="skyblue")
    lienzo.create_rectangle(100, 30, 160, 90, fill="lightgreen")

    # Mostrar tooltip simple usando place()
    tooltip = tk.Label(root, text="Doble clic en el lienzo para limpiar", bg="#ffffe0", relief="solid", bd=1)
    tooltip.place(relx=0.5, rely=0.91, anchor="center")

    # ---- Área de salida ----
    salida = tk.Text(root, height=6)
    salida.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)

    # ---- Botones de acción ----
    def registrar():
        sel = lista.get("active")
        salida.insert("end", f"Registrado: nombre={nombre.get()}, edad={edad.get()}, interés={sel}, acepta={acepta.get()}\n")

    def limpiar_salida():
        salida.delete("1.0", "end")

    btns = ttk.Frame(root)
    btns.grid(row=6, column=0, columnspan=2, pady=6)
    ttk.Button(btns, text="Registrar", command=registrar).pack(side="left", padx=4)
    ttk.Button(btns, text="Limpiar salida", command=limpiar_salida).pack(side="left", padx=4)

    # ---- Eventos ----
    def on_key_return(event):
        registrar()
    root.bind("<Return>", on_key_return)

    def on_canvas_double(event):
        lienzo.delete("all")
        salida.insert("end", "Lienzo limpiado\n")
    lienzo.bind("<Double-Button-1>", on_canvas_double)

    root.mainloop()

if __name__ == "__main__":
    main()
