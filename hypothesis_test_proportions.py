"""
Tests unitarios para la librería de pruebas de hipótesis
para comparación de proporciones.

Para ejecutar los tests:
    pytest test_hypothesis.py -v
    
Para ejecutar con cobertura:
    pytest test_hypothesis.py --cov=hypothesis_test_proportions --cov-report=html
"""

import pytest
import numpy as np
import sys
sys.path.append('..')

from hypothesis_test_proportions import PruebasProporcionesComparacion


class TestPruebasProporcionesComparacion:
    """Tests para la clase PruebasProporcionesComparacion"""
    
    def test_inicializacion_basica(self):
        """Test de inicialización básica con tabla 2x2"""
        tabla = [[10, 5], [3, 12]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        assert prueba.tabla.shape == (2, 2)
        assert prueba.alpha == 0.05
        assert len(prueba.nombres_grupos) == 2
        assert len(prueba.nombres_categorias) == 2
    
    def test_inicializacion_con_nombres(self):
        """Test de inicialización con nombres personalizados"""
        tabla = [[10, 5], [3, 12]]
        grupos = ['Control', 'Tratamiento']
        categorias = ['Éxito', 'Fallo']
        
        prueba = PruebasProporcionesComparacion(
            tabla,
            nombres_grupos=grupos,
            nombres_categorias=categorias,
            alpha=0.01
        )
        
        assert prueba.nombres_grupos == grupos
        assert prueba.nombres_categorias == categorias
        assert prueba.alpha == 0.01
    
    def test_fisher_tabla_2x2(self):
        """Test de prueba exacta de Fisher con tabla 2x2"""
        tabla = [[10, 5], [3, 12]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.prueba_fisher_exacta()
        
        assert resultado['aplicable'] == True
        assert 'odds_ratio' in resultado
        assert 'p_value' in resultado
        assert 0 <= resultado['p_value'] <= 1
        assert isinstance(resultado['rechazo_h0'], bool)
    
    def test_fisher_tabla_no_2x2(self):
        """Test de Fisher con tabla no 2x2 (debería indicar no aplicable)"""
        tabla = [[10, 5, 3], [3, 12, 8]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.prueba_fisher_exacta()
        
        assert resultado['aplicable'] == False
        assert 'mensaje' in resultado
    
    def test_chi_cuadrado_basico(self):
        """Test básico de prueba de Chi-cuadrado"""
        tabla = [[10, 5], [3, 12]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.prueba_chi_cuadrado()
        
        assert 'chi2' in resultado
        assert 'p_value' in resultado
        assert 'df' in resultado
        assert resultado['df'] == 1  # (2-1) * (2-1) = 1
        assert isinstance(resultado['supuestos_ok'], bool)
    
    def test_chi_cuadrado_tabla_grande(self):
        """Test de Chi-cuadrado con tabla más grande"""
        tabla = [
            [25, 18, 12],
            [30, 15, 8],
            [15, 20, 17]
        ]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.prueba_chi_cuadrado()
        
        assert resultado['df'] == 4  # (3-1) * (3-1) = 4
        assert 0 <= resultado['p_value'] <= 1
    
    def test_agresti_coull_basico(self):
        """Test de intervalo Agresti-Coull"""
        tabla = [[10, 5], [3, 12]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.intervalo_agresti_coull(grupo=0, categoria_exito=0)
        
        assert 'p_observada' in resultado
        assert 'p_ajustada' in resultado
        assert 'ic_lower' in resultado
        assert 'ic_upper' in resultado
        assert 0 <= resultado['ic_lower'] <= 1
        assert 0 <= resultado['ic_upper'] <= 1
        assert resultado['ic_lower'] <= resultado['ic_upper']
    
    def test_agresti_coull_limites(self):
        """Test de que los límites del IC estén en [0, 1]"""
        tabla = [[15, 0], [0, 15]]  # Casos extremos
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.intervalo_agresti_coull(grupo=0, categoria_exito=0)
        
        assert 0 <= resultado['ic_lower'] <= 1
        assert 0 <= resultado['ic_upper'] <= 1
    
    def test_agresti_caffo_2x2(self):
        """Test de intervalo Agresti-Caffo para diferencia"""
        tabla = [[10, 5], [3, 12]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.intervalo_agresti_caffo_diferencia()
        
        assert resultado is not None
        assert 'p1_obs' in resultado
        assert 'p2_obs' in resultado
        assert 'diff_obs' in resultado
        assert 'ic_lower' in resultado
        assert 'ic_upper' in resultado
        assert isinstance(resultado['incluye_cero'], bool)
    
    def test_agresti_caffo_no_2x2(self):
        """Test de Agresti-Caffo con tabla no 2x2 (debería retornar None)"""
        tabla = [[10, 5, 3], [3, 12, 8]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.intervalo_agresti_caffo_diferencia()
        
        assert resultado is None
    
    def test_proporciones_calculadas(self):
        """Test de que las proporciones se calculen correctamente"""
        tabla = [[12, 8], [6, 14]]  # 60% vs 30%
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.prueba_fisher_exacta()
        
        assert abs(resultado['p1'] - 0.6) < 0.001
        assert abs(resultado['p2'] - 0.3) < 0.001
    
    def test_nivel_significancia_personalizado(self):
        """Test con nivel de significancia personalizado"""
        tabla = [[10, 5], [3, 12]]
        prueba = PruebasProporcionesComparacion(tabla, alpha=0.01)
        
        assert prueba.alpha == 0.01
        
        resultado = prueba.prueba_fisher_exacta()
        # La decisión de rechazo debería usar alpha=0.01
        assert resultado['rechazo_h0'] == (resultado['p_value'] < 0.01)
    
    def test_tabla_numpy_array(self):
        """Test de que funcione con numpy array como input"""
        tabla = np.array([[10, 5], [3, 12]])
        prueba = PruebasProporcionesComparacion(tabla)
        
        assert isinstance(prueba.tabla, np.ndarray)
        assert prueba.tabla.shape == (2, 2)
    
    def test_chi_cuadrado_validacion_supuestos(self):
        """Test de validación de supuestos en Chi-cuadrado"""
        # Tabla con frecuencias muy pequeñas
        tabla = [[2, 1], [1, 2]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.prueba_chi_cuadrado()
        
        # Con estas frecuencias, es probable que no se cumplan los supuestos
        assert 'supuestos_ok' in resultado
        assert 'celdas_bajas' in resultado


class TestCasosEspeciales:
    """Tests para casos especiales y edge cases"""
    
    def test_tabla_con_ceros(self):
        """Test con tabla que contiene ceros"""
        tabla = [[10, 0], [0, 10]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        # Fisher debería manejar esto correctamente
        resultado = prueba.prueba_fisher_exacta()
        assert resultado['aplicable'] == True
        
    def test_tabla_identica(self):
        """Test con tabla donde todos los valores son iguales"""
        tabla = [[5, 5], [5, 5]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        resultado = prueba.prueba_fisher_exacta()
        # p-value debería ser alto (no hay diferencia)
        assert resultado['p_value'] > 0.5
    
    def test_muestra_muy_pequeña(self):
        """Test con muestra muy pequeña (n < 10)"""
        tabla = [[2, 3], [1, 4]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        # Debería ejecutarse sin errores
        resultado_fisher = prueba.prueba_fisher_exacta()
        resultado_chi2 = prueba.prueba_chi_cuadrado()
        
        assert resultado_fisher['aplicable'] == True
        assert resultado_chi2['chi2'] >= 0


class TestIntegracion:
    """Tests de integración que prueban múltiples métodos juntos"""
    
    def test_analisis_completo_2x2(self):
        """Test de análisis completo con tabla 2x2"""
        tabla = [[10, 5], [3, 12]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        # Debería ejecutarse sin errores
        prueba.analisis_completo()
    
    def test_comparacion_consistencia(self):
        """Test de que Fisher y Chi-cuadrado den resultados consistentes"""
        # Con muestra grande, ambos deberían dar resultados similares
        tabla = [[50, 30], [20, 60]]
        prueba = PruebasProporcionesComparacion(tabla)
        
        fisher_result = prueba.prueba_fisher_exacta()
        chi2_result = prueba.prueba_chi_cuadrado()
        
        # Los p-values deberían ser similares (no idénticos)
        # pero al menos la decisión debería ser la misma
        assert fisher_result['rechazo_h0'] == chi2_result['rechazo_h0']


# Fixtures para pytest
@pytest.fixture
def tabla_2x2_basica():
    """Fixture con tabla 2x2 básica"""
    return [[10, 5], [3, 12]]


@pytest.fixture
def tabla_3x3_basica():
    """Fixture con tabla 3x3 básica"""
    return [
        [25, 18, 12],
        [30, 15, 8],
        [15, 20, 17]
    ]


@pytest.fixture
def prueba_basica(tabla_2x2_basica):
    """Fixture con objeto de prueba básico"""
    return PruebasProporcionesComparacion(tabla_2x2_basica)


# Tests parametrizados
@pytest.mark.parametrize("alpha,esperado", [
    (0.05, 0.05),
    (0.01, 0.01),
    (0.10, 0.10),
])
def test_diferentes_alphas(alpha, esperado):
    """Test con diferentes niveles de significancia"""
    tabla = [[10, 5], [3, 12]]
    prueba = PruebasProporcionesComparacion(tabla, alpha=alpha)
    assert prueba.alpha == esperado


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
