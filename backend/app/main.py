"""
API FastAPI para liquidación de sueldos.
Expone endpoints sobre la clase Liquidacion para que el frontend
pueda calcular el sueldo de un empleado.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import os

from app.liquidacion import Liquidacion

app = FastAPI(
    title="API Liquidación de Sueldos",
    description="Demo de CI/CD - cálculo de liquidación de sueldos de empleados",
    version="1.0.0",
)

# CORS: en la demo se permite todo origen para simplificar.
# En un caso real, restringir a la URL de Netlify.
origins_env = os.getenv("CORS_ORIGINS", "*")
allow_origins = ["*"] if origins_env == "*" else origins_env.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LiquidacionRequest(BaseModel):
    horas_trabajadas: int = Field(..., ge=0, description="Cantidad de horas trabajadas")
    antiguedad: int = Field(..., ge=0, description="Años de antigüedad del empleado")


class LiquidacionResponse(BaseModel):
    horas_trabajadas: int
    antiguedad: int
    sueldo_basico: float
    sueldo_bruto: float
    sueldo_neto: float


@app.get("/")
def read_root():
    return {"status": "ok", "service": "liquidacion-api"}


@app.get("/health")
def health_check():
    """Endpoint de health check, útil para Render y para monitoreo."""
    return {"status": "healthy"}


@app.post("/api/liquidacion", response_model=LiquidacionResponse)
def calcular_liquidacion(payload: LiquidacionRequest):
    """Calcula la liquidación completa (básico, bruto y neto) de un empleado."""
    try:
        liquidacion = Liquidacion()
        sueldo_basico = liquidacion.calcular_sueldo_basico(payload.horas_trabajadas)
        sueldo_bruto = liquidacion.calcular_sueldo_bruto(sueldo_basico, payload.antiguedad)
        sueldo_neto = liquidacion.calcular_sueldo_neto(sueldo_bruto)

        return LiquidacionResponse(
            horas_trabajadas=payload.horas_trabajadas,
            antiguedad=payload.antiguedad,
            sueldo_basico=sueldo_basico,
            sueldo_bruto=sueldo_bruto,
            sueldo_neto=sueldo_neto,
        )
    except (ValueError, TypeError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
