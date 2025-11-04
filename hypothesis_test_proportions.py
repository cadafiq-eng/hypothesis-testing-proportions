"""
Herramienta para pruebas de hipótesis e intervalos de confianza
en comparación de proporciones para muestras pequeñas.

Implementa métodos robustos específicamente diseñados para muestras pequeñas:
- Prueba exacta de Fisher
- Prueba de Chi-cuadrado
- Intervalo de confianza Agresti-Coull
- Intervalo de confianza Agresti-Caffo

Autor: Tu Nombre
Versión: 1.0.0
Licencia: MIT
"""

import numpy as np
from scipy import stats
from scipy.stats import chi2_contingency, fisher_exact
import pandas as pd

__version__ = "1.0.0"


class PruebasProporcionesComparacion:
    """
    Clase para realizar pruebas de hipótesis e intervalos de confianza 
    para comparación de proporciones en muestras pequeñas
    
    Métodos implementados:
    - Prueba exacta de Fisher (tablas 2x2)
    - Prueba de Chi-cuadrado (cualquier tabla)
    - Intervalo de confianza Agresti-Coull (proporciones individuales)
    - Intervalo de confianza Agresti-Caffo (diferencia de proporciones)
    
    Referencias:
    -----------
    - Agresti, A., & Coull, B. A. (1998). Approximate is better than 'exact'
      for interval estimation of binomial proportions. The American Statistician.
    - Agresti, A., & Caffo, B. (2000). Simple and effective confidence intervals
      for proportions and differences of proportions result from adding two
      successes and two failures. The American Statistician.
    """
    
    def __init__(self, tabla_contingencia, nombres_grupos=None, nombres_categorias=None, alpha=0.05):
        """
        Inicializa con una tabla de contingencia
        
        Parámetros:
        -----------
        tabla_contingencia : array-like
            Tabla de contingencia (puede ser 2x2 o mayor)
        nombres_grupos : list, opcional
            Nombres de los grupos (filas)
        nombres_categorias : list, opcional
            Nombres de las categorías (columnas)
        alpha : float
            Nivel de significancia (por defecto 0.05)
            
        Ejemplos:
        ---------
        >>> tabla = [[10, 5], [3, 12]]
        >>> prueba = PruebasProporcionesComparacion(tabla)
        >>> resultado = prueba.prueba_fisher_exacta()
        """
        self.tabla = np.array(tabla_contingencia)
        self.alpha = alpha
        self.nombres_grupos = nombres_grupos or [f"Grupo {i+1}" for i in range(self.tabla.shape[0])]
        self.nombres_categorias = nombres_categorias or [f"Categoría {i+1}" for i in range(self.tabla.shape[1])]
        
    def mostrar_tabla(self):
        """Muestra la tabla de contingencia de forma elegante"""
        df = pd.DataFrame(
            self.tabla, 
            index=self.nombres_grupos,
            columns=self.nombres_categorias
        )
        df['Total'] = df.sum(axis=1)
        df.loc['Total'] = df.sum()
        
        print("\n" + "="*60)
        print("TABLA DE CONTINGENCIA")
        print("="*60)
        print(df)
        print("="*60 + "\n")
        
    def prueba_fisher_exacta(self, alternativa='two-sided'):
        """
        Realiza la prueba exacta de Fisher (solo para tablas 2x2)
        
        Parámetros:
        -----------
        alternativa : str
            'two-sided', 'less', 'greater'
            
        Retorna:
        --------
        dict : Diccionario con resultados de la prueba
        
        Ejemplos:
        ---------
        >>> resultado = prueba.prueba_fisher_exacta(alternativa='two-sided')
        >>> print(resultado['p_value'])
        """
        if self.tabla.shape != (2, 2):
            return {
                'aplicable': False,
                'mensaje': 'La prueba exacta de Fisher solo es aplicable a tablas 2x2'
            }
        
        odds_ratio, p_value = fisher_exact(self.tabla, alternative=alternativa)
        
        # Calcular proporciones
        p1 = self.tabla[0, 0] / self.tabla[0].sum()
        p2 = self.tabla[1, 0] / self.tabla[1].sum()
        
        print("\n" + "="*60)
        print("PRUEBA EXACTA DE FISHER")
        print("="*60)
        print(f"Hipótesis nula (H₀): Las proporciones son iguales")
        print(f"Hipótesis alternativa (H₁): {alternativa}")
        print(f"\nProporción {self.nombres_grupos[0]}: {p1:.4f} ({self.tabla[0,0]}/{self.tabla[0].sum()})")
        print(f"Proporción {self.nombres_grupos[1]}: {p2:.4f} ({self.tabla[1,0]}/{self.tabla[1].sum()})")
        print(f"\nOdds Ratio: {odds_ratio:.4f}")
        print(f"Valor p: {p_value:.4f}")
        print(f"Nivel de significancia: {self.alpha}")
        
        if p_value < self.alpha:
            print(f"\n✓ CONCLUSIÓN: Se RECHAZA H₀ (p={p_value:.4f} < {self.alpha})")
            print("  Existe evidencia significativa de diferencia entre proporciones")
        else:
            print(f"\n✗ CONCLUSIÓN: NO se rechaza H₀ (p={p_value:.4f} >= {self.alpha})")
            print("  No hay evidencia suficiente de diferencia entre proporciones")
        
        print("="*60 + "\n")
        
        return {
            'aplicable': True,
            'odds_ratio': odds_ratio,
            'p_value': p_value,
            'p1': p1,
            'p2': p2,
            'rechazo_h0': p_value < self.alpha
        }
    
    def prueba_chi_cuadrado(self):
        """
        Realiza la prueba de Chi-cuadrado de independencia
        
        Retorna:
        --------
        dict : Diccionario con resultados de la prueba
        
        Notas:
        ------
        Se recomienda que al menos el 80% de las celdas tengan frecuencia esperada >= 5
        """
        chi2, p_value, df, expected = chi2_contingency(self.tabla)
        
        # Verificar condición de frecuencias esperadas >= 5
        celdas_bajas = np.sum(expected < 5)
        total_celdas = expected.size
        porcentaje_bajas = (celdas_bajas / total_celdas) * 100
        
        print("\n" + "="*60)
        print("PRUEBA DE CHI-CUADRADO")
        print("="*60)
        print(f"Hipótesis nula (H₀): Las variables son independientes")
        print(f"Hipótesis alternativa (H₁): Las variables están asociadas")
        print(f"\nEstadístico χ²: {chi2:.4f}")
        print(f"Grados de libertad: {df} = ({self.tabla.shape[0]}-1) × ({self.tabla.shape[1]}-1)")
        print(f"Valor p: {p_value:.4f}")
        print(f"Nivel de significancia: {self.alpha}")
        
        print(f"\n--- Frecuencias Esperadas ---")
        df_expected = pd.DataFrame(
            expected, 
            index=self.nombres_grupos,
            columns=self.nombres_categorias
        )
        print(df_expected.round(2))
        
        print(f"\n--- Validación de Supuestos ---")
        print(f"Celdas con frecuencia esperada < 5: {celdas_bajas}/{total_celdas} ({porcentaje_bajas:.1f}%)")
        
        if porcentaje_bajas > 20:
            print("⚠ ADVERTENCIA: Más del 20% de celdas tienen frecuencia esperada < 5")
            print("  La prueba de Chi-cuadrado puede no ser apropiada.")
            print("  Considere usar la prueba exacta de Fisher (si es 2x2)")
        else:
            print("✓ Condición de frecuencias esperadas satisfecha")
        
        if p_value < self.alpha:
            print(f"\n✓ CONCLUSIÓN: Se RECHAZA H₀ (p={p_value:.4f} < {self.alpha})")
            print("  Existe evidencia significativa de asociación entre variables")
        else:
            print(f"\n✗ CONCLUSIÓN: NO se rechaza H₀ (p={p_value:.4f} >= {self.alpha})")
            print("  No hay evidencia suficiente de asociación entre variables")
        
        print("="*60 + "\n")
        
        return {
            'chi2': chi2,
            'p_value': p_value,
            'df': df,
            'expected': expected,
            'celdas_bajas': celdas_bajas,
            'rechazo_h0': p_value < self.alpha,
            'supuestos_ok': porcentaje_bajas <= 20
        }
    
    def intervalo_agresti_coull(self, grupo=0, categoria_exito=0):
        """
        Calcula el intervalo de confianza Agresti-Coull para una proporción
        (método ajustado recomendado para muestras pequeñas)
        
        Parámetros:
        -----------
        grupo : int
            Índice del grupo (fila)
        categoria_exito : int
            Índice de la categoría considerada como "éxito" (columna)
            
        Retorna:
        --------
        dict : Diccionario con resultados del intervalo
        
        Referencias:
        ------------
        Agresti, A., & Coull, B. A. (1998). The American Statistician.
        """
        x = self.tabla[grupo, categoria_exito]  # Número de éxitos
        n = self.tabla[grupo].sum()  # Tamaño de muestra
        
        # Valor crítico para el nivel de confianza
        z = stats.norm.ppf(1 - self.alpha/2)
        
        # Método Agresti-Coull (agregar z²/2 éxitos y z² observaciones)
        n_tilde = n + z**2
        p_tilde = (x + z**2/2) / n_tilde
        
        # Error estándar ajustado
        se = np.sqrt(p_tilde * (1 - p_tilde) / n_tilde)
        
        # Intervalo de confianza
        ic_lower = p_tilde - z * se
        ic_upper = p_tilde + z * se
        
        # Asegurar que esté en [0, 1]
        ic_lower = max(0, ic_lower)
        ic_upper = min(1, ic_upper)
        
        # Proporción observada (sin ajuste)
        p_obs = x / n
        
        print("\n" + "="*60)
        print("INTERVALO DE CONFIANZA AGRESTI-COULL")
        print("="*60)
        print(f"Grupo: {self.nombres_grupos[grupo]}")
        print(f"Categoría: {self.nombres_categorias[categoria_exito]}")
        print(f"Nivel de confianza: {(1-self.alpha)*100:.0f}%")
        print(f"\nDatos observados:")
        print(f"  Éxitos: {x}/{n}")
        print(f"  Proporción observada: {p_obs:.4f}")
        print(f"\nAjuste Agresti-Coull:")
        print(f"  n ajustado (ñ): {n_tilde:.2f}")
        print(f"  p ajustado (p̃): {p_tilde:.4f}")
        print(f"\nIntervalo de Confianza {(1-self.alpha)*100:.0f}%:")
        print(f"  [{ic_lower:.4f}, {ic_upper:.4f}]")
        print(f"  ≈ [{ic_lower*100:.2f}%, {ic_upper*100:.2f}%]")
        print("="*60 + "\n")
        
        return {
            'p_observada': p_obs,
            'p_ajustada': p_tilde,
            'ic_lower': ic_lower,
            'ic_upper': ic_upper,
            'n': n,
            'x': x
        }
    
    def intervalo_agresti_caffo_diferencia(self):
        """
        Calcula el intervalo de confianza Agresti-Caffo para la diferencia de proporciones
        (solo para tablas 2x2, método recomendado para muestras pequeñas)
        
        Retorna:
        --------
        dict : Diccionario con resultados del intervalo
        
        Referencias:
        ------------
        Agresti, A., & Caffo, B. (2000). The American Statistician.
        """
        if self.tabla.shape != (2, 2):
            print("El método Agresti-Caffo solo es aplicable a tablas 2x2")
            return None
        
        x1 = self.tabla[0, 0]  # Éxitos grupo 1
        n1 = self.tabla[0].sum()  # Total grupo 1
        x2 = self.tabla[1, 0]  # Éxitos grupo 2
        n2 = self.tabla[1].sum()  # Total grupo 2
        
        # Valor crítico
        z = stats.norm.ppf(1 - self.alpha/2)
        
        # Método Agresti-Caffo: agregar 1 éxito y 1 fallo a cada grupo
        x1_tilde = x1 + 1
        n1_tilde = n1 + 2
        x2_tilde = x2 + 1
        n2_tilde = n2 + 2
        
        # Proporciones ajustadas
        p1_tilde = x1_tilde / n1_tilde
        p2_tilde = x2_tilde / n2_tilde
        
        # Diferencia de proporciones ajustada
        diff = p1_tilde - p2_tilde
        
        # Error estándar
        se = np.sqrt((p1_tilde * (1 - p1_tilde) / n1_tilde) + 
                     (p2_tilde * (1 - p2_tilde) / n2_tilde))
        
        # Intervalo de confianza
        ic_lower = diff - z * se
        ic_upper = diff + z * se
        
        # Proporciones observadas
        p1_obs = x1 / n1
        p2_obs = x2 / n2
        diff_obs = p1_obs - p2_obs
        
        print("\n" + "="*60)
        print("INTERVALO DE CONFIANZA AGRESTI-CAFFO")
        print("PARA DIFERENCIA DE PROPORCIONES")
        print("="*60)
        print(f"Nivel de confianza: {(1-self.alpha)*100:.0f}%")
        print(f"\nDatos observados:")
        print(f"  {self.nombres_grupos[0]}: {x1}/{n1} = {p1_obs:.4f}")
        print(f"  {self.nombres_grupos[1]}: {x2}/{n2} = {p2_obs:.4f}")
        print(f"  Diferencia observada: {diff_obs:.4f}")
        print(f"\nAjuste Agresti-Caffo (+1 éxito, +1 fallo a cada grupo):")
        print(f"  p̃₁: {p1_tilde:.4f}")
        print(f"  p̃₂: {p2_tilde:.4f}")
        print(f"  Diferencia ajustada: {diff:.4f}")
        print(f"\nIntervalo de Confianza {(1-self.alpha)*100:.0f}%:")
        print(f"  [{ic_lower:.4f}, {ic_upper:.4f}]")
        print(f"  ≈ [{ic_lower*100:.2f}%, {ic_upper*100:.2f}%]")
        
        if ic_lower > 0:
            print(f"\n✓ El intervalo NO incluye 0: p₁ > p₂ con {(1-self.alpha)*100:.0f}% de confianza")
        elif ic_upper < 0:
            print(f"\n✓ El intervalo NO incluye 0: p₁ < p₂ con {(1-self.alpha)*100:.0f}% de confianza")
        else:
            print(f"\n✗ El intervalo INCLUYE 0: no hay evidencia suficiente de diferencia")
        
        print("="*60 + "\n")
        
        return {
            'p1_obs': p1_obs,
            'p2_obs': p2_obs,
            'diff_obs': diff_obs,
            'p1_ajustada': p1_tilde,
            'p2_ajustada': p2_tilde,
            'diff_ajustada': diff,
            'ic_lower': ic_lower,
            'ic_upper': ic_upper,
            'incluye_cero': ic_lower <= 0 <= ic_upper
        }
    
    def comparar_metodos(self):
        """
        Compara los resultados de Fisher y Chi-cuadrado (solo para tablas 2x2)
        y proporciona recomendaciones sobre qué método usar
        """
        if self.tabla.shape != (2, 2):
            print("La comparación detallada solo está disponible para tablas 2x2")
            return
        
        print("\n" + "="*60)
        print("COMPARACIÓN DE MÉTODOS")
        print("="*60)
        
        # Fisher
        fisher_result = fisher_exact(self.tabla, alternative='two-sided')
        p_fisher = fisher_result[1]
        
        # Chi-cuadrado
        chi2, p_chi2, df, expected = chi2_contingency(self.tabla)
        
        print(f"\n{'Método':<30} {'Valor p':<15} {'Decisión':<20}")
        print("-" * 65)
        print(f"{'Fisher Exacta':<30} {p_fisher:<15.4f} {'Rechazar H₀' if p_fisher < self.alpha else 'No rechazar H₀'}")
        print(f"{'Chi-cuadrado':<30} {p_chi2:<15.4f} {'Rechazar H₀' if p_chi2 < self.alpha else 'No rechazar H₀'}")
        
        print(f"\n--- Recomendación ---")
        total = self.tabla.sum()
        min_expected = expected.min()
        
        if total < 20 or min_expected < 5:
            print("✓ USAR: Prueba exacta de Fisher")
            print(f"  Razón: Muestra pequeña (n={total}) o frecuencias esperadas < 5")
        else:
            print("✓ USAR: Chi-cuadrado o Fisher (ambos son válidos)")
            print(f"  Razón: Muestra suficientemente grande (n={total})")
        
        print("\n--- Intervalo de Confianza ---")
        print("✓ USAR: Método Agresti-Caffo (recomendado para muestras pequeñas)")
        print("  Este método proporciona mejor cobertura que métodos clásicos")
        
        print("="*60 + "\n")
        
    def analisis_completo(self):
        """
        Realiza un análisis completo con todos los métodos aplicables
        """
        self.mostrar_tabla()
        
        if self.tabla.shape == (2, 2):
            self.prueba_fisher_exacta()
            self.intervalo_agresti_caffo_diferencia()
        
        self.prueba_chi_cuadrado()
        
        if self.tabla.shape == (2, 2):
            self.comparar_metodos()
