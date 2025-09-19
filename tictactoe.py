"""Tic Tac Fight - Juego de gato y perro con clicker para desempate"""

from turtle import *
from freegames import line
import sys # cuando eliminemos lo que que si ganan se cierra lo quito!!!
from turtle import Turtle, Screen
import time
import pygame # solo para la música

pygame.mixer.init() #música :D
pygame.mixer.music.load("clicker_song.mp3")
pygame.mixer.music.play(-1)

screen = Screen()
tracer(False)

# GIFS
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

#Matriz de control, va cambiando con el juego!!!
matriz = [[0,0,0],[0,0,0],[0,0,0]]

#Crear turtle para el grid (para poder borrarlo y redibujarlo)
grid_turtle = Turtle()
grid_turtle.hideturtle()
grid_turtle.penup()

def grid():
    """Draw tic-tac-toe grid."""
    #line(-67, 200, -67, -200) line(67, 200, 67, -200) line(-200, -67, 200, -67) line(-200, 67, 200, 67)
    grid_turtle.clear()
    grid_turtle.pensize(3)
    grid_turtle.color("black")

    #Verticales
    grid_turtle.penup()
    grid_turtle.goto(-67, 200)
    grid_turtle.pendown()
    grid_turtle.goto(-67, -200)

    grid_turtle.penup()
    grid_turtle.goto(67, 200)
    grid_turtle.pendown()
    grid_turtle.goto(67, -200)

    #Horizontales
    grid_turtle.penup()
    grid_turtle.goto(-200, -67)
    grid_turtle.pendown()
    grid_turtle.goto(200, -67)

    grid_turtle.penup()
    grid_turtle.goto(-200, 67)
    grid_turtle.pendown()
    grid_turtle.goto(200, 67)

    grid_turtle.penup()
    screen.bgpic("fondo.gif") #fondo del tablero

#Listas globales
turtles_jugadas = [] #Para X y O

# --- Mostrar personajes y vidas en la ventana ---

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

# -------------- FUNCIONES DEL JUEGO!!! :0
def mostrar_vidas(): #mostrar vidas restantes con los gifs
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
    t_x.shape("gato_enojado.gif") # Perro con hueso
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

    #Borrar todos los turtles de X/O
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

def revisar(): #revisar si ha ganado alguien!
    #filas
    for row in matriz:
        if row[0] != 0 and row[0] == row[1] == row[2]:
            return row[0]
    #columnas
    for column in range(3):
        if matriz[0][column] != 0 and matriz[0][column] == matriz[1][column] == matriz[2][column]:
            return matriz[0][column]
    #diagonal izq-der
    if matriz[0][0] != 0 and matriz[0][0] == matriz[1][1] == matriz[2][2]:
        return matriz[0][0]
    #diagonal der-izq
    if matriz[0][2] != 0 and matriz[0][2] == matriz[1][1] == matriz[2][0]:
        return matriz[0][2]
    #no ha ganado nadie:
    return 0

def empate():
    for row in range(3):
        for column in range(3):
            if matriz[row][column] == 0:
                return False
    return True


"""
state['player'] guarda quién juega: 0 para X, 1 para O.
players es una lista de funciones; players[0] es drawx, players[1] es drawo.
"""
state = {'player': 0}
players = [drawx, drawo]

# Vidas iniciales
vidas_gato = 3
vidas_perro = 3

def tap(x, y):
    """Draw X or O in tapped square."""
    global vidas_gato, vidas_perro

    # Definimos los límites del tablero
    if x < -200 or x > 200 or y < -200 or y > 200:
        return  # Si está fuera, no se dibuja nada

    x = floor(x)
    y = floor(y)

    col = int((x + 200) // 133)
    row = int((y + 200) // 133)

    # casilla ocupada?
    if matriz[row][col] != 0:
        print("Casilla ocupada")
        return

    # checar jugador actual
    player = state['player']
    draw = players[player]

    #dibujar en pantalla
    draw(x, y)
    update()
    state['player'] = not player

    # x --> 1, o --> 2
    matriz[row][col] = 1 if player == 0 else 2

    # ver si alguien ganó
    resultado = revisar()
    if resultado != 0:
        if resultado == 1: # gana el gato → perro pierde vida
            vidas_gato -= 1
        elif resultado == 2: # gana el perro → gato pierde vida
            vidas_perro -= 1

        mostrar_vidas() # actualizar vidas en pantalla

        if vidas_gato == 0 or vidas_perro == 0: # si alguien se queda sin vidas, termina el juego
            #print("¡Juego terminado!")
            # Limpiar tablero y dejar en blanco
            screen.bgpic("")  # quitar fondo
            grid_turtle.clear() # borrar líneas del grid
            for t_xo in turtles_jugadas:
                t_xo.hideturtle() # ocultar todas las X y O
            gato.hideturtle()        # ocultar gato principal
            perro.hideturtle()       # ocultar perro principal
            vida_gato.hideturtle()  # ocultar vidas
            vida_perro.hideturtle()
            screen.update()

                # Countdown para cerrar
            pre_countdown = 5
            pre_timer = Turtle()
            pre_timer.hideturtle()
            pre_timer.penup()
            pre_timer.goto(0, 100)
            for i in range(pre_countdown, 0, -1): # cuenta regresiva
                pre_timer.clear()
                if(vidas_perro < vidas_gato):
                    pre_timer.write(f"¡Los gatos ganan!", align="center", font=("Arial", 20, "bold"))
                    #gato = Turtle()
                    #gato.hideturtle()
                    gato.penup()
                    gato.shape("gato_principal.gif")
                    gato.goto(0, -100)
                    gato.showturtle()
                else:
                    pre_timer.write(f"¡Los perros ganan!", align="center", font=("Arial", 20, "bold"))
                    # Perro principal a la derecha
                    #perro = Turtle()
                    #perro.hideturtle()
                    perro.penup()
                    perro.shape("perro_principal.gif")
                    perro.goto(0, -100)
                    perro.showturtle()
                screen.update()
                time.sleep(1)
                pre_timer.clear()  # limpiar mensaje
            sys.exit()    
        else:
            reiniciar_tablero() # reiniciar el tablero para una nueva ronda


    # Revisar empate
    if empate():
        resultado_clicker = clicker_round()
        if resultado_clicker == 1: 
            vidas_gato -= 1
        elif resultado_clicker == 2:
            vidas_perro -= 1

        mostrar_vidas()

        if vidas_gato == 0 or vidas_perro == 0:
            screen.bgpic("")  # quitar fondo
            grid_turtle.clear() # borrar líneas del grid
            for t_xo in turtles_jugadas:
                t_xo.hideturtle() # ocultar todas las X y O
            gato.hideturtle()        # ocultar gato principal
            perro.hideturtle()       # ocultar perro principal
            vida_gato.hideturtle()  # ocultar vidas
            vida_perro.hideturtle()
            screen.update()

                # Countdown para cerrar
            pre_countdown = 5
            pre_timer = Turtle()
            pre_timer.hideturtle()
            pre_timer.penup()
            pre_timer.goto(0, 100)
            for i in range(pre_countdown, 0, -1): # cuenta regresiva
                pre_timer.clear()
                if(vidas_perro < vidas_gato):
                    pre_timer.write(f"¡Los gatos ganan!", align="center", font=("Arial", 20, "bold"))
                else:
                    pre_timer.write(f"¡Los perros ganan!", align="center", font=("Arial", 20, "bold"))
                screen.update()
                time.sleep(1)
                pre_timer.clear()  # limpiar mensaje
            sys.exit()
        else:
            reiniciar_tablero()

# --- Ronda de clicker para desempatar ---
def clicker_round():
    clicks = {'gato': 0, 'perro': 0}
    start_time = time.time()
    duration = 9  # segundos mayores porque no es muy exacto

    # Limpiar tablero y dejar en blanco
    screen.bgpic("")  # quitar fondo
    grid_turtle.clear() # borrar líneas del grid
    for t_xo in turtles_jugadas:
        t_xo.hideturtle() # ocultar todas las X y O
    gato.hideturtle()        # ocultar gato principal
    perro.hideturtle()       # ocultar perro principal
    vida_gato.hideturtle()  # ocultar vidas
    vida_perro.hideturtle()
    screen.update()

    # Countdown antes de iniciar
    pre_countdown = 3
    pre_timer = Turtle()
    pre_timer.hideturtle()
    pre_timer.penup()
    pre_timer.goto(0, 100)
    for i in range(pre_countdown, 0, -1): # cuenta regresiva
        pre_timer.clear()
        pre_timer.write(f"¡Prepárense! {i}", align="center", font=("Arial", 20, "bold"))
        screen.update()
        time.sleep(1)
    pre_timer.clear()  # limpiar mensaje

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

    while True: # loop hasta que se acabe el tiempo
        elapsed = time.time() - start_time
        remaining = int(duration - elapsed)
        contador.clear()
        contador.write(f"Tiempo: {remaining}s   Gato: {clicks['gato']}   Perro: {clicks['perro']}", align="center", font=("Arial", 16, "bold"))
        screen.update()

        if elapsed >= duration: # tiempo terminado
            break

    # Limpiar todo lo del clicker
    mensaje.clear()
    contador.clear()
    gato_clicker.hideturtle()
    perro_clicker.hideturtle()
    screen.onkey(None, "a")
    screen.onkey(None, "l")

    # Reiniciar el tablero
    screen.bgpic("fondo.gif") # restaurar fondo
    grid() # redibujar grid
    gato.showturtle()        # mostrar gato principal
    perro.showturtle()       # mostrar perro principal
    for t_xo in turtles_jugadas:
        t_xo.showturtle()
    mostrar_vidas() # mostrar vidas actualizadas
    vida_gato.showturtle()
    vida_perro.showturtle()
    update()

    # Determinar ganador
    if clicks['gato'] > clicks['perro']:
        return 2  # gana el gato → perro pierde vida
    elif clicks['perro'] > clicks['gato']:
        return 1  # gana el perro → gato pierde vida
    else:
        return 0  # empate de clicks → nadie pierde vida
    

# Configuración de la ventana
setup(775, 550, 370, 0) #ancho = 775, alto = 550

hideturtle() #ocultar cursor
grid()
mostrar_vidas()
vida_gato.showturtle()
vida_perro.showturtle()
update()
onscreenclick(tap)
done()