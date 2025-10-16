"""
serial_viewer_db.py
Visor serial mínimo con Tkinter que almacena automáticamente números en SQLite
usando el módulo serial_db.py

Requisitos:
    pip install pyserial
Archivos:
    - serial_db.py (en la misma carpeta)
"""

import tkinter as tk
import serial
import serial.tools.list_ports
from tkinter import ttk
import serial_db as sdb  # módulo de DB separado

DB_PATH = "serial_data.sqlite3"  # puedes cambiar la ruta si quieres

class SerialViewerDB(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Arduino Serial Viewer + SQLite")
        self.geometry("640x420")

        # Estado de Serial y buffer de líneas
        self.ser = None
        self.buf = ""                 # buffer de texto para reconstruir líneas completas
        self.read_interval_ms = 50    # período de lectura

        # Inicializar DB
        sdb.init_db(DB_PATH)

        # --- UI Superior ---
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        ttk.Button(top, text="Actualizar puertos", command=self.listar_puertos).pack(side="left")

        self.puerto_var = tk.StringVar()
        self.menu_puertos = ttk.Combobox(top, textvariable=self.puerto_var, width=28, state="readonly")
        self.menu_puertos.pack(side="left", padx=6)

        ttk.Label(top, text="Baud:").pack(side="left")
        self.baud_var = tk.StringVar(value="9600")
        self.baud_combo = ttk.Combobox(top, textvariable=self.baud_var, width=8,
                                       values=["9600","115200","57600","38400","19200","4800"], state="readonly")
        self.baud_combo.pack(side="left", padx=6)

        self.chk_guardar_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(top, text="Guardar en DB", variable=self.chk_guardar_var).pack(side="left", padx=8)

        ttk.Button(top, text="Conectar", command=self.conectar).pack(side="left", padx=6)
        ttk.Button(top, text="Desconectar", command=self.desconectar).pack(side="left")

        # --- Text area ---
        mid = ttk.Frame(self, padding=(8,0,8,8))
        mid.pack(fill="both", expand=True)
        self.texto = tk.Text(mid, wrap="none")
        self.texto.pack(side="left", fill="both", expand=True)
        yscroll = ttk.Scrollbar(mid, orient="vertical", command=self.texto.yview)
        yscroll.pack(side="right", fill="y")
        self.texto.configure(yscrollcommand=yscroll.set)

        # --- Barra inferior ---
        bottom = ttk.Frame(self, padding=(8,0,8,8))
        bottom.pack(fill="x")
        self.estado = tk.StringVar(value="Desconectado")
        ttk.Label(bottom, textvariable=self.estado).pack(side="left")
        ttk.Button(bottom, text="Últimos 10", command=self.mostrar_recientes).pack(side="right")
        self.contador_var = tk.StringVar()
        ttk.Label(bottom, textvariable=self.contador_var).pack(side="right", padx=(0,12))

        self.actualizar_contador()
        self.listar_puertos()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    # --- Serial & Lectura ---
    def listar_puertos(self):
        puertos = [p.device for p in serial.tools.list_ports.comports()]
        self.menu_puertos["values"] = puertos
        if puertos:
            self.puerto_var.set(puertos[0])
        self.estado.set(f"Puertos: {', '.join(puertos) if puertos else 'ninguno'}")

    def conectar(self):
        if self.ser:
            return
        port = self.puerto_var.get()
        if not port:
            self.estado.set("Selecciona un puerto.")
            return
        try:
            baud = int(self.baud_var.get())
        except ValueError:
            self.estado.set("Baud inválido.")
            return

        try:
            self.ser = serial.Serial(port, baud, timeout=0)
            self.estado.set(f"Conectado a {port} @ {baud}")
            self.after(self.read_interval_ms, self.loop_lectura)
        except Exception as e:
            self.ser = None
            self.estado.set(f"Error al conectar: {e}")

    def desconectar(self):
        if self.ser:
            try:
                self.ser.close()
            except:
                pass
            self.ser = None
        self.estado.set("Desconectado")

    def loop_lectura(self):
        if not self.ser:
            return
        try:
            n = self.ser.in_waiting
            if n:
                # Leemos bytes, decodificamos, y reconstruimos líneas con '\n'
                data = self.ser.read(n).decode("utf-8", errors="ignore")
                self.buf += data
                *lineas_completas, self.buf = self.buf.split("\n")
                for linea in lineas_completas:
                    self.procesar_linea(linea)
        except Exception as e:
            self.estado.set(f"Error de lectura: {e}")
            self.desconectar()
            return
        self.after(self.read_interval_ms, self.loop_lectura)

    def procesar_linea(self, linea: str):
        """Muestra la línea en el Text y, si corresponde, la guarda en DB."""
        # Mostrar
        self.texto.insert("end", linea + "\n")
        self.texto.see("end")

        # Guardar (si checkbox activo y hay números)
        if self.chk_guardar_var.get():
            inserted = sdb.insert_from_line(
                port=self.puerto_var.get(),
                baud=int(self.baud_var.get()),
                line=linea,
                db_path=DB_PATH
            )
            if inserted:
                self.actualizar_contador()

    # --- Utilidades UI ---
    def actualizar_contador(self):
        try:
            total = sdb.count(DB_PATH)
        except Exception as e:
            self.contador_var.set(f"DB Err: {e}")
            return
        self.contador_var.set(f"Guardados: {total}")

    def mostrar_recientes(self):
        try:
            filas = sdb.recent(10, DB_PATH)
        except Exception as e:
            self.texto.insert("end", f"[DB error] {e}\n")
            self.texto.see("end")
            return
        self.texto.insert("end", "\n=== Últimos 10 registros ===\n")
        for rid, ts, port, baud, raw, val in filas:
            self.texto.insert("end", f"#{rid} [{ts}] {port}@{baud}  value={val}  raw='{raw}'\n")
        self.texto.insert("end", "============================\n\n")
        self.texto.see("end")

    def on_close(self):
        self.desconectar()
        self.destroy()

if __name__ == "__main__":
    app = SerialViewerDB()
    app.mainloop()
