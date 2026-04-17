import pygame
import sys
from tablero import Tablero
from minimax import mejor_movimiento
from piezas import Dama, Torre, Alfil, Caballo

# ------------------------------------------------------------------
# Configuración visual
# ------------------------------------------------------------------

ANCHO = 640
ALTO = 640
TAMANO_CASILLA = ANCHO // 8
PROFUNDIDAD_IA = 3

COLOR_CLARO      = (240, 217, 181)
COLOR_OSCURO     = (181, 136,  99)
COLOR_SELECCION  = (106, 168,  79, 180)
COLOR_MOVIMIENTO = (106, 168,  79, 100)
COLOR_JAQUE      = (220,  50,  50, 180)
FONDO_INFO       = ( 30,  30,  30)
COLOR_TEXTO      = (255, 255, 255)
COLOR_MENU_BG    = ( 40,  40,  40)
COLOR_MENU_HOVER = ( 70,  70,  70)

SIMBOLOS = {
    'P': '♙', 'p': '♟',
    'T': '♖', 't': '♜',
    'C': '♘', 'c': '♞',
    'A': '♗', 'a': '♝',
    'D': '♕', 'd': '♛',
    'R': '♔', 'r': '♚',
}

OPCIONES_CORONACION = [Dama, Torre, Alfil, Caballo]
SIMBOLOS_CORONACION_BLANCO = ['♕', '♖', '♗', '♘']
SIMBOLOS_CORONACION_NEGRO  = ['♛', '♜', '♝', '♞']


# ------------------------------------------------------------------
# Funciones de dibujo
# ------------------------------------------------------------------

def dibujar_tablero(superficie):
    for fila in range(8):
        for col in range(8):
            color = COLOR_CLARO if (fila + col) % 2 == 0 else COLOR_OSCURO
            pygame.draw.rect(superficie, color,
                             (col * TAMANO_CASILLA, fila * TAMANO_CASILLA,
                              TAMANO_CASILLA, TAMANO_CASILLA))


def dibujar_piezas(superficie, tablero, fuente):
    for fila in range(8):
        for col in range(8):
            pieza = tablero.casillas[fila][col]
            if pieza:
                simbolo = SIMBOLOS.get(str(pieza), '?')
                color_pieza = (255, 255, 255) if pieza.color == 'blanco' else (20, 20, 20)
                texto = fuente.render(simbolo, True, color_pieza)
                x = col * TAMANO_CASILLA + (TAMANO_CASILLA - texto.get_width()) // 2
                y = fila * TAMANO_CASILLA + (TAMANO_CASILLA - texto.get_height()) // 2
                superficie.blit(texto, (x, y))


def dibujar_seleccion(superficie, seleccion, movimientos_validos):
    capa = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA), pygame.SRCALPHA)
    if seleccion:
        fila, col = seleccion
        capa.fill(COLOR_SELECCION)
        superficie.blit(capa, (col * TAMANO_CASILLA, fila * TAMANO_CASILLA))
    capa.fill(COLOR_MOVIMIENTO)
    for fila, col in movimientos_validos:
        superficie.blit(capa, (col * TAMANO_CASILLA, fila * TAMANO_CASILLA))


def dibujar_jaque(superficie, tablero):
    pos_rey = tablero.encontrar_rey(tablero.turno)
    if pos_rey and tablero.rey_en_jaque(tablero.turno):
        fila, col = pos_rey
        capa = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA), pygame.SRCALPHA)
        capa.fill(COLOR_JAQUE)
        superficie.blit(capa, (col * TAMANO_CASILLA, fila * TAMANO_CASILLA))


def dibujar_info(superficie_info, turno, estado, fuente_info):
    superficie_info.fill(FONDO_INFO)
    msg = f"Turno: {turno.capitalize()}   {estado}"
    texto = fuente_info.render(msg, True, COLOR_TEXTO)
    superficie_info.blit(texto, (10, 8))


def dibujar_menu_coronacion(pantalla, color_pieza, fuente):
    """Dibuja un menú central con las 4 opciones de coronación."""
    ancho_menu = 4 * TAMANO_CASILLA
    alto_menu = TAMANO_CASILLA + 40
    x_menu = (ANCHO - ancho_menu) // 2
    y_menu = (ALTO - alto_menu) // 2

    # Fondo semitransparente
    overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    pantalla.blit(overlay, (0, 0))

    # Caja del menú
    pygame.draw.rect(pantalla, COLOR_MENU_BG, (x_menu - 10, y_menu - 10, ancho_menu + 20, alto_menu + 20), border_radius=12)

    simbolos = SIMBOLOS_CORONACION_BLANCO if color_pieza == 'blanco' else SIMBOLOS_CORONACION_NEGRO
    mx, my = pygame.mouse.get_pos()
    rects = []

    for i, simbolo in enumerate(simbolos):
        rx = x_menu + i * TAMANO_CASILLA
        ry = y_menu + 20
        rect = pygame.Rect(rx, ry, TAMANO_CASILLA, TAMANO_CASILLA)
        rects.append(rect)

        hover = rect.collidepoint(mx, my)
        pygame.draw.rect(pantalla, COLOR_MENU_HOVER if hover else COLOR_MENU_BG, rect, border_radius=8)

        texto = fuente.render(simbolo, True, (255, 255, 255) if color_pieza == 'blanco' else (20, 20, 20))
        pantalla.blit(texto, (rx + (TAMANO_CASILLA - texto.get_width()) // 2,
                               ry + (TAMANO_CASILLA - texto.get_height()) // 2))

    fuente_label = pygame.font.SysFont('arial', 16)
    label = fuente_label.render('Elige la pieza', True, (200, 200, 200))
    pantalla.blit(label, (x_menu + (ancho_menu - label.get_width()) // 2, y_menu - 2))

    return rects


# ------------------------------------------------------------------
# Conversión coordenadas ratón -> casilla
# ------------------------------------------------------------------

def pixel_a_casilla(x, y):
    return y // TAMANO_CASILLA, x // TAMANO_CASILLA


# ------------------------------------------------------------------
# Bucle principal
# ------------------------------------------------------------------

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO + 40))
    pygame.display.set_caption('Ajedrez — Humano vs IA')

    fuente = pygame.font.SysFont('segoeuisymbol', 60)
    fuente_info = pygame.font.SysFont('arial', 18)

    tablero = Tablero()
    seleccion = None
    movimientos_validos = []
    estado = ''
    color_humano = 'blanco'
    esperando_coronacion = None  # (fila, col) del peón coronado pendiente

    reloj = pygame.time.Clock()

    while True:
        superficie_tablero = pantalla.subsurface((0, 0, ANCHO, ALTO))
        superficie_info = pantalla.subsurface((0, ALTO, ANCHO, 40))

        # --- Turno de la IA ---
        if tablero.turno != color_humano and esperando_coronacion is None:
            estado = 'IA pensando...'
            dibujar_info(superficie_info, tablero.turno, estado, fuente_info)
            pygame.display.flip()

            mov = mejor_movimiento(tablero, PROFUNDIDAD_IA)
            if mov:
                tablero.hacer_movimiento(*mov)
                estado = f'IA jugó {mov}'
            else:
                estado = 'IA sin movimientos'

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                x, y = evento.pos

                # Menú de coronación activo
                if esperando_coronacion is not None and y < ALTO:
                    fila_c, col_c = esperando_coronacion
                    color_c = tablero.casillas[fila_c][col_c].color
                    rects = dibujar_menu_coronacion(pantalla, color_c, fuente)
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(x, y):
                            tablero.coronar_peon(fila_c, col_c, OPCIONES_CORONACION[i])
                            esperando_coronacion = None
                            estado = ''
                            break
                    continue

                # Movimiento normal del humano
                if tablero.turno == color_humano and y < ALTO:
                    fila, col = pixel_a_casilla(x, y)
                    pieza = tablero.casillas[fila][col]

                    if seleccion is None:
                        if pieza and pieza.color == color_humano:
                            seleccion = (fila, col)
                            legales = tablero.movimientos_legales(color_humano)
                            movimientos_validos = [d for o, d in legales if o == seleccion]
                    else:
                        if (fila, col) in movimientos_validos:
                            tablero.hacer_movimiento(seleccion, (fila, col))
                            seleccion = None
                            movimientos_validos = []
                            estado = ''

                            # Comprobar si el humano acaba de coronar
                            ultimo = tablero.historial[-1]
                            if ultimo.get('coronacion'):
                                fd, cd = ultimo['destino']
                                esperando_coronacion = (fd, cd)

                        elif pieza and pieza.color == color_humano:
                            seleccion = (fila, col)
                            legales = tablero.movimientos_legales(color_humano)
                            movimientos_validos = [d for o, d in legales if o == seleccion]
                        else:
                            seleccion = None
                            movimientos_validos = []

        # --- Comprobar fin de partida ---
        if esperando_coronacion is None:
            legales_actuales = tablero.movimientos_legales(tablero.turno)
            if not legales_actuales:
                if tablero.rey_en_jaque(tablero.turno):
                    estado = f'¡Jaque mate! Ganan las {("negras" if tablero.turno == "blanco" else "blancas")}'
                else:
                    estado = 'Ahogado — tablas'

        # --- Renderizado ---
        dibujar_tablero(superficie_tablero)
        dibujar_seleccion(superficie_tablero, seleccion, movimientos_validos)
        dibujar_jaque(superficie_tablero, tablero)
        dibujar_piezas(superficie_tablero, tablero, fuente)
        dibujar_info(superficie_info, tablero.turno, estado, fuente_info)

        if esperando_coronacion is not None:
            fila_c, col_c = esperando_coronacion
            color_c = tablero.casillas[fila_c][col_c].color
            dibujar_menu_coronacion(pantalla, color_c, fuente)

        pygame.display.flip()
        reloj.tick(30)


if __name__ == '__main__':
    main()


# ------------------------------------------------------------------
# Configuración visual
# ------------------------------------------------------------------

ANCHO = 640
ALTO = 640
TAMANO_CASILLA = ANCHO // 8
PROFUNDIDAD_IA = 3

COLOR_CLARO    = (240, 217, 181)
COLOR_OSCURO   = (181, 136,  99)
COLOR_SELECCION = (106, 168,  79, 180)
COLOR_MOVIMIENTO = (106, 168,  79, 100)
COLOR_JAQUE    = (220,  50,  50, 180)
FONDO_INFO     = ( 30,  30,  30)
COLOR_TEXTO    = (255, 255, 255)

SIMBOLOS = {
    'P': '♙', 'p': '♟',
    'T': '♖', 't': '♜',
    'C': '♘', 'c': '♞',
    'A': '♗', 'a': '♝',
    'D': '♕', 'd': '♛',
    'R': '♔', 'r': '♚',
}


# ------------------------------------------------------------------
# Funciones de dibujo
# ------------------------------------------------------------------

def dibujar_tablero(superficie):
    for fila in range(8):
        for col in range(8):
            color = COLOR_CLARO if (fila + col) % 2 == 0 else COLOR_OSCURO
            pygame.draw.rect(superficie, color,
                             (col * TAMANO_CASILLA, fila * TAMANO_CASILLA,
                              TAMANO_CASILLA, TAMANO_CASILLA))


def dibujar_piezas(superficie, tablero, fuente):
    for fila in range(8):
        for col in range(8):
            pieza = tablero.casillas[fila][col]
            if pieza:
                simbolo = SIMBOLOS.get(str(pieza), '?')
                color_pieza = (255, 255, 255) if pieza.color == 'blanco' else (20, 20, 20)
                texto = fuente.render(simbolo, True, color_pieza)
                x = col * TAMANO_CASILLA + (TAMANO_CASILLA - texto.get_width()) // 2
                y = fila * TAMANO_CASILLA + (TAMANO_CASILLA - texto.get_height()) // 2
                superficie.blit(texto, (x, y))


def dibujar_seleccion(superficie, seleccion, movimientos_validos):
    capa = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA), pygame.SRCALPHA)

    if seleccion:
        fila, col = seleccion
        capa.fill(COLOR_SELECCION)
        superficie.blit(capa, (col * TAMANO_CASILLA, fila * TAMANO_CASILLA))

    capa.fill(COLOR_MOVIMIENTO)
    for fila, col in movimientos_validos:
        superficie.blit(capa, (col * TAMANO_CASILLA, fila * TAMANO_CASILLA))


def dibujar_jaque(superficie, tablero):
    pos_rey = tablero.encontrar_rey(tablero.turno)
    if pos_rey and tablero.rey_en_jaque(tablero.turno):
        fila, col = pos_rey
        capa = pygame.Surface((TAMANO_CASILLA, TAMANO_CASILLA), pygame.SRCALPHA)
        capa.fill(COLOR_JAQUE)
        superficie.blit(capa, (col * TAMANO_CASILLA, fila * TAMANO_CASILLA))


def dibujar_info(superficie_info, turno, estado, fuente_info):
    superficie_info.fill(FONDO_INFO)
    msg = f"Turno: {turno.capitalize()}   {estado}"
    texto = fuente_info.render(msg, True, COLOR_TEXTO)
    superficie_info.blit(texto, (10, 8))


# ------------------------------------------------------------------
# Conversión coordenadas ratón -> casilla
# ------------------------------------------------------------------

def pixel_a_casilla(x, y):
    return y // TAMANO_CASILLA, x // TAMANO_CASILLA


# ------------------------------------------------------------------
# Bucle principal
# ------------------------------------------------------------------

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO + 40))
    pygame.display.set_caption('Ajedrez — Humano vs IA')

    fuente = pygame.font.SysFont('segoeuisymbol', 52)
    fuente_info = pygame.font.SysFont('arial', 18)

    tablero = Tablero()
    seleccion = None
    movimientos_validos = []
    estado = ''
    color_humano = 'blanco'

    reloj = pygame.time.Clock()

    while True:
        superficie_tablero = pantalla.subsurface((0, 0, ANCHO, ALTO))
        superficie_info = pantalla.subsurface((0, ALTO, ANCHO, 40))

        # --- Turno de la IA ---
        if tablero.turno != color_humano:
            estado = 'IA pensando...'
            dibujar_info(superficie_info, tablero.turno, estado, fuente_info)
            pygame.display.flip()

            mov = mejor_movimiento(tablero, PROFUNDIDAD_IA)
            if mov:
                tablero.hacer_movimiento(*mov)
                estado = f'IA jugó {mov}'
            else:
                estado = 'IA sin movimientos'

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and tablero.turno == color_humano:
                x, y = evento.pos
                if y < ALTO:
                    fila, col = pixel_a_casilla(x, y)
                    pieza = tablero.casillas[fila][col]

                    if seleccion is None:
                        # Primera pulsación: seleccionar pieza propia
                        if pieza and pieza.color == color_humano:
                            seleccion = (fila, col)
                            legales = tablero.movimientos_legales(color_humano)
                            movimientos_validos = [d for o, d in legales if o == seleccion]
                    else:
                        # Segunda pulsación: mover o cambiar selección
                        if (fila, col) in movimientos_validos:
                            tablero.hacer_movimiento(seleccion, (fila, col))
                            seleccion = None
                            movimientos_validos = []
                            estado = ''
                        elif pieza and pieza.color == color_humano:
                            seleccion = (fila, col)
                            legales = tablero.movimientos_legales(color_humano)
                            movimientos_validos = [d for o, d in legales if o == seleccion]
                        else:
                            seleccion = None
                            movimientos_validos = []

        # --- Comprobar fin de partida ---
        legales_actuales = tablero.movimientos_legales(tablero.turno)
        if not legales_actuales:
            if tablero.rey_en_jaque(tablero.turno):
                estado = f'¡Jaque mate! Ganan las {("negras" if tablero.turno == "blanco" else "blancas")}'
            else:
                estado = 'Ahogado — tablas'

        # --- Renderizado ---
        dibujar_tablero(superficie_tablero)
        dibujar_seleccion(superficie_tablero, seleccion, movimientos_validos)
        dibujar_jaque(superficie_tablero, tablero)
        dibujar_piezas(superficie_tablero, tablero, fuente)
        dibujar_info(superficie_info, tablero.turno, estado, fuente_info)

        pygame.display.flip()
        reloj.tick(30)


if __name__ == '__main__':
    main()