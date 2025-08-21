
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Layout: pack()")

    tk.Label(root, text="Arriba", bg="lightblue").pack(side="top", fill="x")
    tk.Label(root, text="Izquierda", bg="lightgreen").pack(side="left", fill="y")
    tk.Label(root, text="Derecha", bg="lightpink").pack(side="right", fill="y")
    tk.Label(root, text="Abajo", bg="lightyellow").pack(side="bottom", fill="x")

    root.mainloop()

if __name__ == "__main__":
    main()
