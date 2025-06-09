# import pandas as pd
# import logging
# from domain.dataset import Dataset
# from utils.logger_mixin import LoggerMixin  # Si estás usando el LoggerMixin

# class DatasetCSV(Dataset, LoggerMixin):
#     def __init__(self, fuente):
#         """
#         Inicializa la clase con la ruta o URL del archivo CSV.
#         """
#         super().__init__(fuente)

#     def cargar_datos(self):
#         """
#         Carga datos desde un archivo CSV. Valida y transforma si corresponde.
#         """
#         if not self.fuente:
#             self.logger.error("Ruta de archivo CSV no especificada.")
#             return

#         try:
#             df = pd.read_csv(self.fuente)
#             self.datos = df
#             self.logger.info("Datos CSV cargados correctamente.")

#             if self.validar_datos():
#                 self.transformar_datos()

#         except FileNotFoundError:
#             self.logger.error(f"Archivo CSV no encontrado: {self.fuente}")
#         except pd.errors.EmptyDataError:
#             self.logger.error("El archivo CSV está vacío.")
#         except pd.errors.ParserError as e:
#             self.logger.error(f"Error al parsear CSV: {e}")
#         except Exception as e:
#             self.logger.exception(f"Error inesperado al cargar CSV: {e}")

import pandas as pd
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
        delimitadores = [';', ',']
        for sep in delimitadores:
            
            try:
                df = pd.read_csv(
                    self.fuente,
                    sep=sep,
                    encoding='latin1',  # permite caracteres como 'Género'
                    dayfirst=True
                )

                if df.shape[1] > 1:
                    self.datos = df
                    self.logger.info(f"Datos CSV cargados correctamente con separador '{sep}'.")

                    # Combinar fecha y hora si están presentes
                    # if 'fecha' in df.columns and 'hora' in df.columns:
                    #     try:
                    #         df['fecha_hora'] = pd.to_datetime(
                    #             df['fecha'] + ' ' + df['hora'],
                    #             dayfirst=True,
                    #             errors='coerce'
                    #         )
                    #     except Exception as e:
                    #         self.logger.warning(f"No se pudo combinar 'fecha' y 'hora': {e}")

                    if self.validar_datos():
                        self.transformar_datos()
                    return

            
            except FileNotFoundError:
                self.logger.error(f"Archivo CSV no encontrado: {self.fuente}")
            except pd.errors.EmptyDataError:
                self.logger.error("El archivo CSV está vacío.")
            except pd.errors.ParserError as e:
                self.logger.error(f"Error al parsear CSV: {e}")
            except Exception as e:
                self.logger.warning(f"Error con separador '{sep}': {e}")
