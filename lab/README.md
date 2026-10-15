# lab/ · Laboratorio de la red de tiendas

Aquí se prueba; en la raíz de cada tienda se vende.

| Tienda | En vivo | Laboratorio |
|---|---|---|
| L://Gospel_Bookstore | [`gospel/`](https://lutheraninstitute.github.io/bookstores/gospel/) | [`lab/gospel/`](https://lutheraninstitute.github.io/bookstores/lab/gospel/) |
| L://teologia.ai/gospel_bookstore (expresión teológica: Ley y Evangelio del día + lecturas por pasaje) | dominio teologia.ai pendiente | [`lab/teologia.ai/gospel_bookstore/`](https://lutheraninstitute.github.io/bookstores/lab/teologia.ai/gospel_bookstore/) |

## Flujo
1. Issue con la idea.
2. Rama → cambios en `lab/<tienda>/` → se ven en vivo en su enlace de laboratorio.
3. Cuando funciona, pull request que copia el cambio a `<tienda>/`.
4. Yæl aprueba y fusiona a `main`: sale a la tienda real.

## Reglas
- El laboratorio lleva la marca **LAB** y `noindex`.
- El lab lee el mismo `catalog.json` de la tienda; no lleva su propio catálogo.
- El botón de pago lleva a la tienda oficial real. Probar sin completar el pago.
- Ningún agente publica precios, procesa órdenes ni cambia inventario. Evidencia ≠ Autoridad.

## Expresiones
Una tienda puede tener varias expresiones (otra voz, mismo catálogo y mismo carrito). Cada expresión lee el `catalog.json` de su tienda y vive en `lab/<dominio>/<tienda>/` hasta que su dominio se conecte.
