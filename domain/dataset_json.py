import pandas as pd
import json
from domain.dataset import Dataset
from utils.logger_mixin import LoggerMixin

class DatasetJSON(Dataset, LoggerMixin):
    def __init__(self, fuente):
        """
        Inicializa la clase con la fuente (archivo JSON).
        """
        super().__init__(fuente)

    def cargar_datos(self):
        """
        Carga datos desde un archivo JSON local.
        Valida la estructura del JSON antes de cargar con Pandas.
        Aplica validaciones y transformaciones si es exitoso.
        """
        if not self.fuente:
            self.logger.error("Fuente no especificada.")
            return

        try:
            # Verificación sintáctica del JSON
            with open(self.fuente, 'r', encoding='utf-8') as file:
                contenido = file.read()
                json.loads(contenido)

            df = pd.read_json(self.fuente)

            if df.empty:
                self.logger.warning("El archivo JSON está vacío.")
                return

            self.datos = df
            self.logger.info("Datos JSON cargados correctamente.")

            if self.validar_datos():
                self.transformar_datos()

        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"El archivo no contiene JSON válido: {e}")
        except FileNotFoundError:
            self.logger.error(f"Archivo no encontrado: {self.fuente}")
        except Exception as e:
            self.logger.exception(f"Error inesperado cargando JSON: {e}")
