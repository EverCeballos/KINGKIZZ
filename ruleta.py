import tkinter as tk
from PIL import Image, ImageTk
import math
from tkinter import messagebox
from trivia_client import closeSession, getScore, updateScore
import random
import json

# Constantes para la ubicación de preguntas y servidor
Preguntas_File = {
    "preguntas0.txt",  # Deportes
    "preguntas1.txt",  # Música
    "preguntas2.txt",  # Cultura General
    "preguntas3.txt",  # Cine y Películas
    "preguntas4.txt",  # Historia
    "preguntas5.txt"   # Videojuegos
}

Base_Url = "http://localhost:80"


class Ruleta:
    def __init__(self, root, username, password, base_url):
        self.root = root
        self.username = username
        self.password = password
        self.base_url = base_url
        self.puntaje = int(self.obtener_puntaje())  # Obtener el puntaje inicial desde el servidor
        self.root.title("Ruleta de Trivia")
        self.root.geometry("700x800")

        self.frame_ruleta = tk.Frame(self.root, bg="#f0f0f0")
        self.frame_ruleta.pack(fill=tk.BOTH, expand=True)

        self.ruleta_image = Image.open("Ruleta.png")
        self.ruleta_image = self.ruleta_image.resize((400, 400))
        self.ruleta_photo = ImageTk.PhotoImage(self.ruleta_image)

        self.canvas = tk.Canvas(self.frame_ruleta, width=500, height=500, bg="#ffffff", bd=0, highlightthickness=0)
        self.canvas.pack(pady=20)
        self.canvas.create_image(250, 250, image=self.ruleta_photo)

        self.angle = 0
        self.center_x = 250
        self.center_y = 250
        self.radius = 200
        self.flecha_radius = 100
        self.initial_speed = 30
        self.speed = 0
        self.deceleration = 0.5
        self.flecha = None
        self.girando = False

        self.categorias = ["Musica", "Deportes", "Cultura General",
                           "Cine y Peliculas", "Historia", "Videojuegos"]

        self.label_categoria = tk.Label(self.frame_ruleta, text="Selecciona una categoria", font=("Arial", 14), bg="#f0f0f0", fg="#333")
        self.label_categoria.pack()

        self.boton_iniciar = tk.Button(self.frame_ruleta, text="Iniciar Ruleta", font=("Arial", 12), command=self.iniciar_ruleta, bg="#4CAF50", fg="#fff")
        self.boton_iniciar.pack(pady=10)

        self.boton_ver_puntaje = tk.Button(self.frame_ruleta, text="Ver Puntaje", font=("Arial", 12), command=self.ver_puntaje, bg="#008CBA", fg="#fff")
        self.boton_ver_puntaje.pack(pady=10)

        self.boton_cerrar_sesion = tk.Button(self.frame_ruleta, text="Cerrar Sesion", font=("Arial", 12), command=self.cerrar_sesion, bg="#f44336", fg="#fff")
        self.boton_cerrar_sesion.pack(pady=10)

    def obtener_puntaje(self):
        """Obtiene el puntaje actual desde el servidor usando `getScore`."""
        try:
            puntaje = getScore(self.base_url, self.username, self.password)
            return puntaje
        except Exception as e:
            print(f"Error al obtener el puntaje: {e}")
            return 0

    def actualizar_puntaje(self, puntos):
        """Actualiza el puntaje en el servidor usando `updateScore`."""
        try:
            nuevo_puntaje = self.puntaje + puntos
            print(f"Actualizando puntaje. Puntaje actual: {self.puntaje}, Nuevo puntaje: {nuevo_puntaje}")

            mensaje = updateScore(self.base_url, self.username, self.password, nuevo_puntaje)
            print(f"Respuesta del servidor: {mensaje}")

            if isinstance(mensaje, str) and "Actualizado" in mensaje:
                self.puntaje = nuevo_puntaje
                messagebox.showinfo("Puntaje Actualizado", "Tu puntaje ha sido actualizado a: " + str(self.puntaje))
            else:
                messagebox.showerror("Error", "No se pudo actualizar el puntaje. Respuesta: " + str(mensaje))
        except Exception as e:
            print(f"Error al actualizar el puntaje: {e}")
            messagebox.showerror("Error", "Error al actualizar el puntaje: " + str(e))

    def iniciar_ruleta(self):
        if not self.girando:  # Evitar que se inicie otra vez mientras está girando
            self.boton_iniciar.config(state=tk.DISABLED)  # Deshabilitar el botón
            self.speed = self.initial_speed
            self.girando = True
            self.animar_flecha()
            
    def animar_flecha(self):
        if self.speed > 0:
            self.angle += self.speed
            self.speed -= self.deceleration

            if self.angle >= 360:
                self.angle -= 360

            if self.flecha:
                self.canvas.delete(self.flecha)

            self.flecha = self.dibujar_flecha(self.angle)

            categoria = self.obtener_categoria(self.angle)
            self.label_categoria.config(text=f"Categoria: {categoria}")

            self.root.after(50, self.animar_flecha)
        else:
            self.girando = False
            self.finalizar_ruleta()

    def finalizar_ruleta(self):
        categoria = self.obtener_categoria(self.angle)
        self.label_categoria.config(text=f"Categoría seleccionada: {categoria}")
        self.boton_iniciar.config(state=tk.NORMAL)  # Habilitar el botón nuevamente
        self.mostrar_pregunta(categoria)

    def mostrar_pregunta(self, categoria):
        try:
            pregunta, opciones, respuesta_correcta = self.obtener_pregunta_y_opciones(categoria)
            if pregunta:
                self.mostrar_ventana_respuesta(pregunta, opciones, respuesta_correcta)
            else:
                messagebox.showerror("Error", "No se pudo obtener la pregunta.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener la pregunta: {e}")

    def obtener_pregunta_y_opciones(self, categoria):
        archivo = f"preguntas{self.categorias.index(categoria)}.txt"
        try:
            with open(archivo, 'r', encoding="utf-8") as file:
                preguntas = json.load(file)
                pregunta_data = random.choice(preguntas)
                pregunta = pregunta_data["pregunta"]
                opciones = list(pregunta_data["opciones"].values())
                respuesta_correcta = pregunta_data["respuesta_correcta"]
                return pregunta, opciones, respuesta_correcta
        except FileNotFoundError:
            messagebox.showerror("Error", f"No se encontró el archivo {archivo}.")
            return None, None, None

    def mostrar_ventana_respuesta(self, pregunta, opciones, respuesta_correcta):
        self.ventana_respuesta = tk.Toplevel(self.root)
        self.ventana_respuesta.title("Pregunta")
        self.ventana_respuesta.geometry("400x300")
        
        label_pregunta = tk.Label(self.ventana_respuesta, text=pregunta, font=("Arial", 14), wraplength=350)
        label_pregunta.pack(pady=20)

        opciones_con_letras = ['a', 'b', 'c', 'd']
        for i, opcion in enumerate(opciones):
            boton_opcion = tk.Button(self.ventana_respuesta, text=f"{opciones_con_letras[i].upper()}. {opcion}", font=("Arial", 12), command=lambda opt=opciones_con_letras[i]: self.elegir_respuesta(opt, respuesta_correcta))
            boton_opcion.pack(pady=5)

    def elegir_respuesta(self, opcion, respuesta_correcta):
        if opcion == respuesta_correcta:
            messagebox.showinfo("Respuesta Correcta", "¡Correcto! Has ganado 10 puntos.")
            self.actualizar_puntaje(10)
        else:
            messagebox.showinfo("Respuesta Incorrecta", "Respuesta incorrecta. No se sumaron puntos.")
        self.ventana_respuesta.destroy()
        print("Regresando a la ruleta...")

    def obtener_categoria(self, angle):
        index = int((angle % 360) / (360 / len(self.categorias)))
        return self.categorias[index]

    def dibujar_flecha(self, angle):
        radianes = math.radians(angle)
        x1 = self.center_x + self.flecha_radius * math.cos(radianes)
        y1 = self.center_y + self.flecha_radius * math.sin(radianes)
        return self.canvas.create_line(self.center_x, self.center_y, x1, y1, width=3, fill="red")

    def ver_puntaje(self):
        messagebox.showinfo("Puntaje Actual", f"Tu puntaje es: {self.puntaje}")

    def cerrar_sesion(self):
        try:
            mensaje = closeSession(self.base_url, self.username, self.password)
            if "Sseccion cerrada":
                self.root.quit()
            else:
                messagebox.showerror("Error", mensaje)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cerrar sesión: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = Ruleta(root, "usuario", "contraseña", Base_Url)
    root.mainloop()
