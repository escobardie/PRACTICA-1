import requests
import pandas as pd
from domain.dataset import Dataset
from utils.logger_mixin import LoggerMixin


class DatasetPokeAPI(Dataset, LoggerMixin):
    """
        optimizado solo para la api de provincias
    """
    def __init__(self, fuente):
        super().__init__(fuente)

    def cargar_datos(self):
        if not self.fuente:
            self.logger.error("URL de la API no especificada.")
            return

        try:
            response = requests.get(self.fuente, timeout=10)
            response.raise_for_status()  # Lanza excepción si no es 200

            # Acceder al contenido dentro de "results"
            data = response.json()
            df = pd.json_normalize(data.get("results", []))

            # Convertir columnas con listas a strings
            for col in df.columns:
                if df[col].apply(lambda x: isinstance(x, list)).any():
                    df[col] = df[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

            self.datos = df
            self.logger.info("Datos de API cargados correctamente.")

            if self.validar_datos():
                self.transformar_datos()

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"Error HTTP al acceder a la API: {e}")
        except requests.exceptions.ConnectionError:
            self.logger.error("Error de conexión a la API.")
        except requests.exceptions.Timeout:
            self.logger.error("Tiempo de espera agotado para la API.")
        except ValueError as e:
            self.logger.error(f"Error al parsear JSON: {e}")
        except Exception as e:
            self.logger.exception(f"Error inesperado al cargar datos de la API: {e}")
