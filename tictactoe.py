"""Tic Tac Fight - Juego de gato y perro con clicker para desempate"""

from turtle import *
from freegames import line
import sys
from turtle import Turtle, Screen
import time
import pygame

# Música
pygame.mixer.init()
pygame.mixer.music.load("clicker_song.mp3")
pygame.mixer.music.play(-1)

screen = Screen()
tracer(False)

# GIFS importados
screen.addshape("gato_enojado.gif")
screen.addshape("gato_principal.gif")
screen.addshape("gato_pelea.gif")
screen.addshape("perro_principal.gif")
screen.addshape("perro_enojado.gif")
screen.addshape("pescado_X.gif")
screen.addshape("fondo.gif")
screen.addshape("3_corazones.gif")
screen.addshape("2_corazones.gif")
screen.addshape("1_corazon.gif")
screen.addshape("perro_final.gif")
screen.addshape("gato_final.gif")
screen.addshape("hueso_perro_O.gif")
# AÑADIR PERRO PELEANDO Y HUESO

# Matriz de control inicial, va cambiando con el juego
matriz = [[0,0,0],[0,0,0],[0,0,0]]

# Crear turtle para el grid (para poder borrarlo y redibujarlo)
grid_turtle = Turtle()
grid_turtle.hideturtle()
grid_turtle.penup()

def grid():
    """Draw tic-tac-toe grid."""
    grid_turtle.clear()
    grid_turtle.pensize(3)
    grid_turtle.color("black")

    # Líneas verticales
    grid_turtle.penup()
    grid_turtle.goto(-67, 200)
    grid_turtle.pendown()
    grid_turtle.goto(-67, -200)

    grid_turtle.penup()
    grid_turtle.goto(67, 200)
    grid_turtle.pendown()
    grid_turtle.goto(67, -200)

    # Líneas horizontales
    grid_turtle.penup()
    grid_turtle.goto(-200, -67)
    grid_turtle.pendown()
    grid_turtle.goto(200, -67)

    grid_turtle.penup()
    grid_turtle.goto(-200, 67)
    grid_turtle.pendown()
    grid_turtle.goto(200, 67)

    grid_turtle.penup()
    screen.bgpic("fondo.gif") # Fondo del tablero

# Listas globales para x y o
turtles_jugadas = []

# Mostrar personajes y vidas en la ventana

#Gato principal a la izquierda
gato = Turtle()
gato.hideturtle()
gato.penup()
gato.shape("gato_principal.gif")
gato.goto(-300, -165)
gato.showturtle()

# Perro principal a la derecha
perro = Turtle()
perro.hideturtle()
perro.penup()
perro.shape("perro_principal.gif")
perro.goto(300, -150)
perro.showturtle()

# Crear turtles de vidas una sola vez
vida_gato = Turtle()
vida_gato.hideturtle()
vida_gato.penup()
vida_gato.goto(-300, -50)
vida_gato.showturtle()
vida_perro = Turtle()
vida_perro.hideturtle()
vida_perro.penup()
vida_perro.goto(290, -50)
vida_perro.showturtle()

# Funciones principales del juego
def mostrar_vidas(): # Mostrar vidas restantes con los gifs
    if vidas_gato == 3: vida_gato.shape("3_corazones.gif")
    elif vidas_gato == 2: vida_gato.shape("2_corazones.gif")
    elif vidas_gato == 1: vida_gato.shape("1_corazon.gif")
    if vidas_perro == 3: vida_perro.shape("3_corazones.gif")
    elif vidas_perro == 2: vida_perro.shape("2_corazones.gif")
    elif vidas_perro == 1: vida_perro.shape("1_corazon.gif")

def drawx(x, y):
    """Draw X player."""
    t_x = Turtle()
    t_x.penup()
    t_x.shape("hueso_perro_O.gif") # Perro con hueso AÑADIIIIIIIIIIIRRRRRRRR
    t_x.goto(x+67, y+67) 
    t_x.showturtle()
    turtles_jugadas.append(t_x)

def drawo(x, y):
    """Draw O player."""
    t_o = Turtle()
    t_o.penup()
    t_o.shape("pescado_X.gif") # Gato con pescado
    t_o.goto(x+67, y+90)
    t_o.showturtle() 
    turtles_jugadas.append(t_o)


def reiniciar_tablero():
    global matriz, turtles_jugadas

    matriz = [[0,0,0],[0,0,0],[0,0,0]] # Reiniciar la matriz

    # Borrar todos los turtles de x y o
    for t_xo in turtles_jugadas:
        t_xo.hideturtle()
        t_xo.clear()
    turtles_jugadas.clear()

    # Redibujar la cuadrícula
    grid()
    update()

def floor(value):
    """Round value down to grid with square size 133."""
    return ((value + 200) // 133) * 133 - 200

# Revisar si ha ganado alguien
def revisar():
    # Revisar filas
    for row in matriz:
        if row[0] != 0 and row[0] == row[1] == row[2]:
            return row[0]
    # Revisar Columnas
    for column in range(3):
        if matriz[0][column] != 0 and matriz[0][column] == matriz[1][column] == matriz[2][column]:
            return matriz[0][column]
    # Revisar diagonal de izquierda a derecha
    if matriz[0][0] != 0 and matriz[0][0] == matriz[1][1] == matriz[2][2]:
        return matriz[0][0]
    # Revisar diagonal de derecha a izquierda
    if matriz[0][2] != 0 and matriz[0][2] == matriz[1][1] == matriz[2][0]:
        return matriz[0][2]
    # Si no ha ganado nadie
    return 0

# Revisar si han empatado
def empate(): 
    for row in range(3):
        for column in range(3):
            if matriz[row][column] == 0:
                return False
    return True

# Estados actuales de ambos jugadores
state = {'player': 0}
players = [drawx, drawo]

# Vidas iniciales
vidas_gato = 3
vidas_perro = 3

def tap(x, y):
    """Draw X or O in tapped square."""

    # Variables globales previamente declaradas
    global vidas_gato, vidas_perro

    # Definimos los límites del tablero, si está fuera, no se dibuja nada
    if x < -200 or x > 200 or y < -200 or y > 200:
        return

    x = floor(x)
    y = floor(y)

    col = int((x + 200) // 133)
    row = int((y + 200) // 133)

    # Revisar si la casilla está ocupada
    if matriz[row][col] != 0:
        return

    # Revisar estado actual de jugadores
    player = state['player']
    draw = players[player]

    # Dibujar en pantalla los movimientos
    draw(x, y)
    update()
    state['player'] = not player

    # Identificamos 0 como vacío, 1 movimiento correspondiente de gatos y 2 de perros
    matriz[row][col] = 1 if player == 0 else 2

    # Revisar si alguien ha ganado
    resultado = revisar()
    if resultado != 0:
        if resultado == 1: # Si gana gato, perro pierde vida
            vidas_gato -= 1
        elif resultado == 2: # Si gana perro, gato pierde vida
            vidas_perro -= 1

        mostrar_vidas() # Actualizar vidas en pantalla

        if vidas_gato == 0 or vidas_perro == 0: # Si alguien se queda sin vidas, termina el juego
            # Limpiar tablero y dejar en blanco
            screen.bgpic("") # Quitar fondo
            grid_turtle.clear() # Borrar líneas del grid
            for t_xo in turtles_jugadas:
                t_xo.hideturtle() # Ocultar todas las X y O
            gato.hideturtle() # Ocultar gato principal
            perro.hideturtle() # Ocultar perro principal
            vida_gato.hideturtle() # Ocultar vidas
            vida_perro.hideturtle()
            screen.update()

            # Contador para terminar el juego y cerrarlo
            pre_countdown = 5
            pre_timer = Turtle()
            pre_timer.hideturtle()
            pre_timer.penup()
            pre_timer.goto(0, 100)
            for i in range(pre_countdown, 0, -1): # Cuenta regresiva
                pre_timer.clear()
                if(vidas_perro < vidas_gato):
                    pre_timer.write(f"¡Los gatos ganan!", align="center", font=("Arial", 20, "bold"))
                    gato.penup()
                    gato.shape("gato_final.gif")
                    gato.goto(0, -100)
                    gato.showturtle()
                else:
                    pre_timer.write(f"¡Los perros ganan!", align="center", font=("Arial", 20, "bold"))
                    perro.penup()
                    perro.shape("perro_final.gif")
                    perro.goto(0, -100)
                    perro.showturtle()
                screen.update()
                time.sleep(1)
                pre_timer.clear() # Limpiar mensaje
            sys.exit()    
        else:
            reiniciar_tablero() # Reiniciar el tablero para una nueva ronda


    # Revisar empate
    if empate():
        resultado_clicker = clicker_round()
        if resultado_clicker == 1: 
            vidas_gato -= 1
        elif resultado_clicker == 2:
            vidas_perro -= 1

        mostrar_vidas()

        if vidas_gato == 0 or vidas_perro == 0: # Si alguien se queda sin vidas, termina el juego
            screen.bgpic("") # Quitar fondo
            grid_turtle.clear() # Borrar líneas del grid
            for t_xo in turtles_jugadas:
                t_xo.hideturtle() # Ocultar todas las X y O
            gato.hideturtle() # Ocultar gato principal
            perro.hideturtle() # Ocultar perro principal
            vida_gato.hideturtle() # Ocultar vidas
            vida_perro.hideturtle()
            screen.update()

            # Contador para terminar juego y cerrar
            pre_countdown = 5
            pre_timer = Turtle()
            pre_timer.hideturtle()
            pre_timer.penup()
            pre_timer.goto(0, 100)
            for i in range(pre_countdown, 0, -1): # Cuenta regresiva
                pre_timer.clear()
                if(vidas_perro < vidas_gato):
                    pre_timer.write(f"¡Los gatos ganan!", align="center", font=("Arial", 20, "bold"))
                    gato.penup()
                    gato.shape("gato_final.gif")
                    gato.goto(0, -100)
                    gato.showturtle()
                else:
                    pre_timer.write(f"¡Los perros ganan!", align="center", font=("Arial", 20, "bold"))
                    perro.penup()
                    perro.shape("perro_final.gif")
                    perro.goto(0, -100)
                    perro.showturtle()
                screen.update()
                time.sleep(1)
                pre_timer.clear() # Limpiar mensaje
            sys.exit()    
        else:
            reiniciar_tablero() # Reiniciar el tablero para una nueva ronda


# Iniciar ronda de clicks para desempatar
def clicker_round():
    clicks = {'gato': 0, 'perro': 0}
    start_time = time.time()
    duration = 9  # Segundos aproximados

    # Limpiar tablero y dejar en blanco
    screen.bgpic("")  # Quitar fondo
    grid_turtle.clear() # Borrar líneas del grid
    for t_xo in turtles_jugadas:
        t_xo.hideturtle() # Ocultar todas las X y O
    gato.hideturtle() # Ocultar gato principal
    perro.hideturtle() # Ocultar perro principal
    vida_gato.hideturtle() # Ocultar vidas
    vida_perro.hideturtle()
    screen.update()

    # Countdown antes de iniciar
    pre_countdown = 3
    pre_timer = Turtle()
    pre_timer.hideturtle()
    pre_timer.penup()
    pre_timer.goto(0, 100)
    for i in range(pre_countdown, 0, -1): # Cuenta regresiva
        pre_timer.clear()
        pre_timer.write(f"¡Prepárense! {i}", align="center", font=("Arial", 20, "bold"))
        screen.update()
        time.sleep(1)
    pre_timer.clear() # Limpiar mensaje

    # Mostrar vidas de nuevo
    mostrar_vidas()
    vida_gato.showturtle()
    vida_perro.showturtle()
    screen.update()

    # Mostrar los personajes del clicker
    gato_clicker = Turtle()
    gato_clicker.hideturtle()
    gato_clicker.penup()
    gato_clicker.shape("gato_pelea.gif")
    gato_clicker.goto(-300, -165)
    gato_clicker.showturtle()

    perro_clicker = Turtle()
    perro_clicker.hideturtle()
    perro_clicker.penup()
    perro_clicker.shape("perro_enojado.gif")
    perro_clicker.goto(300, -150)
    perro_clicker.showturtle()

    # Mostrar mensaje de instrucciones
    mensaje = Turtle()
    mensaje.hideturtle()
    mensaje.penup()
    mensaje.goto(0, 200)
    mensaje.write("¡Clicker! Presiona 'A' (Gato) o 'L' (Perro) 5 segundos", align="center", font=("Arial", 16, "bold"))

    # Mostrar contador
    contador = Turtle()
    contador.hideturtle()
    contador.penup()
    contador.goto(0,100)

    # Configurar teclas para contar clicks
    def click_gato(): clicks['gato'] += 1
    def click_perro(): clicks['perro'] += 1
    screen.listen()
    screen.onkey(click_gato, "a")
    screen.onkey(click_perro, "l")

    while True: # Loop hasta que se acabe el tiempo
        elapsed = time.time() - start_time
        remaining = int(duration - elapsed)
        contador.clear()
        contador.write(f"Tiempo: {remaining}s   Gato: {clicks['gato']}   Perro: {clicks['perro']}", align="center", font=("Arial", 16, "bold"))
        screen.update()

        if elapsed >= duration: # Tiempo terminado
            break

    # Limpiar todo lo del clicker
    mensaje.clear()
    contador.clear()
    gato_clicker.hideturtle()
    perro_clicker.hideturtle()
    screen.onkey(None, "a")
    screen.onkey(None, "l")

    # Reiniciar el tablero
    screen.bgpic("fondo.gif") # Restaurar fondo
    grid() # Redibujar grid
    gato.showturtle() # Mostrar gato principal
    perro.showturtle() # Mostrar perro principal
    grid() # redibujar grid
    gato.showturtle()        # mostrar gato principal
    perro.showturtle()       # mostrar perro principal

    for t_xo in turtles_jugadas:
        t_xo.showturtle()
    mostrar_vidas() # Mostrar vidas actualizadas
    vida_gato.showturtle()
    vida_perro.showturtle()
    update()

    # Determinar ganador
    if clicks['gato'] > clicks['perro']:
        return 2  # Si gana gato, perro pierde vida
    elif clicks['perro'] > clicks['gato']:
        return 1  # Si gana perro, gato pierde vida
    else:
        return 0  # Si hay un empate de clicks nadie pierde vida
    

# Configuración de la ventana
setup(775, 550, 370, 0)
hideturtle() # Ocultar cursor
grid()
mostrar_vidas()
vida_gato.showturtle()
vida_perro.showturtle()
update()
onscreenclick(tap)
done()