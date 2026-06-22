"""
Tests de integración para la API de liquidación.
Usan TestClient de FastAPI para probar los endpoints end-to-end
(request HTTP -> lógica de Liquidacion -> response HTTP).
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestEndpointsBasicos:
    def test_root_responde_ok(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestEndpointLiquidacion:
    def test_calculo_exitoso(self):
        payload = {"horas_trabajadas": 40, "antiguedad": 2}
        response = client.post("/api/liquidacion", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["horas_trabajadas"] == 40
        assert data["antiguedad"] == 2
        assert data["sueldo_basico"] == 2_200_000
        assert data["sueldo_neto"] == 2_232_560.0

    def test_calculo_con_cero_horas(self):
        payload = {"horas_trabajadas": 0, "antiguedad": 0}
        response = client.post("/api/liquidacion", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert data["sueldo_basico"] == 0
        assert data["sueldo_neto"] == 0

    def test_horas_negativas_devuelve_error_validacion(self):
        payload = {"horas_trabajadas": -5, "antiguedad": 2}
        response = client.post("/api/liquidacion", json=payload)
        assert response.status_code == 422  # error de validación de Pydantic

    def test_antiguedad_negativa_devuelve_error_validacion(self):
        payload = {"horas_trabajadas": 40, "antiguedad": -1}
        response = client.post("/api/liquidacion", json=payload)
        assert response.status_code == 422

    def test_falta_campo_requerido(self):
        payload = {"horas_trabajadas": 40}
        response = client.post("/api/liquidacion", json=payload)
        assert response.status_code == 422

    def test_tipo_de_dato_invalido(self):
        payload = {"horas_trabajadas": "cuarenta", "antiguedad": 2}
        response = client.post("/api/liquidacion", json=payload)
        assert response.status_code == 422

    @pytest.mark.parametrize(
        "horas,antiguedad,neto_esperado",
        [
            (40, 2, 2_232_560.0),
            (0, 0, 0.0),
            (10, 25, None),  # solo valida que no falle, no el valor exacto
        ],
    )
    def test_casos_parametrizados(self, horas, antiguedad, neto_esperado):
        payload = {"horas_trabajadas": horas, "antiguedad": antiguedad}
        response = client.post("/api/liquidacion", json=payload)
        assert response.status_code == 200
        if neto_esperado is not None:
            assert response.json()["sueldo_neto"] == neto_esperado
