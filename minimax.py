from evaluador import evaluar

# Valor que representa victoria/derrota absoluta
INFINITO = float('inf')


def minimax(tablero, profundidad, alpha, beta, maximizando):
    """
    Minimax con poda Alpha-Beta.

    - profundidad: cuántos niveles más explorar
    - alpha: mejor puntuación garantizada para blancas
    - beta: mejor puntuación garantizada para negras
    - maximizando: True si es el turno de las blancas

    Devuelve la puntuación de la posición.
    """

    # Caso base: profundidad 0 o sin movimientos legales
    color_actual = 'blanco' if maximizando else 'negro'
    movimientos = tablero.movimientos_legales(color_actual)

    if profundidad == 0 or not movimientos:
        return _evaluar_terminal(tablero, movimientos, color_actual)

    if maximizando:
        mejor = -INFINITO
        for origen, destino in movimientos:
            tablero.hacer_movimiento(origen, destino)
            puntuacion = minimax(tablero, profundidad - 1, alpha, beta, False)
            tablero.deshacer_movimiento()

            mejor = max(mejor, puntuacion)
            alpha = max(alpha, mejor)
            if beta <= alpha:
                break  # poda beta — las negras nunca elegirían esta rama
        return mejor

    else:
        mejor = INFINITO
        for origen, destino in movimientos:
            tablero.hacer_movimiento(origen, destino)
            puntuacion = minimax(tablero, profundidad - 1, alpha, beta, True)
            tablero.deshacer_movimiento()

            mejor = min(mejor, puntuacion)
            beta = min(beta, mejor)
            if beta <= alpha:
                break  # poda alpha — las blancas nunca elegirían esta rama
        return mejor


def _evaluar_terminal(tablero, movimientos, color):
    """
    Si no hay movimientos: jaque mate o ahogado.
    Si hay movimientos pero profundidad=0: evaluación estática.
    """
    if not movimientos:
        if tablero.rey_en_jaque(color):
            # Jaque mate: la peor puntuación posible para el color en turno
            return -INFINITO if color == 'blanco' else INFINITO
        else:
            # Ahogado: tablas
            return 0
    return evaluar(tablero)


def mejor_movimiento(tablero, profundidad=3):
    """
    Devuelve el mejor movimiento para el color en turno.
    Si todas las jugadas son perdedoras, devuelve la primera disponible
    en lugar de None — la IA siempre hace un movimiento si puede.
    """
    maximizando = tablero.turno == 'blanco'
    color = tablero.turno
    movimientos = tablero.movimientos_legales(color)

    if not movimientos:
        return None

    mejor = None
    mejor_puntuacion = -INFINITO if maximizando else INFINITO

    for origen, destino in movimientos:
        tablero.hacer_movimiento(origen, destino)
        puntuacion = minimax(tablero, profundidad - 1, -INFINITO, INFINITO, not maximizando)
        tablero.deshacer_movimiento()

        if maximizando and puntuacion > mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor = (origen, destino)
        elif not maximizando and puntuacion < mejor_puntuacion:
            mejor_puntuacion = puntuacion
            mejor = (origen, destino)

        # Guardar siempre el primero como fallback
        if mejor is None:
            mejor = (origen, destino)

    return mejor