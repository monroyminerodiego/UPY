### Aditional Info

''' fase_b.ipynb
'''

''' Folder structure
.
├── Data
│   ├── Processed
│   └── Raw
│       └── train.csv
├── Docs
│   ├── EDA.md
│   └── Instructions.pdf
├── index.html
├── Notebooks
│   ├── fase_a.ipynb
│   ├── fase_b.ipynb
│   ├── fase_c.ipynb
│   └── fase_d.ipynb
├── README.md
└── Scripts

7 directories, 9 files
'''

''' Dataset Overview
Train Dataset (8,523 records)
Includes both input features and the target variable (Item_Outlet_Sales).

Product Features
* Item_Identifier: Unique product ID
* Item_Weight: Weight of the product
* Item_Fat_Content: Fat level (low-fat or regular)
* Item_Visibility: Percentage of display area allocated to the product
* Item_Type: Category of the product
* Item_MRP: Maximum Retail Price

Store Features
* Outlet_Identifier: Unique store ID
* Outlet_Establishment_Year: Year the store was established
* Outlet_Size: Store size (small, medium, large)
* Outlet_Location_Type: City tier classification
* Outlet_Type: Type of outlet (grocery store, supermarket, etc.)

Target Variable
* Item_Outlet_Sales: Sales of the product at a particular store (to be predicted if a regression problem is needed)
'''

### Prompt
Como te puedes dar cuenta, tengo una estructura inicial para completar las instrucciones para este proyecto. Mi idea es hacer una notebook por cada fase, entonces en esta iteracion quiero empezar con la Fase C.  Te estoy compartiendo las instrucciones y los resultados del EDA (Fase A) que realice, además, te estoy dando el contenido de la notebook de la fase_b, que es donde hice la limpieza y el feature engineering. La notebook que vas a generar tiene que tener titulo, objetivo, secciones y un resumen de todo lo que se abarco durante la notebook. Cada seccion tiene que tener su subtitulo, un breve comentario de lo que se va a realizar, el codigo con prints informativos para que me ayuden a seguir el proceso. Tu respuesta tiene que ser un JSON listo para copiar y pegar con la información de la notebook. 

Toma en cuenta que esta iteración es solo una parte de todo el objetivo al que quiero llegar, por lo que tienes que tomar en cuenta los objetivos de la fase D, para que la respuesta que me des de la fase C sea coherente y pueda servirme para la fase D. No descuides lo primordial, que son los objetivos de la fase C.