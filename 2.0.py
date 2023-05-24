import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom
import base64

# Inicializar Firebase
cred = credentials.Certificate(r"C:\Users\cricr\PycharmProjects\pythonProject\encriptador-63d6f-firebase-adminsdk-sk9e2-923a3bc86c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://encriptador-63d6f-default-rtdb.firebaseio.com'
})
#Genera una clave de cifrado aleatoria de 32 bytes
def generar_clave():
    return urandom(32)

def encriptar(mensaje, clave):
    iv = urandom(16)
    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), default_backend())
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(mensaje.encode()) + padder.finalize()
    ct = encryptor.update(padded_data) + encryptor.finalize()
    return base64.b64encode(iv + ct).decode('utf-8')

def desencriptar(token, clave):
    data = base64.b64decode(token)
    iv = data[:16]
    ct = data[16:]
    cipher = Cipher(algorithms.AES(clave), modes.CBC(iv), default_backend())
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ct) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data)
    return (data + unpadder.finalize()).decode('utf-8')

def encriptar_mensaje():
    mensaje = mensaje_entry.get()
    clave_usuario = clave_usuario_entry.get()
    global clave
    clave = base64.b64decode(clave_usuario) if clave_usuario else generar_clave()
    token = encriptar(mensaje, clave)
    token_entry.delete(0, 'end')
    token_entry.insert(0, token)
    clave_label['text'] = 'Clave: ' + base64.b64encode(clave).decode('utf-8')
    # Guardar el mensaje encriptado en Firebase
    ref = db.reference('mensajes')
    ref.push({
        'mensaje': token,
        'clave': base64.b64encode(clave).decode('utf-8') if not clave_usuario else clave_usuario
    })

def desencriptar_mensaje():
    token = token_entry.get()
    global clave
    try:
        mensaje = desencriptar(token, clave)
        mensaje_desencriptado_label['text'] = 'Mensaje desencriptado: ' + mensaje
    except:
        messagebox.showerror("Error", "No se pudo desencriptar el mensaje. Verifique la clave y el mensaje cifrado.")

root = ThemedTk(theme="radiance")
root.title("Encriptador/Desencriptador de Mensajes")
root.geometry("500x300")

# Cambiar color del fondo
root.configure(bg="#d3d3d3")  # light gray

# Cambiar fuente
custom_font = ("Arial", 12)

clave_usuario_label = tk.Label(root, text="Introduce tu clave de encriptación (opcional):", font=custom_font, bg="#d3d3d3")
clave_usuario_entry = tk.Entry(root, font=custom_font)
clave_usuario_entry.insert(0, "")

mensaje_label = tk.Label(root, text="Introduce el mensaje a encriptar:", font=custom_font, bg="#d3d3d3")
mensaje_entry = tk.Entry(root, font=custom_font)
mensaje_entry.insert(0, "")
encriptar_button = ttk.Button(root, text="Encriptar", command=encriptar_mensaje)

clave_label = tk.Label(root, font=custom_font, bg="#d3d3d3")

token_label = tk.Label(root, text="Introduce el mensaje a desencriptar:", font=custom_font, bg="#d3d3d3")
token_entry = tk.Entry(root, font=custom_font)
token_entry.insert(0, "")
desencriptar_button = ttk.Button(root, text="Desencriptar", command=desencriptar_mensaje)

mensaje_desencriptado_label = tk.Label(root, font=custom_font, bg="#d3d3d3")

# Center the widgets
clave_usuario_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
clave_usuario_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

mensaje_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
mensaje_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
encriptar_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

clave_label.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

token_label.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
token_entry.place(relx=0.5, rely=0.8, anchor=tk.CENTER)
desencriptar_button.place(relx=0.5, rely=0.9, anchor=tk.CENTER)

mensaje_desencriptado_label.place(relx=0.5, rely=1.0, anchor=tk.S)

root.mainloop()
