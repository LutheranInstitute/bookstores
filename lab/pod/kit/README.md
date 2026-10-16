# L://Pro^gif.skills · kit

Pipeline abierto (#opensourceware) del GIF diario #zeitgeist de #grandesmodelosdelenguaje.

1. Arte 9:16: pizarra oscura, una sola línea de tiza, sin texto, espacio arriba y abajo.
2. `python3 make_gif.py arte.png base.gif "TITULAR" "SUBLÍNEA" "#grandesmodelosdelenguaje #latam"` — la línea se dibuja sobre su propio trazo, el titular se escribe (540x960, ~8 s).
3. `python3 endcard.py base.gif clarin-wordmark.png final.gif` — +3 s: fundido al cierre Clærín en tiza (~11 s).
4. Texto para X: titular + dato + 🛸🛸🛸 + `#grandesmodelosdelenguaje #latam #zeitgeist 🎺✍️`.

Requiere Python 3, Pillow, NumPy, SciPy. Nada se publica sin aprobación humana. Evidencia ≠ Autoridad.
