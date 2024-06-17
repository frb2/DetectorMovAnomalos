import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw, UnidentifiedImageError
import subprocess
import os

class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        widget.bind("<Enter>", self.enter)
        widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# Funciones para los botones
def iniciar_detector():
    global process
    try:
        process = subprocess.Popen(["python", "main.py"])  
        messagebox.showinfo("Iniciar detector", "El detector ha sido iniciado.")
        estado_detector.config(text="Estado: Activo", fg="green")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo iniciar el detector: {e}")

def detener_detector():
    global process
    if process:
        process.terminate()
        process = None
        messagebox.showinfo("Detener detector", "El detector ha sido detenido.")
        estado_detector.config(text="Estado: Inactivo", fg="red")
    else:
        messagebox.showwarning("Advertencia", "El detector no está activo.")

def evidencias():
    ruta_carpeta = r"Ejecucion"  
    if os.path.isdir(ruta_carpeta):
        os.startfile(ruta_carpeta)
    else:
        messagebox.showerror("Error", "La ruta especificada no existe.")

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz de Detector")
root.geometry("600x450")  # Dimensiones de la ventana (rectangular)

# Crear un marco principal
main_frame = tk.Frame(root)
main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

# Título y descripción
titulo = tk.Label(main_frame, text="Sistema de Detección", font=("Helvetica", 16, "bold"))
titulo.pack(pady=10)

descripcion = tk.Label(main_frame, text="Utilice los botones a continuación para controlar el detector.", font=("Helvetica", 12))
descripcion.pack(pady=5)

# Separador
separator = ttk.Separator(main_frame, orient='horizontal')
separator.pack(fill='x', pady=10)

# Estado del detector
estado_detector = tk.Label(main_frame, text="Estado: Inactivo", font=("Helvetica", 12), fg="red")
estado_detector.pack(pady=5)

# Crear un marco para centrar los botones
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=20)

# Cargar iconos para los botones
def cargar_icono(path, size):
    try:
        image = Image.open(path)
        image = image.resize((size, size), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(image)
    except (UnidentifiedImageError, FileNotFoundError) as e:
        print(f"Error al cargar la imagen {path}: {e}")
        return crear_icono_canvas("gray", size)

# Crear un icono alternativo en memoria usando PIL
def crear_icono_canvas(color, size):
    image = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((2, 2, size-2, size-2), fill=color, outline=color)
    return ImageTk.PhotoImage(image)

# Definir el tamaño del icono
icon_size = 20

icono_iniciar = cargar_icono("start.png", icon_size) or crear_icono_canvas("white", icon_size)
icono_detener = cargar_icono("stop.png", icon_size) or crear_icono_canvas("lightcoral", icon_size)
icono_evidencias = cargar_icono("archivo.png", icon_size) or crear_icono_canvas("lightgreen", icon_size)

# Crear y configurar los botones
boton1 = tk.Button(button_frame, text=" Iniciar detector", bg="white", command=iniciar_detector, image=icono_iniciar, compound="left")
boton1.pack(fill=tk.X, padx=20, pady=10)

boton2 = tk.Button(button_frame, text=" Detener detector", bg="lightcoral", command=detener_detector, image=icono_detener, compound="left")
boton2.pack(fill=tk.X, padx=20, pady=10)

boton3 = tk.Button(button_frame, text=" Evidencias", bg="lightgreen", command=evidencias, image=icono_evidencias, compound="left")
boton3.pack(fill=tk.X, padx=20, pady=10)

# Añadir tooltips a los botones
ToolTip(boton1, "Haga clic para iniciar el detector")
ToolTip(boton2, "Haga clic para detener el detector")
ToolTip(boton3, "Haga clic para mostrar evidencias")

# Variable global para el proceso
process = None

# Ejecutar la aplicación
root.mainloop()
