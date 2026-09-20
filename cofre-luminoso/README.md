# Cofre Luminoso

Tu **archivo vivo de gastos de tarjeta HSBC**: movimientos categorizados, CSV/JSON y reportes para retomar el control y ahorrar.

## Contenido

| Ruta | Qué es |
|------|--------|
| `fuente/` | PDF original del estado de cuenta |
| `data/movimientos.json` | Movimientos + metadatos + totales por categoría |
| `data/movimientos.csv` | Misma información para Excel/Sheets |
| `reportes/resumen-2026-09-18.md` | Análisis del corte sep 2026 |
| `scripts/categorizar_movimientos.py` | Regenera CSV/JSON (editar movimientos ahí) |

## Cómo invocarlo después

En Cursor (o conmigo en otra sesión), di por ejemplo:

- *“Lee la carpeta **cofre-luminoso** y dime en qué categoría gasté más.”*
- *“Agrega el nuevo estado de cuenta a **cofre-luminoso**.”*
- *“Regenera el reporte de **cofre-luminoso**.”*

Ruta absoluta: `/workspace/cofre-luminoso`

## Regenerar datos

```bash
python3 /workspace/cofre-luminoso/scripts/categorizar_movimientos.py
```

## Categorías usadas

Transporte · Supermercado · Farmacia y salud · Restaurantes y cafés · Conveniencia · Suscripciones · Entretenimiento · Compras personales · Mascotas · Telecomunicaciones · Compras a meses (MSI) · Pagos y abonos

Puedes ajustar reglas en `clasificar()` dentro del script.
