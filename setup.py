"""
Setup script para instalar el paquete hypothesis_test_proportions
"""

from setuptools import setup, find_packages

# Leer el contenido del README para la descripción larga
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Leer los requisitos desde requirements.txt
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="hypothesis-test-proportions",
    version="1.0.0",
    author="Tu Nombre",
    author_email="tu.email@ejemplo.com",
    description="Herramienta para pruebas de hipótesis e intervalos de confianza en muestras pequeñas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tu-usuario/hypothesis-testing-proportions",
    project_urls={
        "Bug Tracker": "https://github.com/tu-usuario/hypothesis-testing-proportions/issues",
        "Documentation": "https://github.com/tu-usuario/hypothesis-testing-proportions/blob/main/README.md",
        "Source Code": "https://github.com/tu-usuario/hypothesis-testing-proportions",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    py_modules=["hypothesis_test_proportions"],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "examples": [
            "jupyter>=1.0.0",
            "matplotlib>=3.4.0",
            "seaborn>=0.11.0",
        ],
    },
    keywords=[
        "statistics",
        "hypothesis testing",
        "proportions",
        "small samples",
        "fisher exact test",
        "chi-square",
        "agresti-coull",
        "agresti-caffo",
        "confidence intervals",
    ],
    include_package_data=True,
    zip_safe=False,
)
