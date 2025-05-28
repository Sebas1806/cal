from flask import Flask, render_template, request, jsonify, session
from sympy import symbols, diff, integrate, sympify, Abs, solve, Matrix, sin, cos, tan, exp, log, sqrt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para las sesiones

# Inicializar el historial en la sesión si no existe
@app.before_request
def initialize_session():
    if 'history' not in session:
        session['history'] = []
    if 'favorites' not in session:
        session['favorites'] = []
    if 'notes' not in session:
        session['notes'] = []

# Función para guardar en el historial
def save_to_history(operation_type, input_data, result):
    history_item = {
        'timestamp': datetime.now().isoformat(),
        'type': operation_type,
        'input': input_data,
        'result': result
    }
    history = session.get('history', [])
    history.insert(0, history_item)  # Añadir al principio
    # Mantener solo los últimos 50 cálculos
    history = history[:50]
    session['history'] = history
    return history_item

# Función para guardar notas
def save_note(operation_id, note):
    notes = session.get('notes', {})
    notes[operation_id] = note
    session['notes'] = notes

# Función para manejar favoritos
def toggle_favorite(operation_id):
    favorites = session.get('favorites', [])
    if operation_id in favorites:
        favorites.remove(operation_id)
    else:
        favorites.append(operation_id)
    session['favorites'] = favorites
    return operation_id in favorites

# Definir la variable simbólica
x = symbols('x')

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
                save_to_history('derivada', {'funcion': funcion_str}, derivada)

            elif 'integrar' in request.form:
                funcion_str = request.form['funcion_integral']
                a = request.form.get('a_integral', None)
                b = request.form.get('b_integral', None)
                funcion = safe_sympify(funcion_str)

                if a is None or b is None or a == '' or b == '':
                    # Integral indefinida
                    integral = integrate(funcion, x)
                    resultado_integral = f"<b>Integral Indefinida:</b> {format_result(integral)} + C"
                    save_to_history('integral', {'funcion': funcion_str, 'tipo': 'indefinida'}, integral)
                else:
                    # Integral definida
                    a = float(a)
                    b = float(b)
                    integral_definida = integrate(funcion, (x, a, b))
                    resultado_integral = f"<b>Integral Definida:</b> {format_integral_result(integral_definida.evalf())}"
                    save_to_history('integral', {'funcion': funcion_str, 'tipo': 'definida', 'a': a, 'b': b}, integral_definida)

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
                save_to_history('area', {'funcion1': funcion1_str, 'funcion2': funcion2_str, 'a': a, 'b': b}, area)

            elif 'volumen' in request.form:
                funcion_str = request.form['funcion1_volumen']
                a = float(request.form['a_volumen'])
                b = float(request.form['b_volumen'])
                funcion = safe_sympify(funcion_str)

                # Calcular el volumen de revolución usando el método de discos
                volumen = integrate(funcion**2, (x, a, b)) * 3.14159  # π * ∫[a, b] f(x)^2 dx
                resultado_volumen = format_volume_result(volumen.evalf())
                save_to_history('volumen', {'funcion': funcion_str, 'a': a, 'b': b}, volumen)

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
                save_to_history('limite', {'funcion': funcion_str, 'punto': punto}, limite_izq)

            elif 'series' in request.form:
                funcion_str = request.form['funcion_series']
                punto = float(request.form['punto_series'])
                orden = int(request.form['orden_series'])
                funcion = safe_sympify(funcion_str)
                
                # Calcular serie de Taylor
                serie = funcion.series(x, punto, orden).removeO()
                resultado_series = f"<b>Serie de Taylor:</b> {format_result(serie)}"
                save_to_history('serie', {'funcion': funcion_str, 'punto': punto, 'orden': orden}, serie)

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
                save_to_history('matriz', {'matriz': matriz_str}, det)

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

@app.route('/calculate', methods=['POST'])
def calculate():
    operation_type = request.form.get('type')
    result = None
    input_data = {}

    try:
        if operation_type == 'derivada':
            funcion = request.form.get('funcion')
            input_data = {'funcion': funcion}
            x = symbols('x')
            derivada = diff(funcion, x)
            result = str(derivada)
            save_to_history('derivada', input_data, result)

        elif operation_type == 'integral':
            funcion = request.form.get('funcion')
            tipo = request.form.get('tipo')
            input_data = {'funcion': funcion, 'tipo': tipo}
            
            x = symbols('x')
            if tipo == 'definida':
                a = float(request.form.get('a'))
                b = float(request.form.get('b'))
                integral = integrate(funcion, (x, a, b))
                result = f"{integral}"
                save_to_history('integral', input_data, result)
            else:
                integral = integrate(funcion, x)
                result = f"{integral} + C"
                save_to_history('integral', input_data, result)

        elif operation_type == 'area':
            funcion1_str = request.form['funcion1_area']
            funcion2_str = request.form['funcion2']
            a = float(request.form['a'])
            b = float(request.form['b'])
            funcion1 = safe_sympify(funcion1_str)
            funcion2 = safe_sympify(funcion2_str)

            # Calcular el área entre las curvas
            area = integrate(Abs(funcion1 - funcion2), (x, a, b))
            result = format_area_result(area.evalf())
            save_to_history('area', {'funcion1': funcion1_str, 'funcion2': funcion2_str, 'a': a, 'b': b}, area)

        elif operation_type == 'volumen':
            funcion_str = request.form['funcion1_volumen']
            a = float(request.form['a_volumen'])
            b = float(request.form['b_volumen'])
            funcion = safe_sympify(funcion_str)

            # Calcular el volumen de revolución usando el método de discos
            volumen = integrate(funcion**2, (x, a, b)) * 3.14159  # π * ∫[a, b] f(x)^2 dx
            result = format_volume_result(volumen.evalf())
            save_to_history('volumen', {'funcion': funcion_str, 'a': a, 'b': b}, volumen)

        elif operation_type == 'limite':
            funcion_str = request.form['funcion_limites']
            punto = float(request.form['punto'])
            funcion = safe_sympify(funcion_str)
            
            # Calcular límite por la izquierda y derecha
            limite_izq = funcion.subs(x, punto - 0.0001).evalf()
            limite_der = funcion.subs(x, punto + 0.0001).evalf()
            
            if abs(limite_izq - limite_der) < 0.0001:
                result = format_result(limite_izq)
                save_to_history('limite', {'funcion': funcion_str, 'punto': punto}, limite_izq)
            else:
                result = "El límite no existe"
                save_to_history('limite', {'funcion': funcion_str, 'punto': punto}, result)

        elif operation_type == 'serie':
            funcion_str = request.form['funcion_series']
            punto = float(request.form['punto_series'])
            orden = int(request.form['orden_series'])
            funcion = safe_sympify(funcion_str)
            
            # Calcular serie de Taylor
            serie = funcion.series(x, punto, orden).removeO()
            result = format_result(serie)
            save_to_history('serie', {'funcion': funcion_str, 'punto': punto, 'orden': orden}, serie)

        elif operation_type == 'matriz':
            matriz_str = request.form['matriz']
            # Convertir string de matriz a matriz de SymPy
            filas = matriz_str.strip().split('\n')
            matriz = []
            for fila in filas:
                elementos = [safe_sympify(elem.strip()) for elem in fila.split(',')]
                matriz.append(elementos)
            
            M = Matrix(matriz)
            det = M.det()
            result = format_result(det)
            save_to_history('matriz', {'matriz': matriz_str}, det)

        return jsonify({
            'success': True,
            'result': result,
            'history_item': save_to_history(operation_type, input_data, result)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify(session.get('history', []))

@app.route('/favorites', methods=['POST'])
def handle_favorites():
    operation_id = request.json.get('operation_id')
    is_favorite = toggle_favorite(operation_id)
    return jsonify({'is_favorite': is_favorite})

@app.route('/notes', methods=['POST'])
def handle_notes():
    operation_id = request.json.get('operation_id')
    note = request.json.get('note')
    save_note(operation_id, note)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True) 
