USE Upysusa;
-- SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'GASTOS' OR TABLE_NAME = 'SUCURSALES';

/* ******** BASIC TABLES ********
SELECT * FROM SUCURSALES

SELECT * FROM GASTOS

SELECT * FROM EMPLEADOS

SELECT * FROM TICKETS

SELECT * FROM ALMACEN_POR_SUCURSAL

SELECT * FROM COMPRAS
*/;

-- Relacion Sucursal - Productos (¿Que almacen tiene más variedad de productos?)

SELECT * FROM ALMACEN_POR_SUCURSAL ORDER BY ID_COMPRA ASC
SELECT * FROM COMPRA_POR_PRODUCTO ORDER BY ID_COMPRA ASC
SELECT * FROM PRODUCTOS

SELECT 
    CPP.ID_COMPRA, 
    CPP.ID_PRODUCTO, 
        PRD.CATEGORIA AS CATEGORIA_PRODUCTO,
        PRD.NOMBRE AS NOMBRE_PRODUCTO, 
        PRD.ID_PROVEEDOR,
            PRV.RAZON_SOCIAL,
    CPP.DIA_COMPRA, 
    CPP.MES_COMPRA, 
    CPP.ANO_COMPRA,
    APS.TS_INGRESO
    
FROM COMPRA_POR_PRODUCTO CPP
INNER JOIN ALMACEN_POR_SUCURSAL APS ON CPP.ID_COMPRA = APS.ID_COMPRA
INNER JOIN PRODUCTOS AS PRD ON CPP.ID_PRODUCTO = PRD.ID_PRODUCTO
INNER JOIN PROVEEDORES AS PRV ON PRD.ID_PROVEEDOR = PRV.ID_PROVEEDOR