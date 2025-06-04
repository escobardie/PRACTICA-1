import pandas as pd
import logging
from domain.dataset import Dataset
from utils.logger_mixin import LoggerMixin  # Solo si usás un mixin para logger

class DatasetExcel(Dataset, LoggerMixin):
    def __init__(self, fuente):
        """
        Inicializa la instancia con la ruta del archivo Excel.
        """
        super().__init__(fuente)

    def cargar_datos(self):
        """
        Carga datos desde un archivo Excel (.xlsx o .xls).
        Si la carga es exitosa, valida y transforma los datos.
        """
        if not self.fuente:
            self.logger.error("Ruta de archivo Excel no especificada.")
            return

        try:
            df = pd.read_excel(self.fuente)
            self.datos = df
            self.logger.info("Datos de Excel cargados correctamente.")

            if self.validar_datos():
                self.transformar_datos()

        except FileNotFoundError:
            self.logger.error(f"Archivo Excel no encontrado: {self.fuente}")
        except ValueError as e:
            self.logger.error(f"Error al leer el archivo Excel: {e}")
        except Exception as e:
            self.logger.exception(f"Error inesperado al cargar Excel: {e}")
