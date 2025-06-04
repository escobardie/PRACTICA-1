import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.exc import SQLAlchemyError
from decouple import config
from utils.logger_mixin import LoggerMixin


class DataSaver(LoggerMixin):
    def __init__(self):
        """
        Inicializa la conexión a la base de datos usando variables del archivo .env
        """
        try:
            user = config('DB_USER')
            password = config('DB_PASSWORD')
            host = config('DB_HOST')
            port = config('DB_PORT')
            database = config('DB_NAME')

            # Creamos la URL de conexión
            url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

            # Crea el engine de SQLAlchemy
            self.engine = create_engine(url)
            self.inspector = inspect(self.engine)
            self.logger.info("Conexión con la base de datos establecida correctamente.")

        except Exception as e:
            self.logger.exception("Error al configurar la conexión a la base de datos.")
            raise

    def guardar_dataframe(self, df, nombre_tabla):
        """
        Guarda un DataFrame en una tabla ( de la base de datos), verifica si la tabla ya existe.
        """
        if df is None or df.empty:
            self.logger.warning(f"No se puede guardar: DataFrame vacío para la tabla '{nombre_tabla}'.")
            return

        if not isinstance(df, pd.DataFrame):
            self.logger.error(f"Tipo inválido: se esperaba un DataFrame, se recibió {type(df)}.")
            return

        # Verificar si la tabla ya existe en la base de datos
        tabla_existe = self.inspector.has_table(nombre_tabla)

        if tabla_existe:
            self.logger.info(f"La tabla '{nombre_tabla}' ya existe en la base de datos.")
            opcion = input("¿Qué desea hacer? [R]eemplazar, [A]gregar, [C]ancelar: ").strip().lower()

            # opciones para realizar accion "mejorar"
            if opcion == 'r':
                modo = 'replace'
            elif opcion == 'a':
                modo = 'append'
            else:
                self.logger.info("Operación cancelada por el usuario.")
                return
        else:
            modo = 'replace'

        # Guardar el DataFrame
        try:
            df.to_sql(nombre_tabla, con=self.engine, if_exists=modo, index=False)
            self.logger.info(f"Datos guardados exitosamente en la tabla: {nombre_tabla} (modo: {modo})")

        except SQLAlchemyError as e:
            self.logger.exception(f"Error al guardar datos en la tabla '{nombre_tabla}': {e}")
