# Calculadora Matemática Avanzada

## Descripción
Esta aplicación web proporciona una interfaz intuitiva para realizar diversos cálculos matemáticos avanzados, incluyendo:
- Derivadas
- Integrales (definidas e indefinidas)
- Cálculo de áreas entre curvas
- Volúmenes de sólidos de revolución
- Límites
- Series de Taylor
- Determinantes de matrices

## Requisitos del Sistema
- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación
1. Clonar el repositorio:
```bash
git clone [URL_DEL_REPOSITORIO]
cd MODEL
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución
1. Activar el entorno virtual (si no está activado)
2. Ejecutar la aplicación:
```bash
python APP.py
```
3. Abrir un navegador y acceder a `http://localhost:5000`

## Estructura del Proyecto
```
MODEL/
├── APP.py              # Aplicación principal
├── requirements.txt    # Dependencias del proyecto
├── Procfile           # Configuración para despliegue
├── static/            # Archivos estáticos (CSS, JS)
└── templates/         # Plantillas HTML
    └── index.html     # Interfaz principal
```

## Características Principales
1. **Derivadas**
   - Soporte para funciones polinómicas, trigonométricas y exponenciales
   - Formato intuitivo de entrada

2. **Integrales**
   - Cálculo de integrales definidas e indefinidas
   - Soporte para límites de integración personalizados

3. **Áreas entre Curvas**
   - Cálculo preciso del área entre dos funciones
   - Visualización de resultados en unidades cuadradas

4. **Volúmenes de Revolución**
   - Cálculo de volúmenes usando el método de discos
   - Resultados en unidades cúbicas

5. **Límites**
   - Cálculo de límites laterales
   - Detección de discontinuidades

6. **Series de Taylor**
   - Expansión de funciones en series de Taylor
   - Control del orden de la serie

7. **Matrices**
   - Cálculo de determinantes
   - Soporte para matrices de cualquier dimensión

## Tecnologías Utilizadas
- **Backend**: Flask (Python)
- **Procesamiento Matemático**: SymPy
- **Frontend**: HTML, CSS, JavaScript
- **Despliegue**: Gunicorn

## Contribución
1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto
[TU_NOMBRE] - [TU_EMAIL]

## Agradecimientos
- SymPy por su potente biblioteca de matemáticas simbólicas
- Flask por su framework web ligero y flexible
- La comunidad de código abierto por sus contribuciones
