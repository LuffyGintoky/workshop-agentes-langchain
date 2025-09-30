from typing import List, Literal, Optional
from pydantic import BaseModel, Field

# -------- Tool: calc_costos --------
class CalcCostosInput(BaseModel):
    vuelos: float = Field(..., ge=0, description="Costo de vuelos en moneda base")
    alojamiento: float = Field(..., ge=0, description="Costo total de alojamiento")
    comidas: float = Field(..., ge=0, description="Costo estimado de comidas")
    extras: float = Field(0, ge=0, description="Otros costos (transporte local, entradas, etc.)")
    moneda: str = Field("USD", description="Moneda base, p.ej. USD, EUR, CLP")

def calc_costos(vuelos: float, alojamiento: float, comidas: float, extras: float = 0, moneda: str = "USD") -> str:
    total = float(vuelos) + float(alojamiento) + float(comidas) + float(extras)
    desglose = {
        "vuelos": vuelos,
        "alojamiento": alojamiento,
        "comidas": comidas,
        "extras": extras,
        "total": total,
        "moneda": moneda.upper(),
    }
    return f"Desglose de costos: {desglose}"

# -------- Tool: itinerario_simple --------
class ItinerarioInput(BaseModel):
    destino: str = Field(..., description="Ciudad/país destino, p.ej. 'Lima'")
    dias: int = Field(..., ge=1, le=14, description="Cantidad de días (1-14)")
    interes: Optional[Literal["gastronomia", "historia", "playa", "naturaleza", "mixto"]] = "mixto"

def itinerario_simple(destino: str, dias: int, interes: Optional[str] = "mixto") -> str:
    base = [
        "Llegada, check-in, paseo ligero por el centro",
        "Free tour / principales plazas y museos",
        "Barrio emblemático + mercado local",
        "Actividad temática (gastronomía/historia/playa/naturaleza)",
        "Día libre / compras / miradores",
    ]
    plan = []
    for d in range(1, dias + 1):
        sugerencia = base[(d - 1) % len(base)]
        plan.append(f"Día {d}: {sugerencia}")
    return f"Itinerario sugerido para {destino} ({dias} días, interés: {interes}):\n" + "\n".join(plan)

# -------- Tool: checklist_viaje --------
class ChecklistInput(BaseModel):
    tipo_viaje: Optional[Literal["negocios", "placer", "mixto"]] = "placer"
    documentos: bool = Field(True, description="Incluir recordatorio de documentos")

def checklist_viaje(tipo_viaje: str = "placer", documentos: bool = True) -> str:
    comunes = ["Ropa cómoda", "Calzado", "Cargadores", "Adaptador de enchufe", "Botella reutilizable", "Medicamentos"]
    if documentos:
        comunes = ["Pasaporte/DNI", "Tarjeta de embarque", "Seguro"] + comunes
    extra = {
        "negocios": ["Notebook", "Presentaciones", "Tarjetas de presentación"],
        "placer": ["Gafas de sol", "Bloqueador solar", "Gorra"],
        "mixto": ["Notebook liviano", "Ropa semi-formal"],
    }
    lista = comunes + extra.get(tipo_viaje, [])
    return "Checklist de viaje:\n- " + "\n- ".join(lista)

# -------- Tool: convertir_moneda --------
class ConvertirMonedaInput(BaseModel):
    monto: float = Field(..., ge=0, description="Monto a convertir")
    desde: str = Field(..., description="Moneda origen, p.ej. 'USD'")
    hacia: str = Field(..., description="Moneda destino, p.ej. 'CLP'")
    tasa: Optional[float] = Field(None, ge=0, description="Tasa manual opcional (1 desde = tasa hacia)")

def convertir_moneda(monto: float, desde: str, hacia: str, tasa: Optional[float] = None) -> str:
    desde = desde.upper()
    hacia = hacia.upper()

    # Tasas de ejemplo (⚠️ DEMO, no usar para finanzas reales)
    demo = {
        ("USD", "CLP"): 950.0,
        ("CLP", "USD"): 1/950.0,
        ("USD", "EUR"): 0.9,
        ("EUR", "USD"): 1.1,
    }

    if tasa is None:
        tasa = demo.get((desde, hacia))
        if tasa is None:
            return f"No tengo tasa demo para {desde}->{hacia}. Pasa 'tasa' manual, p.ej. tasa=950."

    convertido = monto * float(tasa)
    return f"{monto:.2f} {desde} ≈ {convertido:.2f} {hacia} (tasa usada: {tasa})"
