# Documentación Técnica - Calculadora Matemática Avanzada

## Arquitectura del Sistema

### 1. Componentes Principales

#### 1.1 Backend (APP.py)
- **Framework**: Flask 3.1.0
- **Procesamiento Matemático**: SymPy 1.13.3
- **Servidor Web**: Gunicorn 23.0.0 (producción)

#### 1.2 Frontend
- **Templates**: Jinja2 3.1.6
- **Interfaz**: HTML5, CSS3, JavaScript
- **Estilos**: Bootstrap (incluido en templates)

### 2. Estructura de Datos

#### 2.1 Procesamiento de Expresiones
```python
# Variables simbólicas
x = symbols('x')  # Variable principal para cálculos

# Estructura de entrada
{
    'funcion': str,  # Expresión matemática en formato string
    'limites': tuple,  # (a, b) para integrales definidas
    'punto': float,  # Para límites y series
    'orden': int  # Para series de Taylor
}
```

#### 2.2 Formato de Respuesta
```python
{
    'resultado': str,  # Resultado formateado
    'error': str,  # Mensaje de error si existe
    'unidad': str  # Unidad de medida (u², u³)
}
```

### 3. Funciones Principales

#### 3.1 Preprocesamiento de Expresiones
```python
def preprocess_expression(expr_str):
    """
    Preprocesa expresiones matemáticas para hacerlas compatibles con SymPy.
    - Convierte superíndices a potencias
    - Maneja multiplicación implícita
    - Procesa funciones trigonométricas
    """
```

#### 3.2 Cálculos Matemáticos
```python
# Derivadas
def calcular_derivada(funcion_str):
    """
    Calcula la derivada de una función.
    Entrada: string con la función
    Salida: string con la derivada
    """

# Integrales
def calcular_integral(funcion_str, a=None, b=None):
    """
    Calcula integral definida o indefinida.
    Entrada: función y límites opcionales
    Salida: resultado numérico o expresión
    """

# Áreas
def calcular_area(funcion1_str, funcion2_str, a, b):
    """
    Calcula el área entre dos curvas.
    Entrada: dos funciones y límites
    Salida: área en unidades cuadradas
    """
```

### 4. Manejo de Errores

#### 4.1 Tipos de Errores
1. **Errores de Sintaxis**
   - Expresiones matemáticas mal formadas
   - Caracteres no válidos
   - Paréntesis desbalanceados

2. **Errores de Cálculo**
   - División por cero
   - Límites no existentes
   - Integrales divergentes

3. **Errores de Entrada**
   - Valores fuera de rango
   - Tipos de datos incorrectos
   - Campos requeridos vacíos

#### 4.2 Sistema de Logging
```python
# Implementación de logging
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 5. Seguridad

#### 5.1 Validación de Entrada
- Sanitización de expresiones matemáticas
- Validación de tipos de datos
- Límites en el tamaño de entrada

#### 5.2 Protección contra Ataques
- CSRF protection (Flask-WTF)
- Rate limiting
- Validación de sesiones

### 6. Rendimiento

#### 6.1 Optimizaciones
- Caché de resultados comunes
- Procesamiento asíncrono de cálculos largos
- Compresión de respuestas HTTP

#### 6.2 Límites
- Tiempo máximo de cálculo: 30 segundos
- Tamaño máximo de matriz: 10x10
- Orden máximo de series: 20

### 7. Pruebas

#### 7.1 Pruebas Unitarias
```python
# test_math_operations.py
def test_derivada():
    assert calcular_derivada("x^2") == "2*x"

def test_integral():
    assert calcular_integral("2*x", 0, 1) == 1.0
```

#### 7.2 Pruebas de Integración
```python
# test_integration.py
def test_calculadora_completa():
    # Prueba el flujo completo de la aplicación
    pass
```

### 8. Despliegue

#### 8.1 Requisitos de Sistema
- Python 3.8+
- 1GB RAM mínimo
- 1 CPU core mínimo

#### 8.2 Configuración de Producción
```python
# config.py
class ProductionConfig:
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'your-secret-key'
    SERVER_NAME = 'your-domain.com'
```

### 9. Mantenimiento

#### 9.1 Monitoreo
- Logs de aplicación
- Métricas de rendimiento
- Alertas de error

#### 9.2 Actualizaciones
- Proceso de actualización de dependencias
- Versionado semántico
- Plan de respaldo

### 10. API Endpoints

#### 10.1 Rutas Principales
```
GET  /              # Página principal
POST /derivar       # Cálculo de derivadas
POST /integrar      # Cálculo de integrales
POST /area          # Cálculo de áreas
POST /volumen       # Cálculo de volúmenes
POST /limites       # Cálculo de límites
POST /series        # Cálculo de series
POST /matriz        # Cálculo de determinantes
```

### 11. Dependencias

#### 11.1 Principales
- Flask==3.1.0
- SymPy==1.13.3
- Gunicorn==23.0.0

#### 11.2 Desarrollo
- pytest
- black
- flake8
- mypy

### 12. Convenciones de Código

#### 12.1 Estilo
- PEP 8
- Docstrings en formato Google
- Nombres descriptivos

#### 12.2 Estructura
- Módulos separados por funcionalidad
- Tests en directorio separado
- Documentación en /docs 