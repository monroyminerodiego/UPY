
# Informacion General
| No. | Column                    | Non-Null Count | Dtype   |
| --- | ------                    | -------------- | -----   |
|  0  | Item_Identifier           | 8523 non-null  | object  |
|  1  | Item_Weight               | 7060 non-null  | float64 |
|  2  | Item_Fat_Content          | 8523 non-null  | object  |
|  3  | Item_Visibility           | 8523 non-null  | float64 |
|  4  | Item_Type                 | 8523 non-null  | object  |
|  5  | Item_MRP                  | 8523 non-null  | float64 |
|  6  | Outlet_Identifier         | 8523 non-null  | object  |
|  7  | Outlet_Establishment_Year | 8523 non-null  | int64   |
|  8  | Outlet_Size               | 6113 non-null  | object  |
|  9  | Outlet_Location_Type      | 8523 non-null  | object  |
|  10 | Outlet_Type               | 8523 non-null  | object  |
|  11 | Item_Outlet_Sales         | 8523 non-null  | float64 |


| Columna                   | Valores únicos | Ejemplo de valores |
| -------                   | -------------- | ------------------ |
| Item_Identifier           | 1559           | ['FDA15' 'DRC01' 'FDN15'] |
| Item_Weight               | 415            | ['9.3' '5.92' '17.5'] |
| Item_Fat_Content          | 5              | ['Low Fat' 'Regular' 'low fat' 'LF' 'reg']
| Item_Visibility           | 7880           | ['0.016047301' '0.019278216' '0.016760075'] |
| Item_Type                 | 16             | ['Dairy' 'Soft Drinks' 'Meat'] |
| Item_MRP                  | 5938           | ['249.8092' '48.2692' '141.618'] |
| Outlet_Identifier         | 10             | ['OUT049' 'OUT018' 'OUT010' 'OUT013' 'OUT027' 'OUT045' 'OUT017' 'OUT046' 'OUT035' 'OUT019']
| Outlet_Establishment_Year | 9              | [1999 2009 1998 1987 1985 2002 2007 1997 2004]
| Outlet_Size               | 3              | ['Medium' nan 'High' 'Small']
| Outlet_Location_Type      | 3              | ['Tier 1' 'Tier 3' 'Tier 2']
| Outlet_Type               | 4              | ['Supermarket Type1' 'Supermarket Type2' 'Grocery Store' 'Supermarket Type3']
| Item_Outlet_Sales         | 3493           | ['3735.138' '443.4228' '2097.27'] |

`Variables numéricas`: ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Outlet_Establishment_Year', 'Item_Outlet_Sales']
`Variables categóricas`: ['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 'Outlet_Identifier', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']

`Análisis de Outliers`
* Item_Outlet_Sales presenta muchos outliers en el rango superior. Esto es natural en ventas (productos estrella).
* Item_Visibility también tiene outliers superiores. Algunos productos tienen mucha más exhibición que otros.
* Item_Weight: 1463 nulos (17.2%) → Puede imputarse con mediana por tipo de producto
* Outlet_Size: 2410 nulos (28.3%) → Fuerte correlación con Outlet_Type, imputación condicional recomendada
* No hay nulos en variables críticas (ID, ventas, precio) → Buena señal de calidad del dataset

`Análisis de Duplicados`
Registros totalmente duplicados: 0

`Análisis de Valores Faltantes`
             Missing Values    Percent
Item_Weight            1463  17.165317
Outlet_Size            2410  28.276428

`NOTAS IMPORTANTE PARA CLUSTERING`
- Tenemos 8523 registros totales, pero solo 1559 productos únicos. Esto confirma que en la Fase B deberemos agregar los datos para reducir las 8523 filas a 1559 filas (una por producto).
- Hay 526 registros con Item_Visibility = 0. Esto no tiene sentido físico (un producto no puede ser invisible). En la limpieza, esto debe tratarse como valor faltante o imputarse con el promedio.
- Existe una correlación positiva clara entre MRP y Ventas. Además, el MRP parece estar segmentado en 4 grupos claros de precios

# Variables Numericas
* Item_Visibility: Rango 0-0.33, media 0.066 → Alta concentración en valores bajos
* Item_Weight: Valores faltantes en 1463 registros (17.2%)
* Item_MRP: Rango $31.29 - $266.89, alta variabilidad (CV: 0.44)
* Item_Outlet_Sales: Altamente sesgada (asimetría: 1.18) → Requiere transformación para clustering

# Variables Categoricas
* Item_Type: 16 categorías → Diversidad de productos significativa para clustering
* Outlet_Type: 4 tipos → Puede definir comportamientos de tienda distintos
* Item_Fat_Content: Valores inconsistentes ('Low Fat' vs 'low fat') → Requiere estandarización
* Outlet_Size: 2410 valores faltantes (28.3%) → Necesita imputación estratégica

# Distribuciones
* `Item_Weight`: Asimetría = 0.08 (Distribución aproximadamente simétrica)
* `Item_Visibility`: Asimetría = 1.17 (Distribución altamente sesgada)
* `Item_MRP`: Asimetría = 0.13 (Distribución aproximadamente simétrica)
* `Outlet_Establishment_Year`: Asimetría = -0.40 (Distribución aproximadamente simétrica)
* `Item_Outlet_Sales`: Asimetría = 1.18 (Distribución altamente sesgada)

`Distribución de Item_Fat_Content`
Low Fat    5089
Regular    2889
LF          316
reg         117
low fat     112
Se observa mezcla de etiquetas (Low Fat, LF, low fat). Esto DEBE unificarse en la Fase B.

`Distribución de Item_Type`
Fruits and Vegetables    1232
Snack Foods              1200
Household                 910
Frozen Foods              856
Dairy                     682
Canned                    649
Baking Goods              648
Health and Hygiene        520
Soft Drinks               445
Meat                      425
Breads                    251
Hard Drinks               214
Others                    169
Starchy Foods             148
Breakfast                 110
Seafood                    64

`Distribución de Outlet_Type`
Supermarket Type1    5577
Grocery Store        1083
Supermarket Type3     935
Supermarket Type2     928

`Distribución de Outlet_Location_Type`
Tier 3    3350
Tier 2    2785
Tier 1    2388

`Distribución de Outlet_Size`
Medium    2793
Small     2388
High       932
