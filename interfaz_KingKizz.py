import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from trivia_client import openSession, getList
from ruleta import Ruleta

Usuarios_File = "usuarios.txt"
Base_Url = "http://localhost:80"

def cargar_usuarios():
    """
    Carga los usuarios del archivo `usuarios.txt` y los devuelve como una lista de diccionarios.
    Filtra líneas vacías o mal formateadas.
    """
    usuarios = []
    try:
        with open(Usuarios_File, "r", encoding="utf-8") as file:
            for linea in file:
                datos = linea.strip().split(",")
                if len(datos) == 4:  # Asegurarse de que la línea tenga el formato correcto
                    nombre, contrasena, puntaje, estado = datos
                    usuarios.append({
                        "nombre": nombre,
                        "contrasena": contrasena,
                        "puntaje": int(puntaje),
                        "estado": estado
                    })
    except FileNotFoundError:
        # Si el archivo no existe, lo creamos vacío
        with open(Usuarios_File, "w", encoding="utf-8") as file:
            pass
    return usuarios

def guardar_usuarios(usuarios):
    """
    Guarda los usuarios en el archivo `usuarios.txt`.
    """
    with open(Usuarios_File, "w", encoding="utf-8") as file:
        for usuario in usuarios:
            file.write(f"{usuario['nombre']},{usuario['contrasena']},{usuario['puntaje']},{usuario['estado']}\n")

class VentanaPrincipal(tk.Tk):
    def __init__(self):
        """
        Ventana principal para manejar registro, inicio de sesión y mostrar usuarios conectados.
        """
        super().__init__()
        self.title("Gestión de Sesión")
        self.geometry("400x400")

        # Cargar imagen de fondo
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.cargar_fondo("le1.jpeg")

        # Componentes de la interfaz
        tk.Label(self, text="Usuario", font=("Arial", 14), bg="white").place(x=120, y=100)
        self.entry_usuario = tk.Entry(self, font=("Arial", 12))
        self.entry_usuario.place(x=120, y=130, width=160)

        tk.Label(self, text="Contraseña", font=("Arial", 14), bg="white").place(x=120, y=160)
        self.entry_contrasena = tk.Entry(self, font=("Arial", 12), show="*")
        self.entry_contrasena.place(x=120, y=190, width=160)

        tk.Button(self, text="Registrar Usuario", font=("Arial", 12), command=self.registrar_usuario).place(x=120, y=230, width=160)
        tk.Button(self, text="Iniciar Sesión", font=("Arial", 12), command=self.iniciar_sesion).place(x=120, y=270, width=160)
        tk.Button(self, text="Ver Usuarios Conectados", font=("Arial", 12), command=self.mostrar_usuarios).place(x=120, y=310, width=160)

    def cargar_fondo(self, ruta_imagen):
        """
        Carga una imagen de fondo para la ventana principal.
        """
        try:
            imagen = Image.open(ruta_imagen)
            imagen = imagen.resize((400, 400), Image.Resampling.LANCZOS)
            self.fondo = ImageTk.PhotoImage(imagen)
            self.canvas.create_image(0, 0, image=self.fondo, anchor="nw")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen de fondo: {e}")

    def registrar_usuario(self):
        """
        Registra un nuevo usuario en `usuarios.txt` si no existe.
        """
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos Vacíos", "Debe llenar todos los campos.")
            return

        usuarios = cargar_usuarios()
        if any(u["nombre"] == usuario for u in usuarios):
            messagebox.showerror("Error", "El usuario ya existe.")
            return

        usuarios.append({"nombre": usuario, "contrasena": contrasena, "puntaje": 0, "estado": "desconectado"})
        guardar_usuarios(usuarios)
        messagebox.showinfo("Registro", "Usuario registrado exitosamente.")
        self.limpiar_campos()

    def iniciar_sesion(self):
        """
        Inicia sesión verificando el usuario y contraseña con `trivia_client` y actualiza el archivo local.
        """
        usuario = self.entry_usuario.get().strip()
        contrasena = self.entry_contrasena.get().strip()

        if not usuario or not contrasena:
            messagebox.showwarning("Campos Vacíos", "Debe llenar todos los campos.")
            return

        try:
            respuesta = openSession(Base_Url, usuario, contrasena)
            if "iniciada" in respuesta.lower():
                usuarios = cargar_usuarios()
                for u in usuarios:
                    if u["nombre"] == usuario:
                        u["estado"] = "conectado"
                        guardar_usuarios(usuarios)
                        break
                messagebox.showinfo("Inicio de Sesión", "Sesión iniciada exitosamente.")
                self.limpiar_campos()
                self.abrir_ventana_ruleta(usuario, contrasena)
            else:
                messagebox.showerror("Error", respuesta)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar sesión: {e}")

    def abrir_ventana_ruleta(self, username, password):
        """
        Abre la ventana de la ruleta tras iniciar sesión correctamente.
        """
        ventana_ruleta = tk.Toplevel(self)
        ventana_ruleta.geometry("700x800")
        ventana_ruleta.title("Ruleta de Trivia")
        
        # Crear instancia de Ruleta con los argumentos requeridos
        Ruleta(ventana_ruleta, username, password, Base_Url)

    def mostrar_usuarios(self):
        """
        Muestra una lista de usuarios conectados obtenidos con `trivia_client`.
        """
        try:
            usuario = self.entry_usuario.get().strip()
            contrasena = self.entry_contrasena.get().strip()

            if not usuario or not contrasena:
                messagebox.showwarning("Campos Vacíos", "Debe llenar todos los campos.")
                return

            respuesta = getList(Base_Url, usuario, contrasena)
            if respuesta:
                messagebox.showinfo("Usuarios Conectados", f"Usuarios conectados:\n{respuesta}")
            else:
                messagebox.showinfo("Usuarios Conectados", "No hay usuarios conectados en este momento.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo obtener la lista de usuarios: {e}")

    def limpiar_campos(self):
        """
        Limpia los campos de entrada de usuario y contraseña.
        """
        self.entry_usuario.delete(0, tk.END)
        self.entry_contrasena.delete(0, tk.END)


if __name__ == "__main__":
    app = VentanaPrincipal()
    app.mainloop()
