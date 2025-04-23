from flask import Flask, render_template, request
from sympy import symbols, diff, integrate, sympify, Abs

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado_derivada = ""
    resultado_integral = ""
    resultado_decimal_area = 0.0
    resultado_volumen = ""
    unidad_area = "u²"

    if request.method == 'POST':
        if 'derivar' in request.form:
            funcion_str = request.form['funcion_derivada']
            funcion = sympify(funcion_str)
            derivada = diff(funcion, x)
            resultado_derivada = f"<b>Derivada:</b> {format_result(derivada)}"

        elif 'integrar' in request.form:
            funcion_str = request.form['funcion_integral']
            a = request.form.get('a_integral', None)
            b = request.form.get('b_integral', None)

            if a is None or b is None or a == '' or b == '':
                # Integral indefinida
                integral = integrate(funcion_str, x)
                resultado_integral = f"<b>Integral Indefinida:</b> {format_result(integral)}"
            else:
                # Integral definida
                a = float(a)
                b = float(b)
                integral_definida = integrate(funcion_str, (x, a, b))
                resultado_integral = f"<b>Integral Definida:</b> {format_integral_result(integral_definida.evalf())}"

        elif 'area' in request.form:
            funcion1_str = request.form['funcion1_area']
            funcion2_str = request.form['funcion2']
            a = float(request.form['a'])
            b = float(request.form['b'])
            funcion1 = sympify(funcion1_str)
            funcion2 = sympify(funcion2_str)

            # Calcular el área entre las curvas
            area = integrate(Abs(funcion1 - funcion2), (x, a, b))
            resultado_decimal_area = format_area_result(area.evalf())

        elif 'volumen' in request.form:
            funcion_str = request.form['funcion1_volumen']
            a = float(request.form['a_volumen'])
            b = float(request.form['b_volumen'])
            funcion = sympify(funcion_str)

            # Calcular el volumen de revolución usando el método de discos
            volumen = integrate(funcion**2, (x, a, b)) * 3.14159  # π * ∫[a, b] f(x)^2 dx
            resultado_volumen = format_volume_result(volumen.evalf())

    return render_template('index.html', resultado_derivada=resultado_derivada,
                           resultado_integral=resultado_integral,
                           resultado_decimal_area=resultado_decimal_area,
                           resultado_volumen=resultado_volumen,
                           unidad_area=unidad_area)

if __name__ == '__main__':
    app.run(debug=True) 
