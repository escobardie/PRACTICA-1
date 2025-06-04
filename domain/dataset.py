from abc import ABC, abstractmethod
import pandas as pd
from utils.logger_mixin import LoggerMixin

class Dataset(ABC, LoggerMixin):
    def __init__(self, fuente):
        """
        Inicializa la clase base con una fuente (puede ser ruta a archivo o URL).
        Valida que la fuente no sea None o vacía.
        """
        if not fuente:
            raise ValueError("La fuente no puede estar vacía.")
        self.__fuente = fuente
        self.__datos = None

    @property
    def datos(self):
        """
        Devuelve los datos cargados como DataFrame.
        """
        return self.__datos

    @datos.setter
    def datos(self, value):
        """
        Asigna los datos al atributo interno si es un DataFrame.
        Lanza un error si se intenta asignar otro tipo de objeto.
        """
        if not isinstance(value, pd.DataFrame):
            raise TypeError("Los datos deben ser un DataFrame de pandas.")
        self.__datos = value

    @property
    def fuente(self):
        """
        Devuelve la fuente de datos.
        """
        return self.__fuente

    @abstractmethod
    def cargar_datos(self):
        """
        Método abstracto que debe implementarse en las subclases para cargar datos.
        """
        pass

    def validar_datos(self):
        """
        Verifica que los datos estén cargados, no estén vacíos,
        y reporta si hay valores nulos o filas duplicadas.
        """
        if self.datos is None:
            raise ValueError("Los datos no han sido cargados todavía.")

        if self.datos.empty:
            raise ValueError("El DataFrame está vacío.")

        if self.datos.isnull().sum().sum() > 0:
            self.logger.warning("Se detectaron valores faltantes.")
        if self.datos.duplicated().sum() > 0:
            self.logger.warning("Se detectaron filas duplicadas.")

        return True

    def transformar_datos(self):
        """
        Aplica transformaciones al DataFrame:
        - Nombres de columnas en minúsculas y sin espacios.
        - Elimina duplicados.
        - Elimina espacios en blanco de strings.
        """
        if self.datos is None:
            raise ValueError("No hay datos para transformar.")

        try:
            # Normaliza nombres de columnas
            self.__datos.columns = self.datos.columns.str.lower().str.replace(" ", "_")

            # Elimina filas duplicadas
            self.__datos = self.datos.drop_duplicates()

            # Limpia strings en columnas de tipo object
            for col in self.datos.select_dtypes(include="object").columns:
                self.__datos[col] = self.datos[col].astype(str).str.strip()

            self.logger.info("Transformaciones aplicadas correctamente.")

        except Exception as e:
            self.logger.exception(f"Error al transformar datos: {e}")
            raise

    def mostrar_resumen(self):
        """
        Muestra un resumen estadístico del DataFrame si hay datos cargados.
        """
        try:
            if self.datos is not None:
                resumen = self.datos.describe(include="all")
                print(resumen)
                return resumen
            else:
                self.logger.warning("No hay datos para mostrar.")
                print("No hay datos para mostrar.")

        except Exception as e:
            self.logger.exception(f"Error al mostrar resumen: {e}")
            raise
