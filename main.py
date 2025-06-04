from os import path
from domain.dataset_csv import DatasetCSV
from domain.dataset_excel import DatasetExcel
from domain.dataset_api import DatasetAPI
from domain.dataset_api2 import DatasetAPI2
from domain.dataset_json import DatasetJSON
from data.data_saver import DataSaver

# URL PARA API
url_users = "https://jsonplaceholder.typicode.com/users"
url_provincias = "https://apis.datos.gob.ar/georef/api/provincias"

# Ruta de archivos
csv_path = path.join(path.dirname(__file__), "files/w_mean_prod.csv")
excel_path = path.join(path.dirname(__file__), "files/ventas.xlsx")
json_path = path.join(path.dirname(__file__), "files/personas.json")

# Cargar y transformar
csv = DatasetCSV(csv_path)
csv.cargar_datos()
# csv.mostrar_resumen()

excel = DatasetExcel(excel_path)
excel.cargar_datos()
# excel.mostrar_resumen()

json = DatasetJSON(json_path)
json.cargar_datos()
# json.mostrar_resumen()

api = DatasetAPI(url_provincias)
api.cargar_datos()
# api.mostrar_resumen()

api2 = DatasetAPI2(url_users)
api2.cargar_datos()
api2.mostrar_resumen()

# guardar en base de datos
db = DataSaver()
# db.guardar_dataframe(csv.datos, "w_mean_prod_csv")
# db.guardar_dataframe(excel.datos, "ventas_xlsx")
# db.guardar_dataframe(json.datos, "personas_json")
# db.guardar_dataframe(api2.datos, "user_api")
# db.guardar_dataframe(api.datos, "provincia_api")
