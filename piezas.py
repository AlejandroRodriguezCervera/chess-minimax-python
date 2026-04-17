class Pieza:
    def __init__(self, color):
        # color: 'blanco' o 'negro'
        self.color = color

    def es_enemigo(self, otra):
        return otra is not None and otra.color != self.color

    def movimientos_posibles(self, fila, col, tablero):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError


class Peon(Pieza):
    def __repr__(self):
        return 'P' if self.color == 'blanco' else 'p'

    def movimientos_posibles(self, fila, col, tablero):
        movimientos = []
        direccion = -1 if self.color == 'blanco' else 1
        fila_inicio = 6 if self.color == 'blanco' else 1

        # Avance simple
        nueva_fila = fila + direccion
        if 0 <= nueva_fila <= 7 and tablero[nueva_fila][col] is None:
            movimientos.append((nueva_fila, col))

            # Avance doble desde posición inicial
            if fila == fila_inicio and tablero[fila + 2 * direccion][col] is None:
                movimientos.append((fila + 2 * direccion, col))

        # Capturas diagonales
        for dc in [-1, 1]:
            nueva_col = col + dc
            if 0 <= nueva_fila <= 7 and 0 <= nueva_col <= 7:
                destino = tablero[nueva_fila][nueva_col]
                if self.es_enemigo(destino):
                    movimientos.append((nueva_fila, nueva_col))

        return movimientos


class Torre(Pieza):
    def __repr__(self):
        return 'T' if self.color == 'blanco' else 't'

    def movimientos_posibles(self, fila, col, tablero):
        return _deslizamiento(self, fila, col, tablero, [(1,0),(-1,0),(0,1),(0,-1)])


class Alfil(Pieza):
    def __repr__(self):
        return 'A' if self.color == 'blanco' else 'a'

    def movimientos_posibles(self, fila, col, tablero):
        return _deslizamiento(self, fila, col, tablero, [(1,1),(1,-1),(-1,1),(-1,-1)])


class Dama(Pieza):
    def __repr__(self):
        return 'D' if self.color == 'blanco' else 'd'

    def movimientos_posibles(self, fila, col, tablero):
        direcciones = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        return _deslizamiento(self, fila, col, tablero, direcciones)


class Caballo(Pieza):
    def __repr__(self):
        return 'C' if self.color == 'blanco' else 'c'

    def movimientos_posibles(self, fila, col, tablero):
        movimientos = []
        saltos = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for df, dc in saltos:
            nf, nc = fila + df, col + dc
            if 0 <= nf <= 7 and 0 <= nc <= 7:
                destino = tablero[nf][nc]
                if destino is None or self.es_enemigo(destino):
                    movimientos.append((nf, nc))
        return movimientos


class Rey(Pieza):
    def __repr__(self):
        return 'R' if self.color == 'blanco' else 'r'

    def movimientos_posibles(self, fila, col, tablero):
        movimientos = []
        for df in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if df == 0 and dc == 0:
                    continue
                nf, nc = fila + df, col + dc
                if 0 <= nf <= 7 and 0 <= nc <= 7:
                    destino = tablero[nf][nc]
                    if destino is None or self.es_enemigo(destino):
                        movimientos.append((nf, nc))

        # Enroque — las condiciones completas se validan en Tablero,
        # aquí solo añadimos los destinos especiales del rey (col 6 y col 2)
        # para que el generador de movimientos los considere.
        # El tablero los filtrará si no se cumplen las condiciones.
        fila_rey = 7 if self.color == 'blanco' else 0
        if fila == fila_rey and col == 4:
            # Enroque corto: rey va a col 6
            movimientos.append((fila_rey, 6))
            # Enroque largo: rey va a col 2
            movimientos.append((fila_rey, 2))

        return movimientos


# --- Función auxiliar para piezas deslizantes ---

def _deslizamiento(pieza, fila, col, tablero, direcciones):
    movimientos = []
    for df, dc in direcciones:
        nf, nc = fila + df, col + dc
        while 0 <= nf <= 7 and 0 <= nc <= 7:
            destino = tablero[nf][nc]
            if destino is None:
                movimientos.append((nf, nc))
            elif pieza.es_enemigo(destino):
                movimientos.append((nf, nc))
                break
            else:
                break
            nf += df
            nc += dc
    return movimientos