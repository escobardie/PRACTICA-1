import requests  # Librería para hacer peticiones HTTP
import pandas as pd  # Librería para manipulación de datos
from domain.dataset import Dataset  # Clase personalizada
from utils.logger_mixin import LoggerMixin # Clase personalizada


class DatasetAPI2(Dataset, LoggerMixin):
    def __init__(self, fuente):
        """
        Constructor que recibe la fuente (URL de la API) y llama al constructor de la clase base.
        """
        super().__init__(fuente)

    def cargar_datos(self):
        """
        Carga datos desde una API RESTful en formato JSON y los almacena como un DataFrame.
        Incluye validación y transformación de listas.
        """
        if not self.fuente:
            self.logger.error("URL de la API no especificada.")
            return

        try:
            # Realiza una petición GET con un timeout de 10 segundos
            response = requests.get(self.fuente, timeout=10)
            response.raise_for_status()  # Lanza una excepción si el status no es 200

            # Intenta decodificar la respuesta JSON
            data = response.json()

            # Normaliza datos anidados del JSON a un DataFrame plano
            df = pd.json_normalize(data)

            # Recorre las columnas para convertir listas a strings
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, list)).any():
                    df[col] = df[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

            # Asigna los datos al atributo `datos`
            self.datos = df
            self.logger.info("Datos de API cargados correctamente.")

            # Valida y transforma los datos si todo salió bien
            if self.validar_datos():
                self.transformar_datos()

        # Excepciones específicas para distintos tipos de error
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Error HTTP al acceder a la API: {e}")
        except requests.exceptions.ConnectionError:
            self.logger.error("Error de conexión a la API.")
        except requests.exceptions.Timeout:
            self.logger.error("La solicitud a la API excedió el tiempo de espera.")
        except ValueError as e:
            self.logger.error(f"No se pudo decodificar JSON: {e}")
        except Exception as e:
            self.logger.exception(f"Error inesperado al cargar datos de la API: {e}")

