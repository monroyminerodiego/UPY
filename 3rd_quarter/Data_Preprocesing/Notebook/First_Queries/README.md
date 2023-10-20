# Class Task: SQL data pre-precessing

## Instructions Given by Professor
INEGI Database: Contains 3 tables.
- Substitute special characters (cols. Nom_ent and Complejida)
- Create Dummy columns based on Categorical data.

Expected delivery:
- File with the screenshots of the followed procedure
- Script sql of the selections made (With comments)


## Description of queries
- Query_1  
Selection of all registers
    Query: 
    ``` sql
    SELECT * FROM INEGI.dbo.INE_DISTRITO_2020
    ```  
    Expected output:  
    <image src='Images/Query_1.png' width="500" height="500">

- Query_2  
Selection of 'NOM_ENT' that fits in range from 18500 to 30500
    Query: 
    ``` sql
    SELECT NOM_ENT
    FROM INEGI.dbo.INE_DISTRITO_2020
    WHERE PCON_DISC BETWEEN 18500 AND 30500;
    ```  
    Expected output:  
    <image src='./Images/Query_2.png' width="500" height="500">

- Query_3  
Updating the value 'Caracolandia' to 'Quintana Roo' from column 'NOM_ENT' and selecting the updated rows
    Query: 
    ``` sql
    UPDATE INEGI.dbo.INE_DISTRITO_2020
    SET NOM_ENT = 'Caracolandia'
    WHERE NOM_ENT = 'Quintana Roo';

    SELECT * FROM INEGI.dbo.INE_DISTRITO_2020
    WHERE NOM_ENT = 'Caracolandia'
    ```  
    Expected output:  
    <image src='./Images/Query_3.png' width="500" height="500">

- Query_4  
First, selecting 'NOM_ENT' column to then update the next values that follows a relation 'key:value' where key is the actual value and the value will be the new value:
Ciudad de M% : Ciudad de México
Michoac% : Michoacán de Ocampo
M%exico : México
Nuevo Le%n : Nuevo León
Quer%taro : Querétaro
Yucat%n : Yucatán
San Luis% : San Luis Potosí
    Query: 
    ``` sql
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
    SET NOM_ENT = 'Nuevo León'
    WHERE NOM_ENT LIKE 'Nuevo Le%n';

    UPDATE INEGI.dbo.INE_DISTRITO_2020
    SET NOM_ENT = 'Querétaro'
    WHERE NOM_ENT LIKE 'Quer%';

    UPDATE INEGI.dbo.INE_DISTRITO_2020
    SET NOM_ENT = 'Yucatán'
    WHERE NOM_ENT LIKE 'Yucat%n';

    UPDATE INEGI.dbo.INE_DISTRITO_2020
    SET NOM_ENT = 'San Luis Potosí'
    WHERE NOM_ENT LIKE 'San Luis%';

    SELECT DISTINCT NOM_ENT FROM INEGI.dbo.INE_DISTRITO_2020;
    ```  
    Expected output:  
    <image src='./Images/Query_4.png' width="500" height="500">

- Query_5  
Updating the values like 'Concentraci%n Media' to 'Concentración Media' and selecting 
    Query: 
    ``` sql
    
    ```  
    Expected output:  
    <image src='./Images/Query_5.png' width="500" height="500">

- Query_6  
    Query: 
    ``` sql
    
    ```  
    Expected output:  
    <image src='./Images/Query_6.png' width="500" height="500">

- Query_7  
    Query: 
    ``` sql
    
    ```  


- Query_8  
    Query: 
    ``` sql
    
    ```  
    Expected output:  
    <image src='./Images/Query_8.png' width="500" height="500">

## Made By
- Diego Monroy Minero