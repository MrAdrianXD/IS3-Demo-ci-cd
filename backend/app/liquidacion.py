#########################################################################
# Script: liquidacion.py
# Descripción: Clase para realizar liquidación de sueldos de empleados,
#   con métodos para calcular sueldo básico, bruto y neto.
# Objetivo: Revisar generación de tests unitarios y de integración para
#   validar la funcionalidad de la clase.
###########################################################################

"""
    Script con una clase para realizar liquidación de sueldos
    para implementar tests unitarios y de integración
"""

class Liquidacion():
    """ Clase para realizar liquidación de sueldos de empleados,
        con métodos para calcular sueldo básico, bruto y neto.
    """

    def __init__(self,
                    p_valor_hora = 55000,
                    p_pct_bonificacion = 8,
                    p_pct_retenciones = 11,
                    p_pct_obra_social = 3):
        self.valor_hora = p_valor_hora
        self.pct_bonificacion = p_pct_bonificacion
        self.pct_retenciones = p_pct_retenciones
        self.pct_obraSocial = p_pct_obra_social


    def calcular_sueldo_basico(self, hs_trabajadas: int) -> float:
        """ Básico = horas trabajadas * valor hora
            Se toma el valor de cantidad de horas semanales

        Args:
            hs_trabajadas (int): cantidad de horas trabajadas

        Returns:
            float: sueldo básico calculado
        """
        basico = int(hs_trabajadas) * self.valor_hora
        return round(basico,2)


    def calcular_sueldo_bruto(self, basico: float, antiguedad: int) -> float:
        """ Bruto = basico + bonificaciones + antiguedad

        Args:
            basico (float): sueldo básico
            antiguedad (int): años de antigüedad

        Returns:
            float: sueldo bruto calculado
        """

        basico = float(basico)
        bruto = basico + (basico * (self.pct_bonificacion * 0.01))
        if (antiguedad < 5):
            bruto = bruto + (basico * 0.1) # 10%
        elif (antiguedad < 10):
            bruto = bruto + (basico * 0.2) # 20%
        elif (antiguedad < 20):
            bruto = bruto + (basico * 0.3) # 30%
        else:
            bruto = bruto + (basico * 0.4) # 40%
        return round(bruto,2)


    def calcular_sueldo_neto(self, bruto: float) -> float:
        """ Neto = bruto - retenciones - obra social

        Args:
            bruto (float): sueldo bruto

        Returns:
            float: sueldo neto calculado
        """
        # Neto = bruto - retenciones - obra social
        neto = bruto - (bruto * (self.pct_retenciones * 0.01)) - (bruto * (self.pct_obraSocial * 0.01))
        return round(neto,2)


    def calcular_sueldo_empleado(self, cant_hs_trabajadas: int, antiguedad_empleado: int) -> float:
        """ Función que calcula el sueldo neto a pagar a un empleado,
            a partir de la cantidad de horas trabajadas y su antigüedad.

        Args:
            cant_hs_trabajadas (int): cantidad de horas trabajadas
            antiguedad_empleado (int): años de antigüedad del empleado

        Returns:
            float: sueldo neto calculado
        """
        sueldo_basico = self.calcular_sueldo_basico(cant_hs_trabajadas)
        sueldo_bruto = self.calcular_sueldo_bruto(sueldo_basico, antiguedad_empleado)
        sueldo_neto = self.calcular_sueldo_neto(sueldo_bruto)
        return round(sueldo_neto,2)
