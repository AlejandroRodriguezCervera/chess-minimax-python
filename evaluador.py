from piezas import Peon, Caballo, Alfil, Torre, Dama, Rey

# ------------------------------------------------------------------
# Valor material de cada pieza
# ------------------------------------------------------------------

VALOR_MATERIAL = {
    Peon:   100,
    Caballo: 320,
    Alfil:   330,
    Torre:   500,
    Dama:    900,
    Rey:    20000,
}

# ------------------------------------------------------------------
# Tablas posicionales (desde la perspectiva del blanco)
# Bonus/penalización según en qué casilla está la pieza
# Fuente: chessprogramming.org / PeSTO
# ------------------------------------------------------------------

TABLA_PEON = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 25, 25, 10,  5,  5,
     0,  0,  0, 20, 20,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-20,-20, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0,
]

TABLA_CABALLO = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

TABLA_ALFIL = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]

TABLA_TORRE = [
     0,  0,  0,  0,  0,  0,  0,  0,
     5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
     0,  0,  0,  5,  5,  0,  0,  0,
]

TABLA_DAMA = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
     -5,  0,  5,  5,  5,  5,  0, -5,
      0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20,
]

TABLA_REY = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-30,-30,-20,-20,-10,
     10, 10, -5,-15,-15, -5, 10, 10,
     20, 30, 25, -5, -5, 15, 35, 20,  # g1/g8 y c1/c8 premiados (enroque)
]

TABLAS = {
    Peon:    TABLA_PEON,
    Caballo: TABLA_CABALLO,
    Alfil:   TABLA_ALFIL,
    Torre:   TABLA_TORRE,
    Dama:    TABLA_DAMA,
    Rey:     TABLA_REY,
}

# ------------------------------------------------------------------
# Función principal de evaluación
# ------------------------------------------------------------------

def evaluar(tablero):
    """
    Devuelve la puntuación del tablero en centipeones.
    Positivo = ventaja blancas, negativo = ventaja negras.
    """
    puntuacion = 0

    for fila in range(8):
        for col in range(8):
            pieza = tablero.casillas[fila][col]
            if pieza is None:
                continue

            tipo = type(pieza)
            valor = VALOR_MATERIAL[tipo]
            bonus = _bonus_posicional(tipo, fila, col, pieza.color)

            if pieza.color == 'blanco':
                puntuacion += valor + bonus
            else:
                puntuacion -= valor + bonus

    return puntuacion


def _bonus_posicional(tipo, fila, col, color):
    """
    Consulta la tabla posicional de la pieza.
    Para el negro se espeja verticalmente (fila 0 <-> fila 7).
    """
    tabla = TABLAS.get(tipo)
    if tabla is None:
        return 0

    if color == 'blanco':
        indice = fila * 8 + col
    else:
        indice = (7 - fila) * 8 + col

    return tabla[indice]