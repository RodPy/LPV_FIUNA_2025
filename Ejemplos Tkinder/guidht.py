import tkinter as tk
import paramiko


app = tk.Tk()
app.title("SSH")
app.geometry("320x260")

var_ip= tk.StringVar()
var_usuario= tk.StringVar()
var_pass= tk.StringVar()

tk.Label(app,text="IP: ").pack()
tk.Entry(app,textvariable=var_ip).pack()

tk.Label(app,text="Usuario: ").pack()
tk.Entry(app,textvariable=var_usuario).pack()

tk.Label(app,text="Pass: ").pack()
tk.Entry(app,textvariable=var_pass).pack()

def conectar():
    ip = var_ip.get()
    usuario = var_usuario.get()
    password = var_pass.get()
    print(f"Conectando a {ip} con usuario {usuario} y password {password}")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, username=usuario, password=password)
    # stdin, stdout, stderr = ssh.exec_command("ls /home/pi/Desktop")
    stdin, stdout, stderr = ssh.exec_command("rm -R /home/pi/Desktop/hola")
    
    print(stdout.read().decode())
    ssh.close()

tk.Button(app,text="Conectar",command=conectar).pack()
app.mainloop()
