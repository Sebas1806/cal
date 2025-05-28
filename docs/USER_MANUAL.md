# Manual de Usuario - Calculadora Matemática Avanzada

## Introducción

Bienvenido a la Calculadora Matemática Avanzada. Esta aplicación web le permite realizar diversos cálculos matemáticos de manera intuitiva y precisa. Este manual le guiará a través de todas las funcionalidades disponibles.

## Acceso a la Aplicación

1. Abra su navegador web preferido
2. Ingrese la URL de la aplicación (por defecto: `http://localhost:5000`)
3. La interfaz principal se cargará automáticamente

## Funcionalidades

### 1. Cálculo de Derivadas

#### Procedimiento:
1. En la sección "Derivadas", ingrese la función en el campo de texto
2. Use la siguiente notación:
   - `x^2` para x²
   - `sin(x)` para seno
   - `cos(x)` para coseno
   - `exp(x)` para e^x
   - `log(x)` para ln(x)
3. Haga clic en "Calcular Derivada"
4. El resultado se mostrará debajo del formulario

#### Ejemplos de Entrada:
- `x^2 + 3*x + 2`
- `sin(x) * cos(x)`
- `exp(x) * log(x)`

### 2. Cálculo de Integrales

#### Integrales Indefinidas:
1. En la sección "Integrales", ingrese la función
2. Deje los campos de límites vacíos
3. Haga clic en "Calcular Integral"
4. El resultado incluirá la constante de integración (+C)

#### Integrales Definidas:
1. Ingrese la función
2. Complete los campos "Límite Inferior" y "Límite Superior"
3. Haga clic en "Calcular Integral"
4. El resultado se mostrará en unidades cuadradas (u²)

#### Ejemplos:
- Indefinida: `2*x + 3`
- Definida: `x^2` con límites 0 y 1

### 3. Cálculo de Áreas entre Curvas

#### Procedimiento:
1. En la sección "Áreas", ingrese las dos funciones
2. Especifique los límites de integración
3. Haga clic en "Calcular Área"
4. El resultado se mostrará en unidades cuadradas (u²)

#### Ejemplo:
- Función 1: `x^2`
- Función 2: `x`
- Límites: 0 y 1

### 4. Cálculo de Volúmenes de Revolución

#### Procedimiento:
1. En la sección "Volúmenes", ingrese la función
2. Especifique los límites de integración
3. Haga clic en "Calcular Volumen"
4. El resultado se mostrará en unidades cúbicas (u³)

#### Ejemplo:
- Función: `x^2`
- Límites: 0 y 1

### 5. Cálculo de Límites

#### Procedimiento:
1. En la sección "Límites", ingrese la función
2. Especifique el punto donde desea calcular el límite
3. Haga clic en "Calcular Límite"
4. El resultado mostrará si el límite existe y su valor

#### Ejemplo:
- Función: `(x^2 - 1)/(x - 1)`
- Punto: 1

### 6. Series de Taylor

#### Procedimiento:
1. En la sección "Series", ingrese la función
2. Especifique el punto de expansión
3. Ingrese el orden de la serie
4. Haga clic en "Calcular Serie"
5. El resultado mostrará la expansión en serie

#### Ejemplo:
- Función: `exp(x)`
- Punto: 0
- Orden: 5

### 7. Determinantes de Matrices

#### Procedimiento:
1. En la sección "Matrices", ingrese la matriz
2. Use el formato:
   ```
   1, 2, 3
   4, 5, 6
   7, 8, 9
   ```
3. Haga clic en "Calcular Determinante"
4. El resultado mostrará el valor del determinante

#### Ejemplo:
```
1, 2
3, 4
```

## Consejos de Uso

### Notación Matemática
- Use `*` para multiplicación explícita
- Use `^` para potencias
- Use paréntesis para agrupar expresiones
- Las funciones trigonométricas usan radianes

### Manejo de Errores
- Si recibe un error de sintaxis, verifique la notación
- Para funciones complejas, use paréntesis para claridad
- Asegúrese de que los límites sean números válidos

### Limitaciones
- El orden máximo para series es 20
- Las matrices tienen un tamaño máximo de 10x10
- Los cálculos tienen un tiempo límite de 30 segundos

## Solución de Problemas

### Problemas Comunes

1. **Error de Sintaxis**
   - Verifique que todos los paréntesis estén balanceados
   - Asegúrese de usar la notación correcta
   - Revise que no haya caracteres especiales no válidos

2. **Resultados Inesperados**
   - Verifique los límites de integración
   - Asegúrese de que la función esté bien definida
   - Compruebe las unidades de los resultados

3. **Tiempo de Cálculo Excesivo**
   - Simplifique la expresión si es posible
   - Reduzca el orden de las series
   - Use matrices más pequeñas

### Contacto para Soporte

Si encuentra algún problema no cubierto en este manual, por favor contacte al soporte técnico:
- Email: [EMAIL_SOPORTE]
- Teléfono: [TELEFONO_SOPORTE]
- Horario de atención: [HORARIO_SOPORTE]

## Actualizaciones

Este manual se actualiza periódicamente para reflejar nuevas funcionalidades y mejoras. La versión actual es 1.0.0.

## Glosario

- **Función**: Expresión matemática que relaciona variables
- **Límite**: Valor al que se aproxima una función
- **Integral**: Operación inversa a la derivada
- **Serie**: Suma infinita de términos
- **Matriz**: Arreglo rectangular de números
- **Determinante**: Valor escalar asociado a una matriz cuadrada 