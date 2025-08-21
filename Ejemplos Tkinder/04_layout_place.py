
import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Layout: place()")
    root.geometry("320x220")

    tk.Label(root, text="(50, 50)", bg="lightblue").place(x=50, y=50)
    tk.Label(root, text="Centro", bg="lightgreen").place(relx=0.5, rely=0.5, anchor="center")
    tk.Label(root, text="Esquina", bg="lightpink").place(relx=1.0, rely=1.0, anchor="se")

    root.mainloop()

if __name__ == "__main__":
    main()
