from piezas import Peon, Torre, Alfil, Dama, Caballo, Rey


class Tablero:
    def __init__(self):
        self.casillas = [[None] * 8 for _ in range(8)]
        self.turno = 'blanco'
        self.historial = []  # para deshacer movimientos en Minimax

        # Derechos de enroque: se pierden al mover rey o torre
        self.enroque = {
            'blanco': {'corto': True, 'largo': True},
            'negro':  {'corto': True, 'largo': True},
        }
        self._colocar_piezas()

    # ------------------------------------------------------------------
    # Configuración inicial
    # ------------------------------------------------------------------

    def _colocar_piezas(self):
        orden = [Torre, Caballo, Alfil, Dama, Rey, Alfil, Caballo, Torre]

        for col, ClasePieza in enumerate(orden):
            self.casillas[0][col] = ClasePieza('negro')
            self.casillas[7][col] = ClasePieza('blanco')

        for col in range(8):
            self.casillas[1][col] = Peon('negro')
            self.casillas[6][col] = Peon('blanco')

    # ------------------------------------------------------------------
    # Hacer y deshacer movimientos
    # ------------------------------------------------------------------

    def hacer_movimiento(self, origen, destino):
        """Mueve la pieza y guarda el estado anterior para poder deshacerlo."""
        fila_o, col_o = origen
        fila_d, col_d = destino

        pieza_movida = self.casillas[fila_o][col_o]
        pieza_capturada = self.casillas[fila_d][col_d]
        es_enroque = False
        torre_origen = torre_destino = None

        # Detectar enroque: rey se mueve dos casillas horizontalmente
        if isinstance(pieza_movida, Rey) and abs(col_d - col_o) == 2:
            es_enroque = True
            if col_d == 6:  # enroque corto
                torre_origen = (fila_o, 7)
                torre_destino = (fila_o, 5)
            else:           # enroque largo
                torre_origen = (fila_o, 0)
                torre_destino = (fila_o, 3)

        # Guardar estado completo para deshacer (incluyendo derechos de enroque)
        self.historial.append({
            'origen': origen,
            'destino': destino,
            'pieza_movida': pieza_movida,
            'pieza_capturada': pieza_capturada,
            'turno': self.turno,
            'es_enroque': es_enroque,
            'torre_origen': torre_origen,
            'torre_destino': torre_destino,
            'enroque': {
                'blanco': dict(self.enroque['blanco']),
                'negro':  dict(self.enroque['negro']),
            },
        })

        # Mover rey
        self.casillas[fila_d][col_d] = pieza_movida
        self.casillas[fila_o][col_o] = None

        # Mover torre si es enroque
        if es_enroque:
            tf_o, tc_o = torre_origen
            tf_d, tc_d = torre_destino
            self.casillas[tf_d][tc_d] = self.casillas[tf_o][tc_o]
            self.casillas[tf_o][tc_o] = None

        # Actualizar derechos de enroque
        color = pieza_movida.color
        if isinstance(pieza_movida, Rey):
            self.enroque[color]['corto'] = False
            self.enroque[color]['largo'] = False
        elif isinstance(pieza_movida, Torre):
            fila_base = 7 if color == 'blanco' else 0
            if col_o == 7:
                self.enroque[color]['corto'] = False
            elif col_o == 0:
                self.enroque[color]['largo'] = False

        self.turno = 'negro' if self.turno == 'blanco' else 'blanco'

        # Detectar coronación de peón
        pieza_en_destino = self.casillas[fila_d][col_d]
        fila_coronacion = 0 if pieza_en_destino.color == 'blanco' else 7
        if isinstance(pieza_en_destino, Peon) and fila_d == fila_coronacion:
            # La IA siempre corona en dama; el humano se gestiona desde main.py
            self.historial[-1]['coronacion'] = True
            self.casillas[fila_d][col_d] = Dama(pieza_en_destino.color)
        else:
            self.historial[-1]['coronacion'] = False

    def deshacer_movimiento(self):
        """Deshace el último movimiento. Clave para el árbol Minimax."""
        if not self.historial:
            return

        estado = self.historial.pop()
        fila_o, col_o = estado['origen']
        fila_d, col_d = estado['destino']

        self.casillas[fila_o][col_o] = estado['pieza_movida']
        self.casillas[fila_d][col_d] = estado['pieza_capturada']

        # Si hubo coronación, restaurar el peón original
        if estado.get('coronacion'):
            self.casillas[fila_o][col_o] = estado['pieza_movida']  # ya es el peón

        # Deshacer movimiento de torre si era enroque
        if estado['es_enroque']:
            tf_o, tc_o = estado['torre_origen']
            tf_d, tc_d = estado['torre_destino']
            self.casillas[tf_o][tc_o] = self.casillas[tf_d][tc_d]
            self.casillas[tf_d][tc_d] = None

        # Restaurar derechos de enroque
        self.enroque = estado['enroque']
        self.turno = estado['turno']

    def coronar_peon(self, fila, col, clase_pieza):
        """Sustituye la dama temporal por la pieza elegida por el humano."""
        color = self.casillas[fila][col].color
        self.casillas[fila][col] = clase_pieza(color)

    def peon_pendiente_coronacion(self):
        """
        Devuelve (fila, col) si hay un peón coronado esperando elección humana,
        o None si no hay ninguno. Solo afecta al turno del humano.
        """
        for fila, col_destino in [(0, range(8)), (7, range(8))]:
            for col in col_destino:
                pieza = self.casillas[fila][col]
                if isinstance(pieza, Dama) and self.historial:
                    ultimo = self.historial[-1]
                    if ultimo.get('coronacion') and ultimo['destino'] == (fila, col):
                        return (fila, col)
        return None

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    def obtener_pieza(self, fila, col):
        return self.casillas[fila][col]

    def piezas_de(self, color):
        """Devuelve lista de (fila, col, pieza) para un color dado."""
        resultado = []
        for fila in range(8):
            for col in range(8):
                pieza = self.casillas[fila][col]
                if pieza is not None and pieza.color == color:
                    resultado.append((fila, col, pieza))
        return resultado

    def encontrar_rey(self, color):
        for fila, col, pieza in self.piezas_de(color):
            if isinstance(pieza, Rey):
                return (fila, col)
        return None

    def rey_en_jaque(self, color):
        """Comprueba si el rey de 'color' está siendo atacado."""
        pos_rey = self.encontrar_rey(color)
        if pos_rey is None:
            return False

        color_rival = 'negro' if color == 'blanco' else 'blanco'
        for fila, col, pieza in self.piezas_de(color_rival):
            if pos_rey in pieza.movimientos_posibles(fila, col, self.casillas):
                return True
        return False

    def movimientos_legales(self, color):
        """Todos los movimientos que no dejan al rey propio en jaque."""
        legales = []
        for fila, col, pieza in self.piezas_de(color):
            for destino in pieza.movimientos_posibles(fila, col, self.casillas):

                # Filtrar destinos de enroque inválidos antes de simular
                if isinstance(pieza, Rey) and abs(destino[1] - col) == 2:
                    if not self._enroque_legal(color, destino[1]):
                        continue

                self.hacer_movimiento((fila, col), destino)
                if not self.rey_en_jaque(color):
                    legales.append(((fila, col), destino))
                self.deshacer_movimiento()
        return legales

    def _enroque_legal(self, color, col_destino_rey):
        """
        Valida todas las condiciones del enroque:
        1. El rey no ha movido (derecho vigente)
        2. La torre correspondiente no ha movido
        3. Las casillas intermedias están vacías
        4. El rey no está en jaque
        5. El rey no pasa por casillas atacadas
        """
        fila = 7 if color == 'blanco' else 0
        corto = col_destino_rey == 6

        # Condición 1: derecho de enroque vigente
        tipo = 'corto' if corto else 'largo'
        if not self.enroque[color][tipo]:
            return False

        # Condición 2: torre en su sitio
        col_torre = 7 if corto else 0
        torre = self.casillas[fila][col_torre]
        if not isinstance(torre, Torre) or torre.color != color:
            return False

        # Condición 3: casillas intermedias vacías
        cols_intermedias = range(5, 7) if corto else range(1, 4)
        for c in cols_intermedias:
            if self.casillas[fila][c] is not None:
                return False

        # Condición 4: rey no está en jaque
        if self.rey_en_jaque(color):
            return False

        # Condición 5: rey no pasa por casilla atacada
        col_paso = 5 if corto else 3
        pieza_rey = self.casillas[fila][4]
        self.casillas[fila][col_paso] = pieza_rey
        self.casillas[fila][4] = None
        atacado = self.rey_en_jaque(color)
        self.casillas[fila][4] = pieza_rey
        self.casillas[fila][col_paso] = None

        return not atacado

    # ------------------------------------------------------------------
    # Visualización
    # ------------------------------------------------------------------

    def __str__(self):
        filas = []
        filas.append('  a b c d e f g h')
        for i, fila in enumerate(self.casillas):
            num = 8 - i
            contenido = ' '.join(str(p) if p else '.' for p in fila)
            filas.append(f'{num} {contenido}')
        return '\n'.join(filas)