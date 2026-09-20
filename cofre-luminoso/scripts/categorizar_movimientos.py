#!/usr/bin/env python3
"""Genera CSV/JSON y resumen por categoría desde movimientos del estado de cuenta."""

from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

PERIODO = {
    "inicio": "2026-08-19",
    "fin": "2026-09-18",
    "banco": "HSBC",
    "producto": "HSBC One Plus",
    "titular": "Yandy Briceno Rodriguez",
    "cuenta_enmascarada": "4568 **** **** 1157",
}


@dataclass
class Movimiento:
    fecha_operacion: str
    fecha_cargo: str
    descripcion: str
    monto_mxn: float
    tarjeta: str
    categoria: str
    subcategoria: str
    es_abono: bool
    notas: str = ""


def normalizar(desc: str) -> str:
    return re.sub(r"\s+", " ", desc.upper().strip())


def clasificar(desc: str, monto: float) -> tuple[str, str, str]:
    d = normalizar(desc)
    notas = ""

    if "SU PAGO" in d or "USO DE SALDO HSBC CASHBACK" in d:
        return "Pagos y abonos", "Pago / cashback", ""

    if "A MESES" in d or "AMAZON AMESES" in d:
        return "Compras a meses (MSI)", "Cuota mensual", "Sin intereses — 3 meses"

    rules: list[tuple[str, str, list[str]]] = [
        ("Transporte", "App / taxi (Paga)", ["PGA*PAGA", "PGA PAGA", "TAX 1211275"]),
        ("Supermercado", "Hiper / super", ["SUPERCENTER", "CHEDRAUI", "BODEGA"]),
        ("Farmacia y salud", "Farmacia", ["FARM GUAD", "F AHORRO", "FAR GUAD"]),
        ("Farmacia y salud", "Laboratorio / clínica", ["CHOPO", "CONSULTORIO MEDICO", "SUPERNATURISTA"]),
        ("Farmacia y salud", "Suplementos", ["GNC "]),
        ("Restaurantes y cafés", "Bar / restaurante", ["HOSTERIA", "LABOTA", "WENDYS", "CHOPPEADITO", "RESTCAFE", "EPIC REFORMA"]),
        ("Restaurantes y cafés", "Café / repostería", ["CAFEBRERIA", "CLARICE", "LA VALIENTE", "PENDULO", "SANTA CLARA", "HELADOS"]),
        ("Conveniencia", "Tienda de conveniencia", ["OXXO", "CELTok", "CELTok".upper()]),
        ("Suscripciones", "Streaming / software", ["NETFLIX", "SPOTIFY", "ADOBE", "ANTHROPIC", "CLAUDE", "SILBE"]),
        ("Entretenimiento", "Cine / cultura", ["CINEMEX", "MUSEO BIMBO", "GANDHI"]),
        ("Compras personales", "Retail / moda", ["LIVERPOOL", "PALACIO HIERRO", "DECATHLON", "PARISINA", "URBAN"]),
        ("Compras personales", "Marketplace / delivery", ["AMAZON", "D LOCAL", "MERPAGO", "SOFT DRALI"]),
        ("Mascotas", "Tienda mascotas", ["PETCO"]),
        ("Telecomunicaciones", "Telefonía", ["TELCEL"]),
        ("Servicios varios", "Otros comercios", ["CENTRO BUTURINI", "FSN PABLO", "DLO*"]),
    ]

    for cat, sub, keys in rules:
        if any(k in d for k in keys):
            return cat, sub, notas

    if monto < 0:
        return "Pagos y abonos", "Abono", notas
    return "Sin clasificar", "Revisar manualmente", ""


MOVIMIENTOS_RAW: list[dict] = [
    # MSI — tarjeta adicional 8020
    {"fecha_operacion": "2026-09-14", "fecha_cargo": "2026-09-14", "descripcion": "AMAZON A MESES CIUDAD DE MEX", "monto": 226.53, "tarjeta": "adicional ···8020", "notas": "Cuota 1/3; original $679.61"},
    # Titular ···1157
    {"fecha_operacion": "2026-08-25", "fecha_cargo": "2026-08-26", "descripcion": "SU PAGO GRACIAS", "monto": -28936.94, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-18", "fecha_cargo": "2026-08-19", "descripcion": "BAR HOSTERIA LA BOTA", "monto": 913.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-18", "fecha_cargo": "2026-08-20", "descripcion": "OXXO TIZAPAN", "monto": 77.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-20", "fecha_cargo": "2026-08-20", "descripcion": "PGA*PAGA AGR CDM", "monto": 110.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-20", "fecha_cargo": "2026-08-21", "descripcion": "FARM GUAD 1411", "monto": 1049.40, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-20", "fecha_cargo": "2026-08-21", "descripcion": "BODEGA BOLIVAR", "monto": 392.50, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-21", "fecha_cargo": "2026-08-24", "descripcion": "PALACIO HIERRO CENTRO", "monto": 341.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-21", "fecha_cargo": "2026-08-24", "descripcion": "D LOCAL*SOFT DRALI", "monto": 1600.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-21", "fecha_cargo": "2026-08-24", "descripcion": "LIVERPOOL CENTRO", "monto": 319.20, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-22", "fecha_cargo": "2026-08-24", "descripcion": "NETFLIX Bogota CO", "monto": 251.23, "tarjeta": "titular ···1157", "notas": "COP convertido"},
    {"fecha_operacion": "2026-08-22", "fecha_cargo": "2026-08-24", "descripcion": "GANDHI MADERO", "monto": 808.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-23", "fecha_cargo": "2026-08-24", "descripcion": "BPK*RESTCAFE COMUNIDAD", "monto": 517.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-23", "fecha_cargo": "2026-08-24", "descripcion": "BAR HOSTERIA LA BOTA", "monto": 510.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-24", "fecha_cargo": "2026-08-24", "descripcion": "PGA*PAGA AGR CDM", "monto": 63.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-24", "fecha_cargo": "2026-08-25", "descripcion": "F AHORRO MXAS AGUASCA", "monto": 1102.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-24", "fecha_cargo": "2026-08-25", "descripcion": "GNC TDA NAT 112", "monto": 1639.53, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-24", "fecha_cargo": "2026-08-25", "descripcion": "OXXO TIZAPAN", "monto": 658.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-25", "fecha_cargo": "2026-08-25", "descripcion": "PGA*PAGA AGR CDM", "monto": 102.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-25", "fecha_cargo": "2026-08-26", "descripcion": "LA VALIENTE", "monto": 165.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-26", "fecha_cargo": "2026-08-26", "descripcion": "PGA*PAGA AGR CDM", "monto": 108.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-26", "fecha_cargo": "2026-08-27", "descripcion": "LA VALIENTE", "monto": 205.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-27", "fecha_cargo": "2026-08-27", "descripcion": "PGA*PAGA AGR CDM", "monto": 102.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-28", "fecha_cargo": "2026-08-28", "descripcion": "PGA*PAGA AGR CDM", "monto": 102.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-28", "fecha_cargo": "2026-08-31", "descripcion": "CELTok NEZA", "monto": 48.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-29", "fecha_cargo": "2026-08-31", "descripcion": "168 URBAN BOTURINI", "monto": 99.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-29", "fecha_cargo": "2026-08-31", "descripcion": "SUPERCENTER P CENTRO", "monto": 3191.59, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-29", "fecha_cargo": "2026-08-31", "descripcion": "CENTRO BUTURINI", "monto": 450.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-29", "fecha_cargo": "2026-08-31", "descripcion": "SANTA CLARA BOTURINI", "monto": 134.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-30", "fecha_cargo": "2026-08-31", "descripcion": "SMARTPY*REST WENDYS REF", "monto": 533.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-30", "fecha_cargo": "2026-08-31", "descripcion": "EPIC REFORMA 222", "monto": 2546.30, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-08-31", "fecha_cargo": "2026-08-31", "descripcion": "PGA*PAGA AGR CDM", "monto": 108.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-01", "fecha_cargo": "2026-09-01", "descripcion": "PGA*PAGA AGR CDM", "monto": 63.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-01", "fecha_cargo": "2026-09-02", "descripcion": "F AHORRO MXRP R BRASIL", "monto": 490.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-01", "fecha_cargo": "2026-09-02", "descripcion": "ZTL*CONSULTORIO MEDICO", "monto": 1500.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-01", "fecha_cargo": "2026-09-02", "descripcion": "FSN PABLO ISABEL LA CAT", "monto": 487.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-01", "fecha_cargo": "2026-09-02", "descripcion": "LA VALIENTE", "monto": 110.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-02", "fecha_cargo": "2026-09-02", "descripcion": "PGA*PAGA AGR CDM", "monto": 63.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-03", "fecha_cargo": "2026-09-03", "descripcion": "PGA*PAGA AGR CDM", "monto": 63.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-03", "fecha_cargo": "2026-09-04", "descripcion": "PETCO MX", "monto": 1369.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-04", "fecha_cargo": "2026-09-04", "descripcion": "PGA*PAGA AGR CDM", "monto": 108.30, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-04", "fecha_cargo": "2026-09-07", "descripcion": "PETCO MX", "monto": 426.43, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-04", "fecha_cargo": "2026-09-07", "descripcion": "DECATHLON POLANCO", "monto": 397.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-04", "fecha_cargo": "2026-09-07", "descripcion": "OXXO MOLIERE", "monto": 24.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-05", "fecha_cargo": "2026-09-07", "descripcion": "OXXO TIZAPAN", "monto": 235.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-06", "fecha_cargo": "2026-09-07", "descripcion": "CAFEBRERIA EL PENDULO", "monto": 419.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-06", "fecha_cargo": "2026-09-07", "descripcion": "CLARICE CAFE LITERATUR", "monto": 462.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-07", "fecha_cargo": "2026-09-07", "descripcion": "PGA*PAGA AGR CDM", "monto": 54.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-07", "fecha_cargo": "2026-09-08", "descripcion": "LA VALIENTE", "monto": 205.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-07", "fecha_cargo": "2026-09-08", "descripcion": "OXXO MEDICO MILITAR", "monto": 35.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-08", "fecha_cargo": "2026-09-08", "descripcion": "PGA*PAGA AGR CDM", "monto": 102.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-08", "fecha_cargo": "2026-09-09", "descripcion": "SUPERNATURISTA IZAZAG", "monto": 215.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-08", "fecha_cargo": "2026-09-09", "descripcion": "OXXO TIZAPAN", "monto": 53.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-08", "fecha_cargo": "2026-09-09", "descripcion": "CHEDRAUI BUEN TONO 129", "monto": 1251.65, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-09", "fecha_cargo": "2026-09-09", "descripcion": "PGA*PAGA AGR CDM", "monto": 63.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-10", "fecha_cargo": "2026-09-10", "descripcion": "PGA*PAGA AGR CDM", "monto": 102.60, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-11", "fecha_cargo": "2026-09-14", "descripcion": "SUPERCENTER P CENTRO", "monto": 2102.83, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-11", "fecha_cargo": "2026-09-14", "descripcion": "OXXO TIZAPAN", "monto": 200.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-12", "fecha_cargo": "2026-09-14", "descripcion": "MERPAGO*BERENICELAZ", "monto": 1400.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-12", "fecha_cargo": "2026-09-14", "descripcion": "ZTL*CHOPPEADITO", "monto": 440.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-12", "fecha_cargo": "2026-09-14", "descripcion": "BAR HOSTERIA LA BOTA", "monto": 500.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-13", "fecha_cargo": "2026-09-14", "descripcion": "FAR GUAD 2789", "monto": 169.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-14", "fecha_cargo": "2026-09-15", "descripcion": "LA VALIENTE", "monto": 275.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-15", "fecha_cargo": "2026-09-15", "descripcion": "PGA*PAGA AGR CDM", "monto": 108.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-15", "fecha_cargo": "2026-09-17", "descripcion": "F AHORRO MXBL ISABEL", "monto": 1794.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-15", "fecha_cargo": "2026-09-17", "descripcion": "TELAS PARISINA 902", "monto": 28.97, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-16", "fecha_cargo": "2026-09-17", "descripcion": "HELADOS SANTA CLARA", "monto": 65.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-16", "fecha_cargo": "2026-09-17", "descripcion": "GLOBO MUSEO BIMBO", "monto": 97.00, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-17", "fecha_cargo": "2026-09-18", "descripcion": "PGA*PAGA AGR CDM", "monto": 102.60, "tarjeta": "titular ···1157"},
    {"fecha_operacion": "2026-09-18", "fecha_cargo": "2026-09-18", "descripcion": "PGA*PAGA AGR CDM", "monto": 63.00, "tarjeta": "titular ···1157"},
    # Adicional ···8020
    {"fecha_operacion": "2026-08-26", "fecha_cargo": "2026-08-27", "descripcion": "SILBE BY SILVY APP (39.99 USD)", "monto": 681.86, "tarjeta": "adicional ···8020"},
    {"fecha_operacion": "2026-08-30", "fecha_cargo": "2026-08-31", "descripcion": "STR*CINEMEX COM", "monto": 328.00, "tarjeta": "adicional ···8020"},
    {"fecha_operacion": "2026-09-04", "fecha_cargo": "2026-09-07", "descripcion": "PPROMEX*ADOBE", "monto": 276.89, "tarjeta": "adicional ···8020"},
    {"fecha_operacion": "2026-09-05", "fecha_cargo": "2026-09-07", "descripcion": "TELCEL 9MPS ECOM", "monto": 316.80, "tarjeta": "adicional ···8020"},
    {"fecha_operacion": "2026-09-05", "fecha_cargo": "2026-09-07", "descripcion": "CHOPO 9003 LIGA E PAG", "monto": 3595.51, "tarjeta": "adicional ···8020"},
    {"fecha_operacion": "2026-09-10", "fecha_cargo": "2026-09-11", "descripcion": "ANTHROPIC* CLAUDE SUB (20 USD)", "monto": 341.14, "tarjeta": "adicional ···8020"},
    {"fecha_operacion": "2026-09-18", "fecha_cargo": "2026-09-18", "descripcion": "DLO*SPOTIFY MEX", "monto": 74.00, "tarjeta": "adicional ···8020"},
    # Adicional ···1207
    {"fecha_operacion": "2026-09-13", "fecha_cargo": "2026-09-14", "descripcion": "SUPERCENTER P CENTRO", "monto": 1004.00, "tarjeta": "adicional ···1207"},
    {"fecha_operacion": "2026-09-14", "fecha_cargo": "2026-09-14", "descripcion": "USO DE SALDO HSBC CASHBACK", "monto": -1004.00, "tarjeta": "adicional ···1207"},
]


def build_movimientos() -> list[Movimiento]:
    out: list[Movimiento] = []
    for row in MOVIMIENTOS_RAW:
        cat, sub, auto_notes = clasificar(row["descripcion"], row["monto"])
        notes = row.get("notas") or auto_notes
        out.append(
            Movimiento(
                fecha_operacion=row["fecha_operacion"],
                fecha_cargo=row["fecha_cargo"],
                descripcion=row["descripcion"],
                monto_mxn=row["monto"],
                tarjeta=row["tarjeta"],
                categoria=cat,
                subcategoria=sub,
                es_abono=row["monto"] < 0,
                notas=notes,
            )
        )
    return out


def resumen_por_categoria(movs: list[Movimiento]) -> dict[str, float]:
    totales: dict[str, float] = defaultdict(float)
    for m in movs:
        if m.es_abono:
            continue
        totales[m.categoria] += m.monto_mxn
    return dict(sorted(totales.items(), key=lambda x: -x[1]))


def main() -> None:
    movs = build_movimientos()
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "periodo": PERIODO,
        "resumen_estado_cuenta": {
            "saldo_deudor_total_mxn": 40181.94,
            "pago_sin_intereses_mxn": 39728.86,
            "pago_minimo_mxn": 595.92,
            "limite_credito_mxn": 42000.00,
            "credito_disponible_mxn": 1818.06,
            "fecha_limite_pago": "2026-10-10",
            "total_cargos_periodo_mxn": 41185.94,
            "total_abonos_periodo_mxn": 29940.94,
        },
        "movimientos": [asdict(m) for m in movs],
        "totales_por_categoria_mxn": resumen_por_categoria(movs),
    }

    (DATA_DIR / "movimientos.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    with (DATA_DIR / "movimientos.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "fecha_operacion",
                "fecha_cargo",
                "descripcion",
                "monto_mxn",
                "tarjeta",
                "categoria",
                "subcategoria",
                "es_abono",
                "notas",
            ],
        )
        w.writeheader()
        for m in movs:
            w.writerow(asdict(m))

    gastos = sum(m.monto_mxn for m in movs if not m.es_abono)
    abonos = sum(-m.monto_mxn for m in movs if m.es_abono)
    print(f"Movimientos: {len(movs)} | Gastos: ${gastos:,.2f} | Abonos: ${abonos:,.2f}")


if __name__ == "__main__":
    main()
