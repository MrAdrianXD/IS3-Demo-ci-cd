"""
Tests unitarios para la clase Liquidacion.
Validan cada método de cálculo de forma aislada.
"""

import pytest
from app.liquidacion import Liquidacion


@pytest.fixture
def liquidacion():
    """Instancia de Liquidacion con valores por defecto."""
    return Liquidacion()


class TestSueldoBasico:
    def test_calcula_basico_correctamente(self, liquidacion):
        # 40 hs * 55000 = 2.200.000
        assert liquidacion.calcular_sueldo_basico(40) == 2_200_000

    def test_basico_con_cero_horas(self, liquidacion):
        assert liquidacion.calcular_sueldo_basico(0) == 0

    def test_basico_acepta_horas_como_string_numerico(self, liquidacion):
        # La implementación castea con int(), debe soportar strings numéricos
        assert liquidacion.calcular_sueldo_basico("10") == 550_000


class TestSueldoBruto:
    def test_antiguedad_menor_a_5_anios(self, liquidacion):
        # basico=1000, bonificacion 8% = 80, antiguedad <5 => +10% = 100
        # bruto = 1000 + 80 + 100 = 1180
        assert liquidacion.calcular_sueldo_bruto(1000, 3) == 1180

    def test_antiguedad_entre_5_y_10_anios(self, liquidacion):
        # bruto = 1000 + 80 + 200 (20%) = 1280
        assert liquidacion.calcular_sueldo_bruto(1000, 7) == 1280

    def test_antiguedad_entre_10_y_20_anios(self, liquidacion):
        # bruto = 1000 + 80 + 300 (30%) = 1380
        assert liquidacion.calcular_sueldo_bruto(1000, 15) == 1380

    def test_antiguedad_20_anios_o_mas(self, liquidacion):
        # bruto = 1000 + 80 + 400 (40%) = 1480
        assert liquidacion.calcular_sueldo_bruto(1000, 20) == 1480

    def test_limite_exacto_5_anios_usa_tramo_siguiente(self, liquidacion):
        # antiguedad=5 no es < 5, entra en el tramo "< 10" (20%)
        assert liquidacion.calcular_sueldo_bruto(1000, 5) == 1280


class TestSueldoNeto:
    def test_calcula_neto_correctamente(self, liquidacion):
        # bruto=1000, retenciones 11% = 110, obra social 3% = 30
        # neto = 1000 - 110 - 30 = 860
        assert liquidacion.calcular_sueldo_neto(1000) == 860

    def test_neto_con_bruto_cero(self, liquidacion):
        assert liquidacion.calcular_sueldo_neto(0) == 0


class TestSueldoEmpleadoEndToEnd:
    def test_calculo_completo_empleado_junior(self, liquidacion):
        # 40 hs, 2 años de antigüedad
        # basico = 40 * 55000 = 2.200.000
        # bruto = 2.200.000 + 8% + 10% = 2.200.000 * 1.18 = 2.596.000
        # neto = 2.596.000 * (1 - 0.11 - 0.03) = 2.596.000 * 0.86 = 2.232.560
        resultado = liquidacion.calcular_sueldo_empleado(40, 2)
        assert resultado == 2_232_560.0

    def test_calculo_completo_empleado_senior(self, liquidacion):
        resultado = liquidacion.calcular_sueldo_empleado(45, 22)
        basico = 45 * 55000
        bruto = basico * 1.08 + basico * 0.4
        neto = round(bruto - bruto * 0.11 - bruto * 0.03, 2)
        assert resultado == neto

    def test_calculo_con_parametros_personalizados(self):
        liq_custom = Liquidacion(
            p_valor_hora=1000,
            p_pct_bonificacion=10,
            p_pct_retenciones=15,
            p_pct_obra_social=5,
        )
        resultado = liq_custom.calcular_sueldo_empleado(10, 1)
        # basico = 10000, bruto = 10000*1.10 + 10000*0.1 = 12000
        # neto = 12000 * (1 - 0.15 - 0.05) = 12000 * 0.8 = 9600
        assert resultado == 9600.0
