"""
Gato vs Perro - Tic Tac Toe (Clicker + MP3 + GIF animado del gato) — FIX

ARREGLOS CLAVE:
- Ahora se puede hacer click en el tablero: se usa Screen.onscreenclick(...) (antes estaba mal con .onclick).
- Redibujo con screen.tracer(0) + screen.update() para que siempre se vean las marcas (X/O).
- Desactivo/activo el click del tablero al entrar/salir del clicker.
- Timer visible de 30 s y barra de progreso en el clicker.
- Música (MP3) del clicker y audio de fin (MP3).

REQUISITOS DE ARCHIVOS (misma carpeta del script / notebook):
- gato_enojado.gif
- Pokémon Battle Music - Anime Version.mp3
- Super Smash Bros Ultimate Final KO Sound Effect.mp3
- pescado_X.gif

NOTA: Instala pygame si aún no lo tienes:
%pip install pygame
"""

# ===================== CONFIG (RUTAS DE ARCHIVOS) =====================

# GIF animado del gato (tablero y clicker)
GATO_GIF_BOARD   = "gato_enojado.gif"   # GIF animado en el tablero (costado)
GATO_GIF_CLICKER = "gato_enojado.gif"   # GIF animado en el clicker

# GIF del pescado (X del gato)
GATO_GIF_FISH = "pescado_X.gif"        # GIF del pescado (tablero)

# Audio MP3
CLICKER_MP3 = "Pokémon Battle Music - Anime Version.mp3"               # música (loop) del clicker (30 s)
WIN_MP3     = "Super Smash Bros Ultimate Final KO Sound Effect.mp3"    # audio corto al finalizar

# Duración del clicker (milisegundos)
CLICK_TIME_MS = 30_000  # 30 segundos

# Velocidad de animación del GIF (ms por frame)
GIF_DELAY_MS = 80

# =====================================================================

import sys
import time
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from turtle import Turtle, Screen
import turtle

# --------- AUDIO con pygame.mixer (MP3) ----------
_PYGAME_OK = False
try:
    import pygame
    from pygame import mixer
    pygame.init()
    mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    _PYGAME_OK = True
except Exception as e:
    print("[AVISO] Sonido deshabilitado (pygame.mixer no disponible o no inició):", e)

def music_play_loop(mp3_path: str):
    """Reproduce un MP3 en loop (canal de música)."""
    if _PYGAME_OK and mp3_path and Path(mp3_path).exists():
        try:
            mixer.music.load(mp3_path)
            mixer.music.play(-1)  # loop
        except Exception as e:
            print("[Audio] No se pudo reproducir (loop):", e)

def music_stop():
    """Detiene el canal de música."""
    if _PYGAME_OK:
        try:
            mixer.music.stop()
        except Exception as e:
            print("[Audio] No se pudo detener:", e)

def music_play_once(mp3_path: str):
    """Reproduce un MP3 una vez (sin loop) en el canal de música."""
    if _PYGAME_OK and mp3_path and Path(mp3_path).exists():
        try:
            mixer.music.load(mp3_path)
            mixer.music.play(0)
        except Exception as e:
            print("[Audio] No se pudo reproducir (una vez):", e)

# --------- HACK para reabrir Turtle en Jupyter ----------
def get_screen():
    try:
        s = Screen()
    except tk.TclError:
        turtle.TurtleScreen._RUNNING = True
        s = Screen()
    return s

# --------- Dibujo base con Turtle ----------
def t_line(t: Turtle, x1, y1, x2, y2, width=6):
    t.width(width)
    t.penup(); t.goto(x1, y1); t.pendown(); t.goto(x2, y2); t.penup()

def draw_grid(screen):
    pen = Turtle(visible=False)
    pen.hideturtle(); pen.speed(0); pen.color("#222")
    # verticales
    t_line(pen, -67, 200, -67, -200, width=8)
    t_line(pen,  67, 200,  67, -200, width=8)
    # horizontales
    t_line(pen, -200, -67, 200, -67, width=8)
    t_line(pen, -200,  67, 200,  67, width=8)
    screen.update()

def floor_to_cell(value):
    return ((value + 200) // 133) * 133 - 200

# --------- GIF animado (carga y animación) ----------
def load_gif_frames(path: str):
    """Devuelve lista de frames (tk.PhotoImage) de un GIF animado."""
    frames = []
    idx = 0
    while True:
        try:
            frame = tk.PhotoImage(file=path, format=f"gif -index {idx}")
        except Exception:
            break
        frames.append(frame)
        idx += 1
    return frames

def start_gif_animation(label_widget, frames, delay_ms=80, state_flag_name="_anim_run"):
    """Anima 'frames' en 'label_widget' mientras el flag esté True."""
    if not frames:
        return
    setattr(label_widget, state_flag_name, True)
    setattr(label_widget, "_anim_frames", frames)
    setattr(label_widget, "_anim_index", 0)

    def _tick():
        if not getattr(label_widget, state_flag_name, False):
            return
        i = getattr(label_widget, "_anim_index", 0)
        label_widget.configure(image=frames[i])
        i = (i + 1) % len(frames)
        setattr(label_widget, "_anim_index", i)
        label_widget.after(delay_ms, _tick)

    _tick()

def stop_gif_animation(label_widget, state_flag_name="_anim_run"):
    """Detiene la animación del label."""
    setattr(label_widget, state_flag_name, False)

# --------- Helpers UI ----------
def hide_widget(w):
    for fn in ("pack_forget", "grid_forget", "place_forget"):
        try:
            getattr(w, fn)()
        except Exception:
            pass

# --------- Pantalla / Estilos ----------
screen = get_screen()
screen.setup(900, 700)  # más ancho para sidebars
screen.title("Gato vs Perro - Tic Tac Toe")
screen.tracer(0)        # dibujamos manualmente y actualizamos con screen.update()

root = screen._root
root.minsize(900, 700)

style = ttk.Style(root)
try: style.theme_use('clam')
except: pass
style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
style.configure("Sub.TLabel", font=("Segoe UI", 14))
style.configure("Label.TLabel", font=("Segoe UI", 12))
style.configure("Entry.TEntry", padding=6)
style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=8)
style.configure("Ghost.TButton", font=("Segoe UI", 11), padding=6)

# --------- UI: Menú (simple para iniciar) ----------
menu_frame = ttk.Frame(root, padding=20)
ttk.Label(menu_frame, text="Gato vs Perro", style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0,12))
ttk.Label(menu_frame, text="Nombre del Gato (Q):", style="Label.TLabel").grid(row=1, column=0, sticky="e", pady=6, padx=(0,8))
entry_gato = ttk.Entry(menu_frame, width=28, style="Entry.TEntry"); entry_gato.grid(row=1, column=1, sticky="w", pady=6)
ttk.Label(menu_frame, text="Nombre del Perro (P):", style="Label.TLabel").grid(row=2, column=0, sticky="e", pady=6, padx=(0,8))
entry_perro = ttk.Entry(menu_frame, width=28, style="Entry.TEntry"); entry_perro.grid(row=2, column=1, sticky="w", pady=6)
menu_buttons = ttk.Frame(menu_frame); menu_buttons.grid(row=3, column=0, columnspan=2, pady=16)
btn_start = ttk.Button(menu_buttons, text="Iniciar partida", style="Primary.TButton")
btn_exit  = ttk.Button(menu_buttons, text="Salir", style="Ghost.TButton")
btn_start.pack(side="left", padx=8); btn_exit.pack(side="left", padx=8)

# --------- Top bar del tablero ----------
topbar_frame = ttk.Frame(root, padding=(10,5))
turno_var = tk.StringVar(value="Turno: -")
ttk.Label(topbar_frame, textvariable=turno_var, style="Sub.TLabel").pack(side="left", padx=6)

# --------- Sidebars del tablero ----------
left_sidebar  = ttk.Frame(root, padding=10)   # Gato (GIF)
right_sidebar = ttk.Frame(root, padding=10)   # Perro (placeholder)

# Label del GIF del gato en el tablero (izquierda)
gato_board_image_lbl = ttk.Label(left_sidebar)
gato_board_image_lbl.pack(pady=10)
# Placeholder del perro (derecha)
ttk.Label(right_sidebar, text="Aquí irá la imagen del Perro", style="Label.TLabel").pack(pady=10)

# --------- Vista Clicker ----------
clicker_frame = ttk.Frame(root, padding=20)
ttk.Label(clicker_frame, text="Clicker de desempate", style="Title.TLabel").pack(pady=(0,8))

# Cuenta 3-2-1-¡YA!
countdown_var = tk.StringVar(value="")
ttk.Label(clicker_frame, textvariable=countdown_var, style="Title.TLabel").pack(pady=(0,12))

# Contador visible 00:30 y barra de progreso
timer_var = tk.StringVar(value="00:30")
timer_label = ttk.Label(clicker_frame, textvariable=timer_var, style="Sub.TLabel")
timer_label.pack(pady=(0,8))

timer_bar = ttk.Progressbar(clicker_frame, orient="horizontal", length=360,
                            mode="determinate", maximum=CLICK_TIME_MS)
timer_bar.pack(pady=(0,12))

players_panel = ttk.Frame(clicker_frame); players_panel.pack(pady=8, fill="x")

# Panel Gato (con GIF)
gato_panel = ttk.Frame(players_panel, padding=10); gato_panel.pack(side="left", expand=True, fill="both", padx=8)
ttk.Label(gato_panel, text="Gato (Q)", style="Sub.TLabel").pack(pady=(0,8))
gato_counter_var = tk.StringVar(value="0")
ttk.Label(gato_panel, textvariable=gato_counter_var, style="Title.TLabel").pack()
gato_clicker_image_lbl = ttk.Label(gato_panel)  # aquí va el GIF del gato en el clicker
gato_clicker_image_lbl.pack(pady=10)

# Panel Perro (sin imagen por ahora)
perro_panel = ttk.Frame(players_panel, padding=10); perro_panel.pack(side="left", expand=True, fill="both", padx=8)
ttk.Label(perro_panel, text="Perro (P)", style="Sub.TLabel").pack(pady=(0,8))
perro_counter_var = tk.StringVar(value="0")
ttk.Label(perro_panel, textvariable=perro_counter_var, style="Title.TLabel").pack()
ttk.Label(perro_panel, text="Aquí irá la imagen del Perro", style="Label.TLabel").pack(pady=10)

clicker_info = ttk.Label(clicker_frame, text="Pulsa tu tecla lo más rápido que puedas cuando diga ¡YA!\nGato = Q   |   Perro = P", style="Label.TLabel")
clicker_info.pack(pady=6)
clicker_buttons = ttk.Frame(clicker_frame); clicker_buttons.pack(pady=12)
btn_volver = ttk.Button(clicker_buttons, text="Volver al tablero", style="Primary.TButton"); btn_volver.pack()

# --------- Estado del juego ----------
matriz = [[0,0,0],[0,0,0],[0,0,0]]   # 0 libre, 1 Gato, 2 Perro
state = {'player': 0}                 # 0 Gato, 1 Perro
players_names = ["Gato", "Perro"]
marks_turtles = []

screen.register_shape(GATO_GIF_FISH) # registrar la forma del pescado

def draw_GATO_at(x, y):
    t = Turtle(visible=False)
    t.penup()
    t.shape(GATO_GIF_FISH)
    t.goto(x+60, y+95)
    t.showturtle()
    marks_turtles.append(t)

def draw_PERRO_at(x, y):
    t = Turtle(visible=False)
    t.hideturtle(); t.speed(0); t.color("#1d6fb8"); t.width(7)
    t.penup(); t.goto(x+66, y+20); t.pendown(); t.circle(46); t.penup()
    marks_turtles.append(t)

def draw_mark_for(player, x, y):
    (draw_GATO_at if player == 0 else draw_PERRO_at)(x, y)
    screen.update()  # <-- asegura que se vea el trazo con tracer(0)

def revisar_ganador():
    # filas
    for row in matriz:
        if row[0] and row[0] == row[1] == row[2]: return row[0]
    # columnas
    for c in range(3):
        if matriz[0][c] and matriz[0][c] == matriz[1][c] == matriz[2][c]: return matriz[0][c]
    # diagonales
    if matriz[0][0] and matriz[0][0] == matriz[1][1] == matriz[2][2]: return matriz[0][0]
    if matriz[0][2] and matriz[0][2] == matriz[1][1] == matriz[2][0]: return matriz[0][2]
    return 0

def hay_empate():
    return all(matriz[r][c] != 0 for r in range(3) for c in range(3))

# --------- Cargar frames de GIF (tablero y clicker) ----------
gato_board_frames   = load_gif_frames(GATO_GIF_BOARD)
gato_clicker_frames = load_gif_frames(GATO_GIF_CLICKER)

# --------- Timer del clicker (actualiza label y barra) ----------
_timer_active = False
_timer_t0 = 0.0

def start_click_timer():
    """Inicia el temporizador visible de 30 s."""
    global _timer_active, _timer_t0
    _timer_active = True
    _timer_t0 = time.monotonic()
    timer_var.set("00:30")
    timer_bar['value'] = 0
    _tick_timer()

def _tick_timer():
    if not _timer_active:
        return
    elapsed_ms = int((time.monotonic() - _timer_t0) * 1000)
    remaining = max(0, CLICK_TIME_MS - elapsed_ms)

    secs = remaining // 1000
    timer_var.set(f"00:{secs:02d}")
    timer_bar['value'] = CLICK_TIME_MS - remaining

    if remaining <= 0:
        return
    root.after(100, _tick_timer)

def stop_click_timer():
    """Detiene el temporizador (por seguridad)."""
    global _timer_active
    _timer_active = False

# --------- Arranque en menú ----------
menu_frame.place(relx=0.5, rely=0.5, anchor="center")

def actualizar_turno_label():
    jugador = state['player']
    turno_var.set(f"Turno: {players_names[jugador]} ({'Gato' if jugador==0 else 'Perro'})")

def limpiar_tablero():
    for t in marks_turtles:
        try: t.hideturtle(); t.clear()
        except: pass
    marks_turtles.clear()
    for r in range(3):
        for c in range(3):
            matriz[r][c] = 0
    screen.clear()
    screen.tracer(0)
    draw_grid(screen)
    screen.update()

def soft_exit():
    music_stop()
    # Detener animaciones
    try: stop_gif_animation(gato_board_image_lbl)
    except: pass
    try: stop_gif_animation(gato_clicker_image_lbl)
    except: pass
    # Apagar UI
    try:
        screen.onscreenclick(None)  # <-- desactiva clicks del tablero
        screen.onkeypress(None); screen.onkeyrelease(None)
    except: pass
    for fr in (menu_frame, topbar_frame, left_sidebar, right_sidebar, clicker_frame):
        hide_widget(fr)
    try: screen.clearscreen()
    except: pass
    try: screen.title("Gato vs Perro (cerrado suavemente)")
    except: pass

btn_exit.configure(command=soft_exit)

# --------- LÓGICA DEL TABLERO (CLICK EN CASILLA) ----------
def on_tap(x, y):
    # límites del tablero 3x3
    if x < -200 or x > 200 or y < -200 or y > 200:
        return

    xx = floor_to_cell(x); yy = floor_to_cell(y)
    # índices de celda seguros
    col = max(0, min(2, int((xx + 200) // 133)))
    row = max(0, min(2, int((yy + 200) // 133)))

    if matriz[row][col] != 0:
        prev = root.title(); root.title("Casilla ocupada"); root.after(700, lambda: root.title(prev))
        return

    jugador = state['player']
    draw_mark_for(jugador, xx, yy)
    matriz[row][col] = 1 if jugador == 0 else 2

    g = revisar_ganador()
    if g != 0:
        screen.onscreenclick(None)  # <-- desactiva clicks del tablero
        anunciar_ganador_tablero(g)
        return

    if hay_empate():
        screen.onscreenclick(None)  # <-- desactiva clicks del tablero
        lanzar_clicker_empate()
        return

    state['player'] = 1 - jugador
    actualizar_turno_label()
    screen.update()

def anunciar_ganador_tablero(g):
    nombre = players_names[0] if g==1 else players_names[1]
    dlg = tk.Toplevel(root); dlg.title("Resultado"); dlg.geometry("+220+220")
    ttk.Label(dlg, text=f"¡Ganó {nombre}!", style="Title.TLabel").pack(padx=20, pady=(20,10))
    f = ttk.Frame(dlg); f.pack(pady=8)
    def jugar_de_nuevo():
        dlg.destroy()
        state['player'] = 0
        limpiar_tablero()
        actualizar_turno_label()
        screen.onscreenclick(on_tap, 1)   # <-- activa clicks del tablero
        screen.update()
    ttk.Button(f, text="Jugar de nuevo", style="Primary.TButton", command=jugar_de_nuevo).pack(side="left", padx=6)
    ttk.Button(f, text="Salir", style="Ghost.TButton", command=lambda:(dlg.destroy(), soft_exit())).pack(side="left", padx=6)
    dlg.transient(root); dlg.grab_set(); root.wait_window(dlg)

# --------- CLICKER ----------
clicker_active = False
gato_clicks = 0
perro_clicks = 0

def lanzar_clicker_empate():
    # Apagar animación del gato en el tablero y ocultar sidebars
    try: stop_gif_animation(gato_board_image_lbl)
    except: pass
    hide_widget(left_sidebar); hide_widget(right_sidebar)

    # Música del clicker: empieza al entrar (incluye countdown)
    music_stop()
    music_play_loop(CLICKER_MP3)

    hide_widget(menu_frame)
    hide_widget(topbar_frame)

    global gato_clicks, perro_clicks, clicker_active
    gato_clicks = 0; perro_clicks = 0; clicker_active = False
    gato_counter_var.set("0"); perro_counter_var.set("0")
    countdown_var.set("")
    timer_var.set("00:30"); timer_bar['value'] = 0

    clicker_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Iniciar animación del GIF del gato (clicker)
    if gato_clicker_frames:
        start_gif_animation(gato_clicker_image_lbl, gato_clicker_frames, delay_ms=GIF_DELAY_MS)

    # 3-2-1-¡YA! (1 segundo por paso)
    secuencia_countdown([3,2,1,"¡YA!"], inicio_clicks, intervalo_ms=1000)

def secuencia_countdown(items, al_final, intervalo_ms=800):
    def paso(idx=0):
        if idx < len(items):
            countdown_var.set(str(items[idx]))
            root.after(intervalo_ms, lambda: paso(idx+1))
        else:
            al_final()
    paso(0)

def inicio_clicks():
    global clicker_active, gato_clicks, perro_clicks
    clicker_active = True
    countdown_var.set("¡YA!")
    gato_clicks = 0; perro_clicks = 0
    gato_counter_var.set("0"); perro_counter_var.set("0")

    # Iniciar temporizador visible de 30 s
    start_click_timer()

    root.bind("<KeyPress-q>", on_q); root.bind("<KeyPress-Q>", on_q)
    root.bind("<KeyPress-p>", on_p); root.bind("<KeyPress-P>", on_p)
    # Al finalizar los 30 s se corta la música y pasamos a resultado
    root.after(CLICK_TIME_MS, fin_clicks)

def on_q(event=None):
    global gato_clicks
    if clicker_active:
        gato_clicks += 1
        gato_counter_var.set(str(gato_clicks))

def on_p(event=None):
    global perro_clicks
    if clicker_active:
        perro_clicks += 1
        perro_counter_var.set(str(perro_clicks))

def fin_clicks():
    global clicker_active
    clicker_active = False

    # Detener temporizador
    stop_click_timer()

    try:
        root.unbind("<KeyPress-q>"); root.unbind("<KeyPress-Q>")
        root.unbind("<KeyPress-p>"); root.unbind("<KeyPress-P>")
    except: pass

    # Detener la música del clicker (exacto al terminar)
    music_stop()
    # Sonido de fin/victoria (MP3) una sola vez
    music_play_once(WIN_MP3)

    # Detener animación del GIF del gato (clicker)
    try: stop_gif_animation(gato_clicker_image_lbl)
    except: pass

    # Determinar ganador del clicker
    if gato_clicks > perro_clicks:
        resultado = f"¡{players_names[0]} (Gato) gana el desempate!"
    elif perro_clicks > gato_clicks:
        resultado = f"¡{players_names[1]} (Perro) gana el desempate!"
    else:
        resultado = "¡Empate en el clicker! (Puedes intentarlo de nuevo)"

    dlg = tk.Toplevel(root); dlg.title("Resultado del clicker"); dlg.geometry("+220+220")
    ttk.Label(dlg, text=resultado, style="Title.TLabel").pack(padx=20, pady=(20,10))
    f = ttk.Frame(dlg); f.pack(pady=8)

    def volver_tablero():
        dlg.destroy()
        regresar_a_tablero()

    def repetir_clicker():
        dlg.destroy()
        lanzar_clicker_empate()

    ttk.Button(f, text="Volver al tablero", style="Primary.TButton", command=volver_tablero).pack(side="left", padx=6)
    ttk.Button(f, text="Repetir clicker", style="Ghost.TButton", command=repetir_clicker).pack(side="left", padx=6)
    dlg.transient(root); dlg.grab_set(); root.wait_window(dlg)

def regresar_a_tablero():
    hide_widget(clicker_frame)
    # Volver a mostrar sidebars del tablero y animar el gato
    left_sidebar.pack(side="left", fill="y")
    right_sidebar.pack(side="right", fill="y")
    if gato_board_frames:
        start_gif_animation(gato_board_image_lbl, gato_board_frames, delay_ms=GIF_DELAY_MS)

    state['player'] = 0
    limpiar_tablero()
    actualizar_turno_label()
    topbar_frame.pack(side="top", fill="x")
    screen.onscreenclick(on_tap, 1)  # <-- activa clicks del tablero
    screen.listen()
    screen.update()

btn_volver.configure(command=regresar_a_tablero)

# --------- Arranque / Menú ----------
def empezar_juego():
    n_gato = entry_gato.get().strip() or "Gato"
    n_perro = entry_perro.get().strip() or "Perro"
    players_names[0] = n_gato
    players_names[1] = n_perro

    hide_widget(menu_frame)
    topbar_frame.pack(side="top", fill="x")

    # Mostrar sidebars del tablero y animar GIF del gato
    left_sidebar.pack(side="left", fill="y")
    right_sidebar.pack(side="right", fill="y")
    if gato_board_frames:
        start_gif_animation(gato_board_image_lbl, gato_board_frames, delay_ms=GIF_DELAY_MS)

    limpiar_tablero()
    actualizar_turno_label()
    screen.onscreenclick(on_tap, 1)  # <-- activa clicks del tablero
    screen.listen()
    screen.update()

btn_start.configure(command=empezar_juego)

# --------- Loop principal ----------
screen.mainloop()
