
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Layout: grid()")

    tk.Label(root, text="Usuario:").grid(row=0, column=0, sticky="e", padx=4, pady=4)
    tk.Entry(root).grid(row=0, column=1, padx=4, pady=4)

    tk.Label(root, text="Contraseña:").grid(row=1, column=0, sticky="e", padx=4, pady=4)
    tk.Entry(root, show="*").grid(row=1, column=1, padx=4, pady=4)

    tk.Button(root, text="Ingresar").grid(row=2, column=0, columnspan=2, pady=8)

    # Hacer que las columnas crezcan
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=2)

    root.mainloop()

if __name__ == "__main__":
    main()
