import pandas as pd
import logging
from domain.dataset import Dataset
from utils.logger_mixin import LoggerMixin  # Si estás usando el LoggerMixin

class DatasetCSV(Dataset, LoggerMixin):
    def __init__(self, fuente):
        """
        Inicializa la clase con la ruta o URL del archivo CSV.
        """
        super().__init__(fuente)

    def cargar_datos(self):
        """
        Carga datos desde un archivo CSV. Valida y transforma si corresponde.
        """
        if not self.fuente:
            self.logger.error("Ruta de archivo CSV no especificada.")
            return

        try:
            df = pd.read_csv(self.fuente)
            self.datos = df
            self.logger.info("Datos CSV cargados correctamente.")

            if self.validar_datos():
                self.transformar_datos()

        except FileNotFoundError:
            self.logger.error(f"Archivo CSV no encontrado: {self.fuente}")
        except pd.errors.EmptyDataError:
            self.logger.error("El archivo CSV está vacío.")
        except pd.errors.ParserError as e:
            self.logger.error(f"Error al parsear CSV: {e}")
        except Exception as e:
            self.logger.exception(f"Error inesperado al cargar CSV: {e}")
