# 📊 Pruebas de Hipótesis para Muestras Pequeñas

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=flat&logo=numpy&logoColor=white)](https://numpy.org/)
[![SciPy](https://img.shields.io/badge/SciPy-%230C55A5.svg?style=flat&logo=scipy&logoColor=white)](https://scipy.org/)

Herramienta en Python para realizar pruebas de hipótesis e intervalos de confianza en **comparación de proporciones**, especialmente diseñada para **muestras pequeñas** donde los métodos tradicionales pueden fallar.

## 🎯 Características Principales

- **Prueba Exacta de Fisher**: Para tablas 2×2, método exacto sin aproximaciones
- **Prueba de Chi-cuadrado**: Para tablas de cualquier dimensión con validación de supuestos
- **Intervalo Agresti-Coull**: Para proporciones individuales (mejor cobertura que métodos clásicos)
- **Intervalo Agresti-Caffo**: Para diferencias de proporciones (robusto en muestras pequeñas)
- **Comparación de métodos**: Recomendaciones automáticas según características de los datos

## 📦 Instalación

### Requisitos previos

- Python 3.8 o superior
- pip

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install numpy scipy pandas
```

## 🚀 Uso Rápido

### Ejemplo básico: Comparación de dos tratamientos

```python
from hypothesis_test_proportions import PruebasProporcionesComparacion

# Tabla 2x2: [éxitos, fallos] para cada grupo
tabla = [
    [12, 8],   # Tratamiento A: 12 éxitos, 8 fallos
    [6, 14]    # Tratamiento B: 6 éxitos, 14 fallos
]

# Crear objeto de prueba
prueba = PruebasProporcionesComparacion(
    tabla,
    nombres_grupos=['Tratamiento A', 'Tratamiento B'],
    nombres_categorias=['Éxito', 'Fallo'],
    alpha=0.05
)

# Realizar análisis completo
prueba.analisis_completo()
```

### Ejemplo: Análisis por partes

```python
# Mostrar tabla
prueba.mostrar_tabla()

# Prueba de Fisher (para tablas 2x2)
resultado_fisher = prueba.prueba_fisher_exacta(alternativa='two-sided')
print(f"Valor p: {resultado_fisher['p_value']:.4f}")

# Prueba de Chi-cuadrado
resultado_chi2 = prueba.prueba_chi_cuadrado()

# Intervalo de confianza para diferencia de proporciones
resultado_ic = prueba.intervalo_agresti_caffo_diferencia()

# Comparar métodos y obtener recomendación
prueba.comparar_metodos()
```

## 📊 Casos de Uso

### 1. Ensayo clínico con muestra pequeña

```python
# Efectividad de vacuna: 30 participantes
tabla_vacuna = [
    [11, 4],   # Vacunados: 11 no enfermaron, 4 enfermaron
    [3, 12]    # Control: 3 no enfermaron, 12 enfermaron
]

prueba = PruebasProporcionesComparacion(
    tabla_vacuna,
    nombres_grupos=['Vacunados', 'Control'],
    nombres_categorias=['Sano', 'Enfermo']
)

prueba.analisis_completo()
```

### 2. Tabla de contingencia más grande

```python
# Satisfacción por plataforma (3 grupos, 3 categorías)
tabla_satisfaccion = [
    [25, 18, 12],  # Web: Satisfecho, Neutral, Insatisfecho
    [30, 15, 8],   # Móvil
    [15, 20, 17]   # Tablet
]

prueba = PruebasProporcionesComparacion(
    tabla_satisfaccion,
    nombres_grupos=['Web', 'Móvil', 'Tablet'],
    nombres_categorias=['Satisfecho', 'Neutral', 'Insatisfecho']
)

# Para tablas mayores a 2x2, solo Chi-cuadrado es aplicable
prueba.prueba_chi_cuadrado()

# Intervalos individuales para cada plataforma
for i in range(3):
    prueba.intervalo_agresti_coull(grupo=i, categoria_exito=0)
```

## 🔍 Métodos Implementados

| Método | Aplicación | Ventaja principal |
|--------|-----------|-------------------|
| **Fisher Exacta** | Tablas 2×2 | Exacto, sin aproximaciones, ideal para n < 20 |
| **Chi-cuadrado** | Cualquier tabla | Flexible, con validación automática de supuestos |
| **Agresti-Coull** | Proporción individual | Mejor cobertura que IC de Wald en muestras pequeñas |
| **Agresti-Caffo** | Diferencia de proporciones | Robusto cuando n₁ o n₂ < 30 |

## 📚 Fundamento Teórico

Los métodos implementados están basados en investigaciones publicadas que demuestran **mejor desempeño que métodos clásicos** en muestras pequeñas:

### Referencias principales:

1. **Agresti, A., & Coull, B. A. (1998)**. "Approximate is better than 'exact' for interval estimation of binomial proportions." *The American Statistician*, 52(2), 119-126.

2. **Agresti, A., & Caffo, B. (2000)**. "Simple and effective confidence intervals for proportions and differences of proportions result from adding two successes and two failures." *The American Statistician*, 54(4), 280-288.

### ¿Por qué estos métodos?

- **Problema con métodos clásicos**: El intervalo de Wald puede tener cobertura real < 95% cuando n < 40
- **Solución Agresti-Coull**: Agrega "observaciones ficticias" para corregir el sesgo
- **Ventaja**: Cobertura más cercana al nivel nominal (95%) incluso con n = 10

## 🧪 Ejemplos Completos

Ver el directorio `examples/` para casos de uso detallados:

- `examples.py`: 4 casos prácticos completos
- `notebook_examples.ipynb`: Tutorial interactivo (próximamente)

## 🛠️ Estructura del Proyecto

```
hypothesis-testing-proportions/
│
├── README.md                          # Este archivo
├── LICENSE                            # Licencia MIT
├── requirements.txt                   # Dependencias
├── .gitignore                         # Archivos ignorados por Git
│
├── hypothesis_test_proportions.py     # Módulo principal
│
├── examples/
│   └── examples.py                    # Ejemplos de uso
│
└── tests/
    └── test_hypothesis.py             # Tests unitarios
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si quieres mejorar este proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

### Ideas para contribuir:

- [ ] Agregar más métodos (prueba de McNemar, exacta de Barnard)
- [ ] Crear visualizaciones de resultados
- [ ] Implementar corrección de Bonferroni para comparaciones múltiples
- [ ] Desarrollar interfaz web con Streamlit
- [ ] Agregar ejemplos con datos reales

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 👤 Autor

**Tu Nombre**
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu.email@ejemplo.com

## 📧 Contacto y Soporte

Si tienes preguntas o encuentras algún problema:

- Abre un [Issue](https://github.com/tu-usuario/hypothesis-testing-proportions/issues)
- Envía un correo a: tu.email@ejemplo.com

## ⭐ ¿Te resultó útil?

Si este proyecto te ayudó en tu investigación o análisis, considera:

- Darle una ⭐ en GitHub
- Citarlo en tu trabajo académico
- Compartirlo con colegas que trabajen con muestras pequeñas

---

**Nota**: Esta herramienta es para fines educativos y de investigación. Para decisiones críticas en salud o regulatorias, consulta con un estadístico profesional.
