"""
Ejemplos de uso de la librería de pruebas de hipótesis
para comparación de proporciones en muestras pequeñas.

Este archivo contiene 4 casos prácticos que demuestran
el uso de los diferentes métodos implementados.
"""

import sys
sys.path.append('..')  # Para importar desde el directorio raíz

from hypothesis_test_proportions import PruebasProporcionesComparacion


def ejemplo_1_vacuna():
    """
    Ejemplo 1: Efectividad de Vacuna en Ensayo Clínico
    
    Contexto: Se realiza un ensayo clínico con 30 participantes
    para probar una nueva vacuna contra la gripe.
    """
    print("\n" + "#"*60)
    print("# EJEMPLO 1: Efectividad de Vacuna en Ensayo Clínico")
    print("#"*60)
    print("Contexto: Se realiza un ensayo clínico con 30 participantes")
    print("para probar una nueva vacuna contra la gripe.")
    print()
    
    # Tabla 2x2: Grupo Control vs Vacunado
    tabla_vacuna = [
        [3, 12],  # Grupo control: 3 no enfermaron, 12 enfermaron
        [11, 4]   # Grupo vacunado: 11 no enfermaron, 4 enfermaron
    ]
    
    prueba = PruebasProporcionesComparacion(
        tabla_vacuna,
        nombres_grupos=['Grupo Control', 'Grupo Vacunado'],
        nombres_categorias=['No enfermó', 'Enfermó'],
        alpha=0.05
    )
    
    # Análisis completo
    prueba.mostrar_tabla()
    prueba.prueba_fisher_exacta(alternativa='two-sided')
    prueba.prueba_chi_cuadrado()
    prueba.intervalo_agresti_coull(grupo=0, categoria_exito=0)
    prueba.intervalo_agresti_coull(grupo=1, categoria_exito=0)
    prueba.intervalo_agresti_caffo_diferencia()
    prueba.comparar_metodos()


def ejemplo_2_satisfaccion():
    """
    Ejemplo 2: Satisfacción del Cliente por Plataforma
    
    Contexto: Una empresa analiza la satisfacción de clientes
    según la plataforma utilizada (Web, Móvil, Tablet).
    """
    print("\n" + "#"*60)
    print("# EJEMPLO 2: Satisfacción del Cliente por Plataforma")
    print("#"*60)
    print("Contexto: Una empresa analiza la satisfacción de clientes")
    print("según la plataforma utilizada (Web, Móvil, Tablet).")
    print()
    
    # Tabla 3x3: Plataforma vs Nivel de Satisfacción
    tabla_satisfaccion = [
        [25, 18, 12],  # Web: Satisfecho, Neutral, Insatisfecho
        [30, 15, 8],   # Móvil: Satisfecho, Neutral, Insatisfecho
        [15, 20, 17]   # Tablet: Satisfecho, Neutral, Insatisfecho
    ]
    
    prueba = PruebasProporcionesComparacion(
        tabla_satisfaccion,
        nombres_grupos=['Web', 'Móvil', 'Tablet'],
        nombres_categorias=['Satisfecho', 'Neutral', 'Insatisfecho'],
        alpha=0.05
    )
    
    prueba.mostrar_tabla()
    fisher_result = prueba.prueba_fisher_exacta()  # No aplicará
    if not fisher_result['aplicable']:
        print(f"ℹ️  {fisher_result['mensaje']}")
    
    prueba.prueba_chi_cuadrado()
    
    # Intervalos para proporción de "Satisfecho" en cada plataforma
    print("\n--- Intervalos de Confianza para Proporción 'Satisfecho' ---")
    for i in range(3):
        prueba.intervalo_agresti_coull(grupo=i, categoria_exito=0)


def ejemplo_3_germinacion():
    """
    Ejemplo 3: Éxito en Germinación de Semillas
    
    Contexto: Se compara la germinación de semillas con dos
    tratamientos diferentes en condiciones controladas.
    """
    print("\n" + "#"*60)
    print("# EJEMPLO 3: Éxito en Germinación de Semillas")
    print("#"*60)
    print("Contexto: Se compara la germinación de semillas con dos")
    print("tratamientos diferentes en condiciones controladas.")
    print()
    
    # Tabla 2x2: Tratamiento A vs B
    tabla_semillas = [
        [6, 9],   # Tratamiento A: 6 germinaron, 9 no germinaron
        [12, 8]   # Tratamiento B: 12 germinaron, 8 no germinaron
    ]
    
    prueba = PruebasProporcionesComparacion(
        tabla_semillas,
        nombres_grupos=['Tratamiento A', 'Tratamiento B'],
        nombres_categorias=['Germinó', 'No germinó'],
        alpha=0.05
    )
    
    prueba.mostrar_tabla()
    prueba.prueba_fisher_exacta(alternativa='less')  # ¿A < B?
    prueba.prueba_chi_cuadrado()
    prueba.intervalo_agresti_caffo_diferencia()
    prueba.comparar_metodos()


def ejemplo_4_turnos():
    """
    Ejemplo 4: Preferencia de Turno Laboral por Edad
    
    Contexto: Una empresa estudia si la preferencia de turno
    laboral está relacionada con el rango de edad.
    """
    print("\n" + "#"*60)
    print("# EJEMPLO 4: Preferencia de Turno Laboral por Edad")
    print("#"*60)
    print("Contexto: Una empresa estudia si la preferencia de turno")
    print("laboral está relacionada con el rango de edad.")
    print()
    
    # Tabla 4x3: Grupo de edad vs Turno preferido
    tabla_turnos = [
        [32, 18, 10],  # 18-30 años: Mañana, Tarde, Noche
        [45, 25, 15],  # 31-45 años: Mañana, Tarde, Noche
        [38, 30, 12],  # 46-60 años: Mañana, Tarde, Noche
        [22, 15, 8]    # 60+ años: Mañana, Tarde, Noche
    ]
    
    prueba = PruebasProporcionesComparacion(
        tabla_turnos,
        nombres_grupos=['18-30 años', '31-45 años', '46-60 años', '60+ años'],
        nombres_categorias=['Mañana', 'Tarde', 'Noche'],
        alpha=0.05
    )
    
    prueba.mostrar_tabla()
    prueba.prueba_chi_cuadrado()


def main():
    """
    Función principal que ejecuta todos los ejemplos
    """
    print("\n" + "="*70)
    print(" "*15 + "EJEMPLOS DE USO DE LA LIBRERÍA")
    print(" "*10 + "Pruebas de Hipótesis para Muestras Pequeñas")
    print("="*70)
    
    # Ejecutar todos los ejemplos
    ejemplo_1_vacuna()
    ejemplo_2_satisfaccion()
    ejemplo_3_germinacion()
    ejemplo_4_turnos()
    
    # Información final
    print("\n" + "#"*60)
    print("# FIN DE LOS EJEMPLOS")
    print("#"*60)
    print("\nPara más información sobre los métodos:")
    print("- Agresti, A., & Coull, B. A. (1998). Approximate is better than 'exact'")
    print("  for interval estimation of binomial proportions. The American Statistician.")
    print("- Agresti, A., & Caffo, B. (2000). Simple and effective confidence intervals")
    print("  for proportions and differences of proportions result from adding two")
    print("  successes and two failures. The American Statistician.")
    print("\n" + "="*70)


if __name__ == "__main__":
    main()
