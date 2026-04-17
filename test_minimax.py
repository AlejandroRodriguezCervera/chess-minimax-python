from tablero import Tablero
from minimax import mejor_movimiento

t = Tablero()
print(t)
mov = mejor_movimiento(t, profundidad=3)
print(f"Mejor movimiento: {mov}")