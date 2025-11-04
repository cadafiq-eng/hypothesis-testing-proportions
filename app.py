"""
Calculadora Web para Pruebas de Hipótesis en Muestras Pequeñas
Interfaz gráfica con Streamlit

Para ejecutar:
    streamlit run app.py
"""

import streamlit as st
import numpy as np
import pandas as pd
from hypothesis_test_proportions import PruebasProporcionesComparacion
import io
import sys

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Hipótesis - Proporciones",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📊 Calculadora de Pruebas de Hipótesis")
st.subheader("Comparación de Proporciones en Muestras Pequeñas")

st.markdown("""
Esta calculadora implementa métodos robustos para análisis estadístico de proporciones,
especialmente diseñados para **muestras pequeñas** (n < 40).
""")

# Barra lateral con información
with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    **Métodos disponibles:**
    - ✓ Prueba Exacta de Fisher
    - ✓ Prueba de Chi-cuadrado
    - ✓ IC Agresti-Coull
    - ✓ IC Agresti-Caffo
    
    **Ideal para:**
    - Ensayos clínicos pequeños
    - Estudios piloto
    - Experimentos con pocos participantes
    """)
    
    st.markdown("---")
    st.markdown("**Nivel de significancia (α)**")
    alpha = st.selectbox(
        "Selecciona α:",
        [0.01, 0.05, 0.10],
        index=1,
        help="Probabilidad de error tipo I"
    )

# Tabs principales
tab1, tab2, tab3 = st.tabs(["📥 Ingresar Datos", "📊 Resultados", "📖 Ayuda"])

with tab1:
    st.header("Ingreso de Datos")
    
    # Selector de tipo de tabla
    tipo_tabla = st.radio(
        "Tipo de tabla:",
        ["Tabla 2×2 (Dos grupos, dos categorías)", 
         "Tabla personalizada (Cualquier tamaño)"],
        help="Las tablas 2×2 tienen más métodos disponibles"
    )
    
    if tipo_tabla == "Tabla 2×2 (Dos grupos, dos categorías)":
        st.markdown("### Tabla 2×2")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Nombres de grupos:**")
            grupo1 = st.text_input("Grupo 1:", value="Grupo Control", key="g1")
            grupo2 = st.text_input("Grupo 2:", value="Grupo Tratamiento", key="g2")
        
        with col2:
            st.markdown("**Nombres de categorías:**")
            cat1 = st.text_input("Categoría 1:", value="Éxito", key="c1")
            cat2 = st.text_input("Categoría 2:", value="Fallo", key="c2")
        
        st.markdown("### Frecuencias observadas:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**{grupo1}**")
            g1_c1 = st.number_input(f"{cat1}:", min_value=0, value=10, step=1, key="g1c1")
            g1_c2 = st.number_input(f"{cat2}:", min_value=0, value=5, step=1, key="g1c2")
            st.info(f"Total: {g1_c1 + g1_c2}")
        
        with col2:
            st.markdown(f"**{grupo2}**")
            g2_c1 = st.number_input(f"{cat1}:", min_value=0, value=3, step=1, key="g2c1")
            g2_c2 = st.number_input(f"{cat2}:", min_value=0, value=12, step=1, key="g2c2")
            st.info(f"Total: {g2_c1 + g2_c2}")
        
        # Crear tabla
        tabla = np.array([[g1_c1, g1_c2], [g2_c1, g2_c2]])
        nombres_grupos = [grupo1, grupo2]
        nombres_categorias = [cat1, cat2]
        
    else:  # Tabla personalizada
        st.markdown("### Tabla personalizada")
        
        col1, col2 = st.columns(2)
        with col1:
            n_grupos = st.number_input("Número de grupos (filas):", min_value=2, max_value=10, value=3, step=1)
        with col2:
            n_categorias = st.number_input("Número de categorías (columnas):", min_value=2, max_value=10, value=3, step=1)
        
        # Nombres de grupos
        st.markdown("**Nombres de grupos:**")
        cols = st.columns(min(n_grupos, 4))
        nombres_grupos = []
        for i in range(n_grupos):
            with cols[i % 4]:
                nombre = st.text_input(f"Grupo {i+1}:", value=f"Grupo {i+1}", key=f"ng{i}")
                nombres_grupos.append(nombre)
        
        # Nombres de categorías
        st.markdown("**Nombres de categorías:**")
        cols = st.columns(min(n_categorias, 4))
        nombres_categorias = []
        for i in range(n_categorias):
            with cols[i % 4]:
                nombre = st.text_input(f"Categoría {i+1}:", value=f"Cat {i+1}", key=f"nc{i}")
                nombres_categorias.append(nombre)
        
        # Ingresar datos en tabla
        st.markdown("### Frecuencias observadas:")
        
        tabla_data = []
        for i in range(n_grupos):
            st.markdown(f"**{nombres_grupos[i]}**")
            cols = st.columns(n_categorias)
            fila = []
            for j in range(n_categorias):
                with cols[j]:
                    valor = st.number_input(
                        f"{nombres_categorias[j]}:",
                        min_value=0,
                        value=10,
                        step=1,
                        key=f"v{i}{j}"
                    )
                    fila.append(valor)
            tabla_data.append(fila)
        
        tabla = np.array(tabla_data)
    
    # Botón para calcular
    st.markdown("---")
    calcular = st.button("🔍 Calcular Análisis", type="primary", use_container_width=True)

with tab2:
    st.header("Resultados del Análisis")
    
    if 'calcular' in locals() and calcular:
        # Crear objeto de prueba
        prueba = PruebasProporcionesComparacion(
            tabla,
            nombres_grupos=nombres_grupos,
            nombres_categorias=nombres_categorias,
            alpha=alpha
        )
        
        # Capturar output para mostrar
        old_stdout = sys.stdout
        sys.stdout = resultado_buffer = io.StringIO()
        
        try:
            # Mostrar tabla
            st.subheader("📋 Tabla de Contingencia")
            df = pd.DataFrame(
                tabla, 
                index=nombres_grupos,
                columns=nombres_categorias
            )
            df['Total'] = df.sum(axis=1)
            totales = df.sum()
            totales.name = 'Total'
            df = pd.concat([df, totales.to_frame().T])
            st.dataframe(df, use_container_width=True)
            
            # Tabs para diferentes análisis
            if tabla.shape == (2, 2):
                subtab1, subtab2, subtab3, subtab4 = st.tabs([
                    "🎯 Fisher Exacta", 
                    "📊 Chi-cuadrado", 
                    "📏 Intervalos IC",
                    "🔄 Comparación"
                ])
                
                with subtab1:
                    st.subheader("Prueba Exacta de Fisher")
                    resultado_fisher = prueba.prueba_fisher_exacta()
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Odds Ratio", f"{resultado_fisher['odds_ratio']:.4f}")
                    with col2:
                        st.metric("Valor p", f"{resultado_fisher['p_value']:.4f}")
                    with col3:
                        decision = "Rechazar H₀" if resultado_fisher['rechazo_h0'] else "No rechazar H₀"
                        st.metric("Decisión", decision)
                    
                    if resultado_fisher['rechazo_h0']:
                        st.success(f"✓ Se rechaza H₀ (p < {alpha}): Existe diferencia significativa")
                    else:
                        st.info(f"✗ No se rechaza H₀ (p ≥ {alpha}): No hay evidencia de diferencia")
                
                with subtab2:
                    st.subheader("Prueba de Chi-cuadrado")
                    resultado_chi2 = prueba.prueba_chi_cuadrado()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("χ²", f"{resultado_chi2['chi2']:.4f}")
                    with col2:
                        st.metric("gl", f"{resultado_chi2['df']}")
                    with col3:
                        st.metric("Valor p", f"{resultado_chi2['p_value']:.4f}")
                    with col4:
                        supuestos = "✓ OK" if resultado_chi2['supuestos_ok'] else "⚠ Revisar"
                        st.metric("Supuestos", supuestos)
                    
                    if resultado_chi2['rechazo_h0']:
                        st.success(f"✓ Se rechaza H₀ (p < {alpha}): Variables asociadas")
                    else:
                        st.info(f"✗ No se rechaza H₀ (p ≥ {alpha}): No hay evidencia de asociación")
                    
                    if not resultado_chi2['supuestos_ok']:
                        st.warning("⚠ Más del 20% de celdas con frecuencia esperada < 5. Se recomienda usar Fisher.")
                
                with subtab3:
                    st.subheader("Intervalos de Confianza")
                    
                    # Agresti-Caffo para diferencia
                    st.markdown("**Diferencia de Proporciones (Agresti-Caffo)**")
                    resultado_diff = prueba.intervalo_agresti_caffo_diferencia()
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(f"Proporción {nombres_grupos[0]}", f"{resultado_diff['p1_obs']:.4f}")
                        st.metric(f"Proporción {nombres_grupos[1]}", f"{resultado_diff['p2_obs']:.4f}")
                    with col2:
                        st.metric("Diferencia observada", f"{resultado_diff['diff_obs']:.4f}")
                        st.metric(f"IC {(1-alpha)*100:.0f}%", 
                                f"[{resultado_diff['ic_lower']:.4f}, {resultado_diff['ic_upper']:.4f}]")
                    
                    if not resultado_diff['incluye_cero']:
                        st.success("✓ El IC no incluye 0: Diferencia significativa")
                    else:
                        st.info("✗ El IC incluye 0: No hay diferencia significativa")
                    
                    # Agresti-Coull individual
                    st.markdown("---")
                    st.markdown("**Proporciones Individuales (Agresti-Coull)**")
                    for i in range(2):
                        with st.expander(f"📊 {nombres_grupos[i]}"):
                            resultado_ic = prueba.intervalo_agresti_coull(grupo=i, categoria_exito=0)
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Proporción observada", f"{resultado_ic['p_observada']:.4f}")
                            with col2:
                                st.metric(f"IC {(1-alpha)*100:.0f}%",
                                        f"[{resultado_ic['ic_lower']:.4f}, {resultado_ic['ic_upper']:.4f}]")
                
                with subtab4:
                    st.subheader("Comparación de Métodos")
                    
                    comparacion = pd.DataFrame({
                        'Método': ['Fisher Exacta', 'Chi-cuadrado'],
                        'Valor p': [resultado_fisher['p_value'], resultado_chi2['p_value']],
                        'Decisión': [
                            'Rechazar H₀' if resultado_fisher['rechazo_h0'] else 'No rechazar H₀',
                            'Rechazar H₀' if resultado_chi2['rechazo_h0'] else 'No rechazar H₀'
                        ]
                    })
                    st.dataframe(comparacion, use_container_width=True)
                    
                    total = tabla.sum()
                    if total < 20:
                        st.success("✓ **Recomendación**: Usar prueba exacta de Fisher (muestra pequeña)")
                    else:
                        st.info("ℹ️ **Recomendación**: Ambos métodos son válidos (muestra adecuada)")
            
            else:  # Tabla mayor a 2x2
                st.subheader("📊 Prueba de Chi-cuadrado")
                resultado_chi2 = prueba.prueba_chi_cuadrado()
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("χ²", f"{resultado_chi2['chi2']:.4f}")
                with col2:
                    st.metric("gl", f"{resultado_chi2['df']}")
                with col3:
                    st.metric("Valor p", f"{resultado_chi2['p_value']:.4f}")
                with col4:
                    supuestos = "✓ OK" if resultado_chi2['supuestos_ok'] else "⚠ Revisar"
                    st.metric("Supuestos", supuestos)
                
                if resultado_chi2['rechazo_h0']:
                    st.success(f"✓ Se rechaza H₀ (p < {alpha}): Variables asociadas")
                else:
                    st.info(f"✗ No se rechaza H₀ (p ≥ {alpha}): No hay evidencia de asociación")
                
                # Intervalos individuales
                st.markdown("---")
                st.subheader("📏 Intervalos de Confianza Individuales (Agresti-Coull)")
                
                for i in range(len(nombres_grupos)):
                    with st.expander(f"📊 {nombres_grupos[i]}"):
                        resultado_ic = prueba.intervalo_agresti_coull(grupo=i, categoria_exito=0)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Proporción observada", f"{resultado_ic['p_observada']:.4f}")
                        with col2:
                            st.metric(f"IC {(1-alpha)*100:.0f}%",
                                    f"[{resultado_ic['ic_lower']:.4f}, {resultado_ic['ic_upper']:.4f}]")
            
            # Descargar reporte
            st.markdown("---")
            st.subheader("📥 Descargar Reporte")
            
            # Generar reporte en texto
            reporte = f"""
REPORTE DE ANÁLISIS ESTADÍSTICO
================================

Nivel de significancia: {alpha}
Tabla de contingencia: {tabla.shape[0]} × {tabla.shape[1]}

TABLA DE DATOS
{df.to_string()}

"""
            if tabla.shape == (2, 2):
                reporte += f"""
PRUEBA EXACTA DE FISHER
-----------------------
Odds Ratio: {resultado_fisher['odds_ratio']:.4f}
Valor p: {resultado_fisher['p_value']:.4f}
Decisión: {"Rechazar H₀" if resultado_fisher['rechazo_h0'] else "No rechazar H₀"}

INTERVALO AGRESTI-CAFFO (Diferencia)
------------------------------------
Diferencia: {resultado_diff['diff_obs']:.4f}
IC {(1-alpha)*100:.0f}%: [{resultado_diff['ic_lower']:.4f}, {resultado_diff['ic_upper']:.4f}]
Incluye cero: {"Sí" if resultado_diff['incluye_cero'] else "No"}
"""
            
            st.download_button(
                label="📄 Descargar reporte (TXT)",
                data=reporte,
                file_name="reporte_analisis.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Error en el análisis: {str(e)}")
        finally:
            sys.stdout = old_stdout
    
    else:
        st.info("👈 Ingresa los datos en la pestaña 'Ingresar Datos' y presiona 'Calcular Análisis'")

with tab3:
    st.header("📖 Guía de Uso")
    
    st.markdown("""
    ### ¿Cómo usar la calculadora?
    
    1. **Selecciona el tipo de tabla**: 2×2 o personalizada
    2. **Ingresa nombres** de grupos y categorías
    3. **Ingresa las frecuencias** observadas
    4. **Ajusta el nivel α** si es necesario (por defecto 0.05)
    5. **Presiona "Calcular"** para ver los resultados
    
    ### ¿Qué método usar?
    
    | Situación | Método recomendado |
    |-----------|-------------------|
    | Tabla 2×2, n < 20 | **Fisher Exacta** |
    | Tabla 2×2, n ≥ 20 | Fisher o Chi-cuadrado |
    | Tabla mayor, frecuencias OK | **Chi-cuadrado** |
    | Intervalo para proporción | **Agresti-Coull** |
    | Diferencia de proporciones | **Agresti-Caffo** |
    
    ### Interpretación de resultados
    
    **Valor p < α**: Se rechaza H₀ → Hay diferencia/asociación significativa
    
    **Valor p ≥ α**: No se rechaza H₀ → No hay evidencia suficiente
    
    **IC no incluye 0**: Diferencia significativa
    
    **IC incluye 0**: No hay diferencia significativa
    
    ### Referencias
    
    - Agresti & Coull (1998) - The American Statistician
    - Agresti & Caffo (2000) - The American Statistician
    
    ### Contacto
    
    Para reportar errores o sugerencias, visita el repositorio en GitHub.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Desarrollado con ❤️ usando Streamlit | Versión 1.0.0</p>
    <p><small>Esta herramienta es para fines educativos y de investigación</small></p>
</div>
""", unsafe_allow_html=True)
