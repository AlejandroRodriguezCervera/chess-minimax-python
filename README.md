[README.md](https://github.com/user-attachments/files/26813404/README.md)
# chess-minimax-python

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green) ![Version](https://img.shields.io/badge/version-1.0.0-orange) ![License](https://img.shields.io/badge/license-MIT-lightgrey)

Ajedrez jugable con interfaz visual en **Pygame** y motor de IA basado en el algoritmo **Minimax con poda Alpha-Beta**. Proyecto desarrollado desde cero en Python como ejercicio de inteligencia artificial clásica aplicada a juegos de tablero.

---

## Demo

![tablero](https://raw.githubusercontent.com/tu-usuario/chess-minimax-python/main/assets/demo.png)

> *Sustituye la imagen por una captura real de la partida*

---

## Características

- Tablero visual con **Pygame** — piezas Unicode, casillas resaltadas y marcador de jaque
- Motor IA con **Minimax + poda Alpha-Beta** (profundidad configurable, por defecto 3)
- **Función de evaluación heurística**: valor material + tablas posicionales por pieza
- Reglas completas implementadas:
  - Movimientos legales con filtrado de jaque
  - Enroque corto y largo para ambos colores
  - Coronación de peón con menú de selección de pieza
  - Detección de jaque mate y ahogado
- Arquitectura modular y bien separada — fácil de extender

---

## Estructura del proyecto

```
chess-minimax-python/
├── main.py          # Bucle principal y renderizado Pygame
├── tablero.py       # Estado del juego, hacer/deshacer movimientos
├── piezas.py        # Clases de piezas y generación de movimientos
├── minimax.py       # Algoritmo Minimax con poda Alpha-Beta
├── evaluador.py     # Función heurística de evaluación de posición
└── README.md
```

---

## Instalación

```bash
git clone https://github.com/tu-usuario/chess-minimax-python.git
cd chess-minimax-python
pip install pygame
python main.py
```

---

## Cómo jugar

- **Click** en una pieza blanca para seleccionarla — se resaltan en verde los movimientos legales
- **Click** en una casilla verde para mover
- La IA responde automáticamente jugando con las negras
- Si un peón corona, aparece un **menú de selección** de pieza
- El rey se marca en **rojo** cuando está en jaque
- La barra inferior muestra el turno y el estado de la partida

---

## Algoritmo

El motor usa **Minimax con poda Alpha-Beta**. En cada turno, el algoritmo explora el árbol de jugadas hasta la profundidad configurada y elige el movimiento que maximiza la puntuación para las blancas o la minimiza para las negras.

La **función de evaluación** combina:
- Valor material de las piezas (peón=100, caballo=320, alfil=330, torre=500, dama=900)
- Tablas posicionales por tipo de pieza — premian el control del centro, el enroque y la actividad

La poda Alpha-Beta elimina ramas del árbol que no pueden mejorar la decisión actual, lo que permite duplicar la profundidad efectiva respecto a Minimax puro.

---

## Configuración

En `main.py` puedes ajustar:

```python
PROFUNDIDAD_IA = 3   # Aumentar para una IA más fuerte (y más lenta)
```

| Profundidad | Tiempo aprox. por jugada | Nivel estimado |
|-------------|--------------------------|----------------|
| 2           | < 0.5 s                  | Principiante   |
| 3           | 1 – 3 s                  | Intermedio     |
| 4           | 5 – 15 s                 | Avanzado       |

---

## Posibles mejoras futuras

- Regla *en passant*
- Búsqueda de quiescencia para evitar el efecto horizonte
- Apertura con libro de tablas
- Interfaz para elegir color y profundidad al inicio
- Exportar partidas en notación PGN

---

## Autor

**Alejandro Rodríguez Cervera**  
[Portfolio](https://alejandrorc.carrd.co) · [LinkedIn]([https://www.linkedin.com/in/alejandro-rodriguez-cervera-62544a35b/])

---

## Versión

`v1.0.0` — Primera versión estable con IA funcional, enroque y coronación.
