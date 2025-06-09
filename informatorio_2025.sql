CREATE DATABASE gestion_analisis;
USE gestion_analisis;
SHOW TABLES;

/* DDL CON ENFOQUE EN SEGURIDAD*/
/* creamos un usuario con permisos solo para acceder a la base de datos gestion_producto*/

/* usuario: userGestionAnalisis1,  password: userGestionAnalisis-1 */
CREATE USER 'userGestionAnalisis1'@'localhost' identified by 'userGestionAnalisis-1';

GRANT ALL PRIVILEGES ON gestion_analisis.* TO userGestionAnalisis1@localhost;
FLUSH PRIVILEGES;

DROP USER 'userGestionAnalisis1'@'localhost';



SHOW TABLES;

desc table ventas_xlsx;
select * from ventas_xlsx;

desc table w_mean_prod_csv;
select * from w_mean_prod_csv;

desc table personas_json;
select * from personas_json;

desc table user_api;
select * from user_api;

desc table provincia_api;
select * from provincia_api;

desc table poke_api;
select * from poke_api; 

desc table precios_csv;
select * from precios_csv;

drop tables precios_csv, poke_api, ventas_xlsx, user_api, provincia_api, w_mean_prod_csv, personas_json, user_api, provincia_api ;