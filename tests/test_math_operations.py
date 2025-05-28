import pytest
from sympy import symbols, diff, integrate, sympify, Abs, sin, cos, exp, log, Matrix
from APP import preprocess_expression, safe_sympify, format_result

# Configuración de variables simbólicas
x = symbols('x')

class TestMathOperations:
    """Suite de pruebas para operaciones matemáticas."""

    def test_preprocess_expression(self):
        """Prueba el preprocesamiento de expresiones matemáticas."""
        # Prueba de superíndices
        assert preprocess_expression("x²") == "x^2"
        assert preprocess_expression("2x³") == "2*x^3"
        
        # Prueba de multiplicación implícita
        assert preprocess_expression("2x") == "2*x"
        assert preprocess_expression("x(2)") == "x*(2)"
        
        # Prueba de funciones trigonométricas
        assert preprocess_expression("2sin(x)") == "2*sin(x)"
        assert preprocess_expression("3cos(x)") == "3*cos(x)"

    def test_safe_sympify(self):
        """Prueba la conversión segura de strings a expresiones simbólicas."""
        # Expresiones válidas
        assert str(safe_sympify("x^2")) == "x**2"
        assert str(safe_sympify("sin(x)")) == "sin(x)"
        
        # Expresiones inválidas
        with pytest.raises(ValueError):
            safe_sympify("invalid@expression")
        with pytest.raises(ValueError):
            safe_sympify("x^")

    def test_derivatives(self):
        """Prueba el cálculo de derivadas."""
        # Derivadas básicas
        expr = safe_sympify("x^2")
        assert str(diff(expr, x)) == "2*x"
        
        # Derivadas de funciones trigonométricas
        expr = safe_sympify("sin(x)")
        assert str(diff(expr, x)) == "cos(x)"
        
        # Derivadas compuestas
        expr = safe_sympify("exp(x^2)")
        assert str(diff(expr, x)) == "2*x*exp(x**2)"

    def test_integrals(self):
        """Prueba el cálculo de integrales."""
        # Integrales indefinidas
        expr = safe_sympify("2*x")
        assert str(integrate(expr, x)) == "x**2"
        
        # Integrales definidas
        expr = safe_sympify("x^2")
        result = integrate(expr, (x, 0, 1))
        assert abs(float(result) - 1/3) < 1e-10
        
        # Integrales de funciones trigonométricas
        expr = safe_sympify("cos(x)")
        assert str(integrate(expr, x)) == "sin(x)"

    def test_areas(self):
        """Prueba el cálculo de áreas entre curvas."""
        # Área entre x^2 y x
        f1 = safe_sympify("x^2")
        f2 = safe_sympify("x")
        area = integrate(Abs(f1 - f2), (x, 0, 1))
        assert abs(float(area) - 1/6) < 1e-10
        
        # Área entre sin(x) y cos(x)
        f1 = safe_sympify("sin(x)")
        f2 = safe_sympify("cos(x)")
        area = integrate(Abs(f1 - f2), (x, 0, 1))
        assert float(area) > 0

    def test_limits(self):
        """Prueba el cálculo de límites."""
        # Límite de x^2 en x=2
        expr = safe_sympify("x^2")
        assert abs(float(expr.subs(x, 2)) - 4) < 1e-10
        
        # Límite de sin(x)/x en x=0
        expr = safe_sympify("sin(x)/x")
        assert abs(float(expr.subs(x, 0.0001)) - 1) < 1e-4

    def test_series(self):
        """Prueba el cálculo de series de Taylor."""
        # Serie de e^x
        expr = safe_sympify("exp(x)")
        series = expr.series(x, 0, 3).removeO()
        assert "1 + x + x**2/2" in str(series)
        
        # Serie de sin(x)
        expr = safe_sympify("sin(x)")
        series = expr.series(x, 0, 3).removeO()
        assert "x - x**3/6" in str(series)

    def test_matrices(self):
        """Prueba el cálculo de determinantes de matrices."""
        # Matriz 2x2
        M = Matrix([[1, 2], [3, 4]])
        assert M.det() == -2
        
        # Matriz 3x3
        M = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        assert M.det() == 0

    def test_format_result(self):
        """Prueba el formateo de resultados."""
        # Formateo de potencias
        assert format_result("x**2") == "x^2"
        assert format_result("x**3") == "x^3"
        
        # Formateo de expresiones complejas
        expr = "2*x**2 + 3*x**3"
        assert format_result(expr) == "2*x^2 + 3*x^3"

    @pytest.mark.parametrize("input_expr,expected", [
        ("x^2", "2*x"),
        ("sin(x)", "cos(x)"),
        ("exp(x)", "exp(x)"),
        ("log(x)", "1/x"),
    ])
    def test_derivatives_parametrized(self, input_expr, expected):
        """Prueba parametrizada de derivadas comunes."""
        expr = safe_sympify(input_expr)
        assert str(diff(expr, x)) == expected

    @pytest.mark.parametrize("input_expr,limits,expected", [
        ("x^2", (0, 1), 1/3),
        ("2*x", (0, 1), 1),
        ("cos(x)", (0, 1), "sin(1)"),
    ])
    def test_integrals_parametrized(self, input_expr, limits, expected):
        """Prueba parametrizada de integrales comunes."""
        expr = safe_sympify(input_expr)
        result = integrate(expr, (x, limits[0], limits[1]))
        if isinstance(expected, (int, float)):
            assert abs(float(result) - expected) < 1e-10
        else:
            assert str(result) == expected 