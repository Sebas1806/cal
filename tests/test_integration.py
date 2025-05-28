import pytest
from APP import app
import json

@pytest.fixture
def client():
    """Fixture para crear un cliente de prueba."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

class TestIntegration:
    """Suite de pruebas de integración para la aplicación web."""

    def test_home_page(self, client):
        """Prueba que la página principal se carga correctamente."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Calculadora Matematica' in response.data

    def test_derivada_endpoint(self, client):
        """Prueba el endpoint de derivadas."""
        # Prueba derivada simple
        response = client.post('/', data={
            'funcion_derivada': 'x^2',
            'derivar': 'Calcular'
        })
        assert response.status_code == 200
        assert b'2*x' in response.data

        # Prueba derivada con error
        response = client.post('/', data={
            'funcion_derivada': 'invalid@expression',
            'derivar': 'Calcular'
        })
        assert response.status_code == 200
        assert b'Error' in response.data

    def test_integral_endpoint(self, client):
        """Prueba el endpoint de integrales."""
        # Prueba integral indefinida
        response = client.post('/', data={
            'funcion_integral': '2*x',
            'integrar': 'Calcular'
        })
        assert response.status_code == 200
        assert b'x^2' in response.data

        # Prueba integral definida
        response = client.post('/', data={
            'funcion_integral': 'x^2',
            'a_integral': '0',
            'b_integral': '1',
            'integrar': 'Calcular'
        })
        assert response.status_code == 200
        assert b'0.3333' in response.data

    def test_area_endpoint(self, client):
        """Prueba el endpoint de áreas entre curvas."""
        response = client.post('/', data={
            'funcion1_area': 'x^2',
            'funcion2': 'x',
            'a': '0',
            'b': '1',
            'area': 'Calcular'
        })
        assert response.status_code == 200
        assert b'0.1667' in response.data

    def test_volumen_endpoint(self, client):
        """Prueba el endpoint de volúmenes de revolución."""
        response = client.post('/', data={
            'funcion1_volumen': 'x^2',
            'a_volumen': '0',
            'b_volumen': '1',
            'volumen': 'Calcular'
        })
        assert response.status_code == 200
        assert b'0.6283' in response.data  # π/5

    def test_limites_endpoint(self, client):
        """Prueba el endpoint de límites."""
        # Prueba límite existente
        response = client.post('/', data={
            'funcion_limites': 'x^2',
            'punto': '2',
            'limites': 'Calcular'
        })
        assert response.status_code == 200
        assert b'4' in response.data

        # Prueba límite no existente
        response = client.post('/', data={
            'funcion_limites': '1/x',
            'punto': '0',
            'limites': 'Calcular'
        })
        assert response.status_code == 200
        assert b'no existe' in response.data.lower()

    def test_series_endpoint(self, client):
        """Prueba el endpoint de series de Taylor."""
        response = client.post('/', data={
            'funcion_series': 'exp(x)',
            'punto_series': '0',
            'orden_series': '3',
            'series': 'Calcular'
        })
        assert response.status_code == 200
        assert b'1 + x + x^2/2' in response.data

    def test_matriz_endpoint(self, client):
        """Prueba el endpoint de determinantes de matrices."""
        response = client.post('/', data={
            'matriz': '1, 2\n3, 4',
            'matriz': 'Calcular'
        })
        assert response.status_code == 200
        assert b'-2' in response.data

    def test_error_handling(self, client):
        """Prueba el manejo de errores en la aplicación."""
        # Prueba con datos inválidos
        response = client.post('/', data={
            'funcion_derivada': '',
            'derivar': 'Calcular'
        })
        assert response.status_code == 200

        # Prueba con tipo de dato incorrecto
        response = client.post('/', data={
            'funcion_integral': 'x^2',
            'a_integral': 'invalid',
            'b_integral': '1',
            'integrar': 'Calcular'
        })
        assert response.status_code == 200
        assert b'Error' in response.data

    def test_concurrent_requests(self, client):
        """Prueba el manejo de múltiples solicitudes simultáneas."""
        import threading
        import queue

        results = queue.Queue()
        def make_request():
            response = client.post('/', data={
                'funcion_derivada': 'x^2',
                'derivar': 'Calcular'
            })
            results.put(response.status_code)

        # Crear múltiples hilos para hacer solicitudes simultáneas
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()

        # Esperar a que todos los hilos terminen
        for thread in threads:
            thread.join()

        # Verificar que todas las solicitudes fueron exitosas
        while not results.empty():
            assert results.get() == 200

    def test_input_validation(self, client):
        """Prueba la validación de entrada en diferentes endpoints."""
        # Prueba de caracteres especiales
        response = client.post('/', data={
            'funcion_derivada': 'x^2@#$',
            'derivar': 'Calcular'
        })
        assert response.status_code == 200
        assert b'Error' in response.data

        # Prueba de límites de integración inválidos
        response = client.post('/', data={
            'funcion_integral': 'x^2',
            'a_integral': '2',
            'b_integral': '1',  # b < a
            'integrar': 'Calcular'
        })
        assert response.status_code == 200

        # Prueba de orden de serie inválido
        response = client.post('/', data={
            'funcion_series': 'exp(x)',
            'punto_series': '0',
            'orden_series': '21',  # > 20
            'series': 'Calcular'
        })
        assert response.status_code == 200
        assert b'Error' in response.data

    def test_response_format(self, client):
        """Prueba el formato de las respuestas."""
        # Prueba formato de derivada
        response = client.post('/', data={
            'funcion_derivada': 'x^2',
            'derivar': 'Calcular'
        })
        assert b'<b>Derivada:</b>' in response.data

        # Prueba formato de integral
        response = client.post('/', data={
            'funcion_integral': '2*x',
            'integrar': 'Calcular'
        })
        assert b'<b>Integral Indefinida:</b>' in response.data

        # Prueba formato de área
        response = client.post('/', data={
            'funcion1_area': 'x^2',
            'funcion2': 'x',
            'a': '0',
            'b': '1',
            'area': 'Calcular'
        })
        assert b'u2' in response.data 