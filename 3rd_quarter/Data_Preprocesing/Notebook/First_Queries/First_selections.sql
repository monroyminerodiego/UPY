-- Detailed description comment: Query_1
SELECT * FROM INEGI.dbo.INE_DISTRITO_2020;


-- Detailed description comment: Query_2
SELECT NOM_ENT
FROM INEGI.dbo.INE_DISTRITO_2020
WHERE PCON_DISC BETWEEN 18500 AND 30500;

-- Detailed description comment: Query_3
UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'Caracolandia'
WHERE NOM_ENT = 'Quintana Roo';

SELECT * FROM INEGI.dbo.INE_DISTRITO_2020
WHERE NOM_ENT = 'Caracolandia'

-- Detailed description comment: Query_4
SELECT DISTINCT NOM_ENT FROM INEGI.dbo.INE_DISTRITO_2020

UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'Ciudad de México'
WHERE NOM_ENT LIKE 'Ciudad de M%';

UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'Michoacán de Ocampo'
WHERE NOM_ENT LIKE 'Michoac%';

UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'México'
WHERE NOM_ENT LIKE 'M%xico';

UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'Nuevo Le�n'
WHERE NOM_ENT LIKE 'Nuevo Le%n';

UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'Quer�taro'
WHERE NOM_ENT LIKE 'Quer%';

UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'Yucat�n'
WHERE NOM_ENT LIKE 'Yucat%n';

UPDATE INEGI.dbo.INE_DISTRITO_2020
SET NOM_ENT = 'San Luis Potos�'
WHERE NOM_ENT LIKE 'San Luis%';

-- Detailed description comment: Query_5
UPDATE INEGI.dbo.INE_DISTRITO_2020
SET COMPLEJIDA = 'Concentraci�n Media'
WHERE COMPLEJIDA LIKE 'Concentraci%n Media';

SELECT * FROM INEGI.dbo.INE_DISTRITO_2020;

-- Detailed description comment: Query_6
SELECT DISTINCT COMPLEJIDA FROM INEGI.dbo.INE_DISTRITO_2020

-- Altamente Concentrado 1
-- Altamente Concentrado 2
-- Concentraci�n Media
-- Concentrado 1
-- Concentrado 2
-- Disperso 1
-- Disperso 2
-- Muy Disperso 1
-- Muy Disperso 2

-- Detailed description comment: Query_7
ALTER TABLE INEGI.dbo.INE_DISTRITO_2020
ADD ALT_CON_1 INT, ALT_CON_2 INT, CON_MED INT, CON1 INT, CON2 INT, DIS1 INT, DIS2 INT, MDIS_1 INT, MDIS_2 INT;