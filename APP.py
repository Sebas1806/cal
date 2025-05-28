from flask import Flask, render_template, request, jsonify
from sympy import symbols, diff, integrate, sympify, Abs, solve, Matrix, sin, cos, tan, exp, log, sqrt
import re

app = Flask(__name__)

# Definir la variable simbólica
x = symbols('x')

def preprocess_expression(expr_str):
    """Función para preprocesar la expresión matemática y hacerla más intuitiva."""
    # Reemplazar superíndices numéricos por potencias
    expr_str = re.sub(r'(\d+)²', r'\1^2', expr_str)
    expr_str = re.sub(r'(\d+)³', r'\1^3', expr_str)
    expr_str = re.sub(r'(\d+)⁴', r'\1^4', expr_str)
    expr_str = re.sub(r'(\d+)⁵', r'\1^5', expr_str)
    expr_str = re.sub(r'(\d+)⁶', r'\1^6', expr_str)
    expr_str = re.sub(r'(\d+)⁷', r'\1^7', expr_str)
    expr_str = re.sub(r'(\d+)⁸', r'\1^8', expr_str)
    expr_str = re.sub(r'(\d+)⁹', r'\1^9', expr_str)
    
    # Reemplazar multiplicación implícita (2x -> 2*x)
    expr_str = re.sub(r'(\d+)x', r'\1*x', expr_str)
    expr_str = re.sub(r'x(\d+)', r'x*\1', expr_str)
    expr_str = re.sub(r'\)(\d+)', r')*\1', expr_str)
    expr_str = re.sub(r'(\d+)\(', r'\1*(', expr_str)
    expr_str = re.sub(r'\)x', r')*x', expr_str)
    expr_str = re.sub(r'x\(', r'x*(', expr_str)
    
    # Reemplazar funciones trigonométricas con multiplicación implícita
    expr_str = re.sub(r'(\d+)sin', r'\1*sin', expr_str)
    expr_str = re.sub(r'(\d+)cos', r'\1*cos', expr_str)
    expr_str = re.sub(r'(\d+)tan', r'\1*tan', expr_str)
    expr_str = re.sub(r'(\d+)ln', r'\1*ln', expr_str)
    expr_str = re.sub(r'(\d+)exp', r'\1*exp', expr_str)
    expr_str = re.sub(r'(\d+)sqrt', r'\1*sqrt', expr_str)
    
    return expr_str

def format_result(result):
    """Función para formatear el resultado y reemplazar ** por ^."""
    return str(result).replace('**', '^')

def format_integral_result(result):
    """Función para formatear el resultado de integrales definidas."""
    return f"{result:.4f} u²"

def format_volume_result(result):
    """Función para formatear el resultado de volumen de sólido de revolución."""
    return f"{result:.4f} u³"

def format_area_result(result):
    """Función para formatear el resultado del área entre curvas."""
    return f"{abs(result):.4f} u²"

def safe_sympify(expr_str):
    """Función segura para convertir string a expresión simbólica."""
    try:
        # Preprocesar la expresión
        expr_str = preprocess_expression(expr_str)
        # Reemplazar ^ por ** para potencias
        expr_str = expr_str.replace('^', '**')
        return sympify(expr_str)
    except Exception as e:
        raise ValueError(f"Error al procesar la expresión: {str(e)}")

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado_derivada = ""
    resultado_integral = ""
    resultado_decimal_area = 0.0
    resultado_volumen = ""
    unidad_area = "u²"
    resultado_limites = ""
    resultado_series = ""
    resultado_matriz = ""

    if request.method == 'POST':
        try:
            if 'derivar' in request.form:
                funcion_str = request.form['funcion_derivada']
                funcion = safe_sympify(funcion_str)
                derivada = diff(funcion, x)
                resultado_derivada = f"<b>Derivada:</b> {format_result(derivada)}"

            elif 'integrar' in request.form:
                funcion_str = request.form['funcion_integral']
                a = request.form.get('a_integral', None)
                b = request.form.get('b_integral', None)
                funcion = safe_sympify(funcion_str)

                if a is None or b is None or a == '' or b == '':
                    # Integral indefinida
                    integral = integrate(funcion, x)
                    resultado_integral = f"<b>Integral Indefinida:</b> {format_result(integral)} + C"
                else:
                    # Integral definida
                    a = float(a)
                    b = float(b)
                    integral_definida = integrate(funcion, (x, a, b))
                    resultado_integral = f"<b>Integral Definida:</b> {format_integral_result(integral_definida.evalf())}"

            elif 'area' in request.form:
                funcion1_str = request.form['funcion1_area']
                funcion2_str = request.form['funcion2']
                a = float(request.form['a'])
                b = float(request.form['b'])
                funcion1 = safe_sympify(funcion1_str)
                funcion2 = safe_sympify(funcion2_str)

                # Calcular el área entre las curvas
                area = integrate(Abs(funcion1 - funcion2), (x, a, b))
                resultado_decimal_area = format_area_result(area.evalf())

            elif 'volumen' in request.form:
                funcion_str = request.form['funcion1_volumen']
                a = float(request.form['a_volumen'])
                b = float(request.form['b_volumen'])
                funcion = safe_sympify(funcion_str)

                # Calcular el volumen de revolución usando el método de discos
                volumen = integrate(funcion**2, (x, a, b)) * 3.14159  # π * ∫[a, b] f(x)^2 dx
                resultado_volumen = format_volume_result(volumen.evalf())

            elif 'limites' in request.form:
                funcion_str = request.form['funcion_limites']
                punto = float(request.form['punto'])
                funcion = safe_sympify(funcion_str)
                
                # Calcular límite por la izquierda y derecha
                limite_izq = funcion.subs(x, punto - 0.0001).evalf()
                limite_der = funcion.subs(x, punto + 0.0001).evalf()
                
                if abs(limite_izq - limite_der) < 0.0001:
                    resultado_limites = f"<b>Límite en x = {punto}:</b> {format_result(limite_izq)}"
                else:
                    resultado_limites = f"<b>El límite no existe en x = {punto}</b>"

            elif 'series' in request.form:
                funcion_str = request.form['funcion_series']
                punto = float(request.form['punto_series'])
                orden = int(request.form['orden_series'])
                funcion = safe_sympify(funcion_str)
                
                # Calcular serie de Taylor
                serie = funcion.series(x, punto, orden).removeO()
                resultado_series = f"<b>Serie de Taylor:</b> {format_result(serie)}"

            elif 'matriz' in request.form:
                matriz_str = request.form['matriz']
                # Convertir string de matriz a matriz de SymPy
                filas = matriz_str.strip().split('\n')
                matriz = []
                for fila in filas:
                    elementos = [safe_sympify(elem.strip()) for elem in fila.split(',')]
                    matriz.append(elementos)
                
                M = Matrix(matriz)
                det = M.det()
                resultado_matriz = f"<b>Determinante:</b> {format_result(det)}"

        except Exception as e:
            error_message = str(e)
            return render_template('index.html', 
                                error=error_message,
                                resultado_derivada=resultado_derivada,
                                resultado_integral=resultado_integral,
                                resultado_decimal_area=resultado_decimal_area,
                                resultado_volumen=resultado_volumen,
                                unidad_area=unidad_area,
                                resultado_limites=resultado_limites,
                                resultado_series=resultado_series,
                                resultado_matriz=resultado_matriz)

    return render_template('index.html', 
                         resultado_derivada=resultado_derivada,
                         resultado_integral=resultado_integral,
                         resultado_decimal_area=resultado_decimal_area,
                         resultado_volumen=resultado_volumen,
                         unidad_area=unidad_area,
                         resultado_limites=resultado_limites,
                         resultado_series=resultado_series,
                         resultado_matriz=resultado_matriz)

if __name__ == '__main__':
    app.run(debug=True) 
