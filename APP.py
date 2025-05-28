from flask import Flask, render_template, request, jsonify, send_file
from sympy import symbols, diff, integrate, sympify, Abs, solve, Matrix, sin, cos, tan, exp, log, sqrt, lambdify
from sympy.parsing.sympy_parser import parse_expr
from sympy.parsing.latex import parse_latex
import numpy as np
import matplotlib.pyplot as plt
import io
import base64
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import seaborn as sns

app = Flask(__name__)

# Configurar estilo de las gráficas
plt.style.use('dark_background')
sns.set_palette("husl")

# Definir la variable simbólica
x = symbols('x')

def format_result(result):
    """Función para formatear el resultado y reemplazar ** por ^."""
    return str(result).replace('**', '^')

def format_integral_result(result):
    """Función para formatear el resultado de integrales definidas."""
    return f"{result:.2f} u²"

def format_volume_result(result):
    """Función para formatear el resultado de volumen de sólido de revolución."""
    return f"{result:.2f} m³"

def format_area_result(result):
    """Función para formatear el resultado del área entre curvas."""
    return f"{abs(result):.2f} u²"

def safe_sympify(expr_str):
    """Función segura para convertir string a expresión simbólica."""
    try:
        # Reemplazar ^ por ** para potencias
        expr_str = expr_str.replace('^', '**')
        return sympify(expr_str)
    except Exception as e:
        raise ValueError(f"Error al procesar la expresión: {str(e)}")

def generate_plot(funcion, a=None, b=None, funcion2=None, tipo='integral'):
    """Genera una gráfica de la función y el área bajo la curva."""
    fig = Figure(figsize=(10, 6), dpi=100)
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    
    # Convertir la función simbólica a una función numérica
    f = lambdify(x, funcion, 'numpy')
    
    # Generar puntos para la gráfica
    if a is not None and b is not None:
        x_vals = np.linspace(a, b, 1000)
    else:
        x_vals = np.linspace(-10, 10, 1000)
    
    y_vals = f(x_vals)
    
    # Graficar la función
    ax.plot(x_vals, y_vals, 'b-', linewidth=2, label='f(x)')
    
    if tipo == 'integral' and a is not None and b is not None:
        # Sombrear el área bajo la curva
        ax.fill_between(x_vals, y_vals, alpha=0.3, color='blue')
        ax.axvline(x=a, color='r', linestyle='--', alpha=0.5)
        ax.axvline(x=b, color='r', linestyle='--', alpha=0.5)
        ax.set_title(f'Área bajo la curva desde x={a} hasta x={b}')
    
    elif tipo == 'area' and funcion2 is not None and a is not None and b is not None:
        # Graficar la segunda función
        f2 = lambdify(x, funcion2, 'numpy')
        y2_vals = f2(x_vals)
        ax.plot(x_vals, y2_vals, 'g-', linewidth=2, label='g(x)')
        
        # Sombrear el área entre las curvas
        ax.fill_between(x_vals, y_vals, y2_vals, alpha=0.3, color='purple')
        ax.axvline(x=a, color='r', linestyle='--', alpha=0.5)
        ax.axvline(x=b, color='r', linestyle='--', alpha=0.5)
        ax.set_title('Área entre curvas')
    
    elif tipo == 'volumen' and a is not None and b is not None:
        # Graficar la función y su revolución
        theta = np.linspace(0, 2*np.pi, 100)
        X, Y = np.meshgrid(x_vals, theta)
        Z = f(X)
        
        # Crear una superficie de revolución
        ax.plot_surface(X, Z*np.cos(Y), Z*np.sin(Y), cmap='viridis', alpha=0.8)
        ax.set_title('Volumen de revolución')
    
    # Configurar la gráfica
    ax.grid(True, alpha=0.3)
    ax.axhline(y=0, color='w', linestyle='-', alpha=0.3)
    ax.axvline(x=0, color='w', linestyle='-', alpha=0.3)
    ax.legend()
    
    # Convertir la gráfica a base64
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', facecolor='#1a1a1a')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    
    return img_str

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
    grafica = None

    if request.method == 'POST':
        try:
            if 'derivar' in request.form:
                funcion_str = request.form['funcion_derivada']
                funcion = safe_sympify(funcion_str)
                derivada = diff(funcion, x)
                resultado_derivada = f"<b>Derivada:</b> {format_result(derivada)}"
                grafica = generate_plot(funcion, tipo='derivada')

            elif 'integrar' in request.form:
                funcion_str = request.form['funcion_integral']
                a = request.form.get('a_integral', None)
                b = request.form.get('b_integral', None)
                funcion = safe_sympify(funcion_str)

                if a is None or b is None or a == '' or b == '':
                    # Integral indefinida
                    integral = integrate(funcion, x)
                    resultado_integral = f"<b>Integral Indefinida:</b> {format_result(integral)}"
                    grafica = generate_plot(funcion)
                else:
                    # Integral definida
                    a = float(a)
                    b = float(b)
                    integral_definida = integrate(funcion, (x, a, b))
                    resultado_integral = f"<b>Integral Definida:</b> {format_integral_result(integral_definida.evalf())}"
                    grafica = generate_plot(funcion, a, b, tipo='integral')

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
                grafica = generate_plot(funcion1, a, b, funcion2, tipo='area')

            elif 'volumen' in request.form:
                funcion_str = request.form['funcion1_volumen']
                a = float(request.form['a_volumen'])
                b = float(request.form['b_volumen'])
                funcion = safe_sympify(funcion_str)

                # Calcular el volumen de revolución usando el método de discos
                volumen = integrate(funcion**2, (x, a, b)) * 3.14159  # π * ∫[a, b] f(x)^2 dx
                resultado_volumen = format_volume_result(volumen.evalf())
                grafica = generate_plot(funcion, a, b, tipo='volumen')

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
                grafica = generate_plot(funcion, punto-2, punto+2)

            elif 'series' in request.form:
                funcion_str = request.form['funcion_series']
                punto = float(request.form['punto_series'])
                orden = int(request.form['orden_series'])
                funcion = safe_sympify(funcion_str)
                
                # Calcular serie de Taylor
                serie = funcion.series(x, punto, orden).removeO()
                resultado_series = f"<b>Serie de Taylor:</b> {format_result(serie)}"
                grafica = generate_plot(funcion, punto-2, punto+2)

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
            return render_template('index.html', 
                                error=f"Error en el cálculo: {str(e)}",
                                resultado_derivada=resultado_derivada,
                                resultado_integral=resultado_integral,
                                resultado_decimal_area=resultado_decimal_area,
                                resultado_volumen=resultado_volumen,
                                unidad_area=unidad_area,
                                resultado_limites=resultado_limites,
                                resultado_series=resultado_series,
                                resultado_matriz=resultado_matriz,
                                grafica=grafica)

    return render_template('index.html', 
                         resultado_derivada=resultado_derivada,
                         resultado_integral=resultado_integral,
                         resultado_decimal_area=resultado_decimal_area,
                         resultado_volumen=resultado_volumen,
                         unidad_area=unidad_area,
                         resultado_limites=resultado_limites,
                         resultado_series=resultado_series,
                         resultado_matriz=resultado_matriz,
                         grafica=grafica)

if __name__ == '__main__':
    app.run(debug=True) 
