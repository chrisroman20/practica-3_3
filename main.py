# Autor: Roman Castro Christopher Alexander 
# Contacto: l20211837@tectijuana.edu.mx
# Fecha: 2023-11-01 
# Descripción: Código que muestra la temperatura en un dispositivo I2C y muestra diferentes imágenes en el mismo dependiendo de la temperatura detectada por el controlador integrado en la Raspberry Pi Pico.

from machine import Pin
import machine
import ssd1306
import time
import framebuf
import machine
import math

# Configuración de la pantalla OLED
i2c = machine.I2C(0, sda=machine.Pin(16), scl=machine.Pin(17))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Definición de las opciones del menú
menu_options = ["Hola Mundo", "Encender LED", "Cuadrado", "Temperatura"]
selected_option = 0

# Configuración de los pines para los botones
button_a = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
button_b = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
button_c = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_UP)

# Iconos en forma de bytearrays (32x32)
icon_arrow = bytearray(b'\x00\xe0\x00\x00\x01\xf0\x00\x00\x01\xf8\x00\x00\x01\xfc\x00\x00\x00\xfe\x00\x00\x00\x7f\x00\x00\x00?\x80\x00\x00\x1f\xc0\x00\x00\x0f\xe0\x00\x00\x07\xf0\x00\x00\x03\xf8\x00\x00\x01\xfc\x00\x00\x00\xfe\x00\x00\x00\x7f\x00\x00\x00?\x80\x00\x00\x1f\x80\x00\x00\x1f\x80\x00\x00?\x80\x00\x00\x7f\x00\x00\x00\xfe\x00\x00\x01\xfc\x00\x00\x03\xf8\x00\x00\x07\xf0\x00\x00\x0f\xe0\x00\x00\x1f\xc0\x00\x00?\x80\x00\x00\x7f\x00\x00\x00\xfe\x00\x00\x01\xfc\x00\x00\x01\xf8\x00\x00\x01\xf0\x00\x00\x00\xe0\x00\x00')


#led integrado pico w
led = Pin("LED", Pin.OUT)


# Función para dibujar un triángulo en una posición dada
def draw_triangle(x, y):
    oled.fill(0)  # Limpia la pantalla

    # Dibuja las tres líneas que forman el triángulo
    oled.line(x, y, x + 20, y, 1)
    oled.line(x, y, x + 10, y - 20, 1)
    oled.line(x + 20, y, x + 10, y - 20, 1)

    oled.show()  # Muestra el triángulo en la pantalla

def ejecutar_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, "r") as archivo:
            codigo = archivo.read()
            exec(codigo)
    except FileNotFoundError:
        print(f"El archivo '{nombre_archivo}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error al ejecutar el archivo '{nombre_archivo}': {e}")



def DrawTriangle():
    timing = 0
    # Parámetros de la animación
    angle = 0
    center_x = 32
    center_y = 32
    radius = 20

    # Bucle de animación
    while timing < 20:
        oled.fill(0)  # Limpia la pantalla en cada cuadro
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        draw_triangle(x, y)  # Dibuja el triangulo en la nueva posición
        oled.show()  # Muestra el cuadro en la pantalla
        time.sleep(0.05)  # Controla la velocidad de la animación
        angle += 0.1  # Aumenta el ángulo para la rotación
        timing += 1
        print(timing)

# Función para dibujar una línea
def draw_line(x0, y0, x1, y1):
    oled.line(x0, y0, x1, y1, 1)

# Función para dibujar los lados de un cubo en una posición dada
def draw_cube(x, y):
    # Dibuja las líneas horizontales superiores del cubo
    draw_line(x + 10, y + 10, x + 40, y + 10)
    draw_line(x + 10, y + 10, x + 10, y + 40)
    draw_line(x + 40, y + 10, x + 40, y + 40)

    # Dibuja las líneas verticales para conectar los lados
    draw_line(x + 10, y + 10, x + 10, y + 40)
    draw_line(x + 40, y + 10, x + 40, y + 40)
    draw_line(x + 10, y + 40, x + 40, y + 40)

# Función para animar el cubo
def DrawCube():
    timing = 0
    # Parámetros de la animación
    angle = 0
    center_x = 32
    center_y = 0
    radius = 20

    # Bucle de animación
    while timing < 20:
        oled.fill(0)  # Limpia la pantalla en cada cuadro
        x = center_x + int(radius * math.cos(angle))
        y = center_y + int(radius * math.sin(angle))
        draw_cube(x, y)  # Dibuja el cubo en la nueva posición
        oled.show()  # Muestra el cuadro en la pantalla
        time.sleep(0.05)  # Controla la velocidad de la animación
        angle += 0.1  # Aumenta el ángulo para la rotación
        timing += 1
        print(timing)


def draw_menu():
    
    fb = framebuf.FrameBuffer(icon_arrow, 32, 32, framebuf.MONO_HLSB)
    
    oled.fill(0)
    oled.text("Menu:", 0, 0)
    
    for i, option in enumerate(menu_options):
        
        if i == selected_option:
            oled.text(" > " + option, 0, 16 + i * 10)
            
        else:
            oled.text("   " + option, 0, 16 + i * 10)
            
    oled.show()

def execute_option(option):
    b = led.value()
    if option == 0:
        oled.fill(0)
        oled.text("Hola Mundo", 0, 0)
        oled.show()
        time.sleep(2)
        draw_menu()
    elif option == 1:
        led.value(1)
        time.sleep(0.01)
        led.value(0)
        draw_menu()
    elif option == 2:
        DrawCube()
        
        draw_menu()
    elif option == 3:
        # Uso de la función para ejecutar un archivo
        nombre_del_archivo = "2.2 Temperatura.py"
        ejecutar_archivo(nombre_del_archivo)
        
        draw_menu()

draw_menu()

while True:
    if not button_a.value():
        selected_option = (selected_option - 1) % len(menu_options)
        draw_menu()
        time.sleep(0.2)

    if not button_c.value():
        selected_option = (selected_option + 1) % len(menu_options)
        draw_menu()
        time.sleep(0.2)

    if not button_b.value():
        execute_option(selected_option)
        time.sleep(0.2)
        


