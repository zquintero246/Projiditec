import firebase_admin
from firebase_admin import credentials, db
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from os import urandom
import base64

# Inicializar Firebase
cred = credentials.Certificate(r"C:\Users\cricr\PycharmProjects\pythonProject\encriptador-63d6f-firebase-adminsdk-sk9e2-923a3bc86c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://encriptador-63d6f-default-rtdb.firebaseio.com'
})

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

root = tk.Tk()
root.title("Encriptador/Desencriptador de Mensajes")
root.geometry("500x300")
root.configure(bg="lightgrey")
style = ttk.Style()
style.theme_use("clam")

clave_usuario_label = tk.Label(root, text="Introduce tu clave de encriptación (opcional):", bg="lightgrey")
clave_usuario_entry = tk.Entry(root)
clave_usuario_label.pack(pady=10)
clave_usuario_entry.pack(pady=10)

mensaje_label = tk.Label(root, text="Introduce el mensaje a encriptar:", bg="lightgrey")
mensaje_entry = tk.Entry(root)
encriptar_button = tk.Button(root, text="Encriptar", command=encriptar_mensaje)

mensaje_label.pack(pady=10)
mensaje_entry.pack(pady=10)
encriptar_button.pack(pady=10)

clave_label = tk.Label(root, bg="lightgrey")
clave_label.pack(pady=10)

token_label = tk.Label(root, text="Introduce el mensaje a desencriptar:", bg="lightgrey")
token_entry = tk.Entry(root)
desencriptar_button = tk.Button(root, text="Desencriptar", command=desencriptar_mensaje)

token_label.pack(pady=10)
token_entry.pack(pady=10)
desencriptar_button.pack(pady=10)

mensaje_desencriptado_label = tk.Label(root, bg="lightgrey")
mensaje_desencriptado_label.pack(pady=10)

root.mainloop()