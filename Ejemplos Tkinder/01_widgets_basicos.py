
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Widgets básicos - Tkinter")

    # 1) Label
    tk.Label(root, text="Hola, soy un Label").pack(pady=4)

    # 2) Button
    def saludar():
        print("¡Hola desde el botón!")
    tk.Button(root, text="Haz clic", command=saludar).pack(pady=4)

    # 3) Entry
    tk.Label(root, text="Entrada de texto:").pack()
    entrada = tk.Entry(root)
    entrada.pack(pady=4)

    # 4) Text
    tk.Label(root, text="Texto multilínea:").pack()
    texto = tk.Text(root, height=4, width=40)
    texto.insert("end", "Escribe aquí...")
    texto.pack(pady=4)

    # 5) Checkbutton
    var_check = tk.BooleanVar(value=False)
    tk.Checkbutton(root, text="Acepto términos", variable=var_check).pack(pady=4)

    # 6) Radiobutton
    tk.Label(root, text="Elige una opción:").pack()
    var_radio = tk.StringVar(value="1")
    tk.Radiobutton(root, text="Opción 1", variable=var_radio, value="1").pack()
    tk.Radiobutton(root, text="Opción 2", variable=var_radio, value="2").pack()

    # 7) Listbox
    tk.Label(root, text="Lista de elementos:").pack()
    lista = tk.Listbox(root, height=4)
    for i, item in enumerate(["Elemento 1", "Elemento 2", "Elemento 3"], start=1):
        lista.insert(i, item)
    lista.pack(pady=4)

    # 8) Frame
    frame = tk.Frame(root, borderwidth=2, relief="groove")
    frame.pack(padx=8, pady=8, fill="x")
    tk.Label(frame, text="Estoy dentro de un Frame").pack(pady=4)

    # 9) Canvas
    cnv = tk.Canvas(root, width=220, height=120, bg="white")
    cnv.pack(pady=4)
    cnv.create_line(10, 10, 210, 110, fill="blue", width=2)
    cnv.create_oval(60, 30, 160, 90, fill="red")

    # 10) Scale
    tk.Label(root, text="Selecciona un valor:").pack()
    tk.Scale(root, from_=0, to=100, orient="horizontal").pack(pady=4)

    # 11) Spinbox
    tk.Label(root, text="Spinbox numérico:").pack()
    tk.Spinbox(root, from_=0, to=10).pack(pady=4)

    # 12) Message
    tk.Message(root, width=300, text="Este es un widget Message que se ajusta al ancho.").pack(pady=4)

    root.mainloop()

if __name__ == "__main__":
    main()
