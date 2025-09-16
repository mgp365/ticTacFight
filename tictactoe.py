"""Tic Tac Toe

Exercises

1. Give the X and O a different color and width.
2. What happens when someone taps a taken spot?
3. How would you detect when someone has won?
4. How could you create a computer player?
"""

from turtle import *
from freegames import line
import sys # cuando eliminemos lo que que si ganan se cierra lo quito!!!
from turtle import Turtle, Screen
screen = Screen()
t = Turtle()

screen.addshape("gato_enojado.gif")
t.shape("gato_enojado.gif")

t.penup()
t.goto(-250,0)

# Implementación: Matrices para control de versiones
matriz = [[0,0,0],[0,0,0],[0,0,0]] # matriz inicial (0)


def grid():
    """Draw tic-tac-toe grid."""
    line(-67, 200, -67, -200)
    line(67, 200, 67, -200)
    line(-200, -67, 200, -67)
    line(-200, 67, 200, 67)


def drawx(x, y):
    """Draw X player."""
    line(x, y, x + 133, y + 133)
    line(x, y + 133, x + 133, y)


def drawo(x, y):
    """Draw O player."""
    up()
    goto(x + 67, y + 5)
    down()
    circle(62)


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
    for row in matriz:
        for cell in row:
            if cell == 0:
                return False
    return True


"""
state['player'] guarda quién juega: 0 para X, 1 para O.
players es una lista de funciones; players[0] es drawx, players[1] es drawo.
"""
state = {'player': 0}
players = [drawx, drawo]


def tap(x, y):
    """Draw X or O in tapped square."""

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
    if revisar()!= 0:
        sys.exit()

    if empate() == True:
        sys.exit()


setup(600, 420, 370, 0) #ancho = 600, alto = 420

hideturtle() #ocltar cursor
tracer(False)
grid()
update()
onscreenclick(tap)
done()
