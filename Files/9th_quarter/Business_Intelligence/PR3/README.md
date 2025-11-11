# Credit Risk Analisys - German Data

## Descripción del Proyecto

Este proyecto se centra en el análisis del conjunto de datos "German Credit", que contiene información sobre 1000 instancias de créditos, describiendo a cada solicitante a través de 20 atributos tanto numéricos como categóricos. El objetivo es explorar los datos, visualizar patrones clave y, finalmente, construir un modelo de aprendizaje automático para predecir el riesgo crediticio (clasificando a los clientes como "buenos" o "malos").

Este análisis es crucial para entender los factores que influyen en la morosidad y para desarrollar herramientas que ayuden en la toma de decisiones financieras.

## Objetivos

Los principales objetivos de este proyecto son:

1.  **Análisis Exploratorio de Datos (EDA):** Realizar una investigación inicial de los datos para descubrir patrones, detectar anomalías, probar hipótesis y verificar suposiciones con la ayuda de estadísticas resumidas y representaciones gráficas.
2.  **Dashboard de Business Intelligence (BI):** Crear un dashboard interactivo que permita a los usuarios visualizar y explorar las métricas y dimensiones más importantes del conjunto de datos, facilitando la comprensión del perfil de los solicitantes de crédito.
3.  **Modelo de Machine Learning (ML):** Desarrollar y evaluar un modelo de clasificación para predecir la solvencia de un cliente (buen o mal pagador), teniendo en cuenta la matriz de costos proporcionada, donde clasificar erróneamente a un cliente "malo" como "bueno" tiene un costo 5 veces mayor que el error inverso.

## Descripción de los Datos (JSON)

A continuación, se detalla la estructura de los 20 atributos contenidos en el archivo `german.data`, en formato JSON:

```json
[
    {
      "nombre": "Attribute 1: Status of existing checking account",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A11": "... < 0 DM",                                             // low
        "A12": "0 <= ... < 200 DM",                                      // mid
        "A13": "... >= 200 DM / salary assignments for at least 1 year", // high
        "A14": "no checking account"                                     // low
      }
    },
    {
      "nombre": "Attribute 2: Duration in month",
      "tipo": "numérico",
      "descripcion_valores": "Duración del crédito en meses"
      // 12 >  year       --> less 1 year
      // 12 <= year <= 36 --> 1 to 3 years
      //       year >  36 --> more 3 years
    },
    {
      "nombre": "Attribute 3: Credit history",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A31": "all credits at this bank paid back duly",                     // good
        "A32": "existing credits paid back duly till now",                    // good
        "A30": "no credits taken / all credits paid back duly",               // warning
        "A33": "delay in paying off in the past",                             // warning
        "A34": "critical account / other credits existing (not at this bank)" // critical
      }
    },
    {
      "nombre": "Attribute 4: Purpose",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A40": "car (new)",                    // durable-goods
        "A41": "car (used)",                   // durable-goods
        "A42": "furniture/equipment",          // durable-goods
        "A43": "radio/television",             // durable-goods
        "A44": "domestic appliances",          // durable-goods
        "A46": "education",                    // education
        "A48": "retraining",                   // education
        "A45": "repairs",                      // business
        "A49": "business",                     // business
        "A47": "(vacation - does not exist?)", // others
        "A410": "others"                       // others
      }
    },
    {
      "nombre": "Attribute 5: Credit amount",
      "tipo": "numérico",
      "descripcion_valores": "Monto del crédito"
      // 3500 >  year         --> less 3.5k
      // 3500 <= year <= 7000 --> 3.5k to 7 k
      //         year >  7000 --> more 7k
    },
    {
      "nombre": "Attribute 6: Savings account/bonds",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A61": "... < 100 DM",               //  low
        "A62": "100 <= ... < 500 DM",        //  mid
        "A63": "500 <= ... < 1000 DM",       //  high
        "A64": ".. >= 1000 DM",              //  high
        "A65": "unknown/ no savings account" //  low
      }
    },
    {
      "nombre": "Attribute 7: Present employment since",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A71": "unemployed",         // jr
        "A72": "... < 1 year",       // jr
        "A73": "1 <= ... < 4 years", // md
        "A74": "4 <= ... < 7 years", // md
        "A75": ".. >= 7 years"       // sr
      }
    },
    {
      "nombre": "Attribute 8: Installment rate in percentage of disposable income",
      "tipo": "numérico",
      "descripcion_valores": "Tasa de cuota en porcentaje del ingreso disponible"
      // 1 --> lowest
      // 3 --> low-mid
      // 2 --> mid-high
      // 4 --> highest
    },
    {
      "nombre": "Attribute 9: Personal status and sex",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A91": "male : divorced/separated",           // male
        "A93": "male : single",                       // male
        "A94": "male : married/widowed",              // male
        "A92": "female : divorced/separated/married", // female
        "A95": "female : single"                      // female
      }
    },
    {
      "nombre": "Attribute 10: Other debtors / guarantors",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A101": "none",         // none
        "A102": "co-applicant", // co-applicant
        "A103": "guarantor"     // guarantor
      }
    },
    {
      "nombre": "Attribute 11: Present residence since",
      "tipo": "numérico",
      "descripcion_valores": "Tiempo en la residencia actual (en años)"
    },
    {
      "nombre": "Attribute 12: Property",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A121": "real estate",                                                       // high
        "A122": "if not A121 : building society savings agreement / life insurance", // mid
        "A123": "if not A121/A122 : car or other, not in attribute 6",               // mid
        "A124": "unknown / no property"                                              // low
      }
    },
    {
      "nombre": "Attribute 13: Age in years",
      "tipo": "numérico",
      "descripcion_valores": "Edad en años"
    },
    {
      "nombre": "Attribute 14: Other installment plans",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A141": "bank",    // bank
        "A142": "stores",  // stores
        "A143": "none"     // none
      }
    },
    {
      "nombre": "Attribute 15: Housing",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A151": "rent",    // rent
        "A152": "own",     // own
        "A153": "for free" // for free
      }
    },
    {
      "nombre": "Attribute 16: Number of existing credits at this bank",
      "tipo": "numérico",
      "descripcion_valores": "Número de créditos existentes en este banco"
    },
    {
      "nombre": "Attribute 17: Job",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A171": "unemployed / unskilled - non-resident",                           // no
        "A172": "unskilled - resident",                                            // no
        "A173": "skilled employee / official",                                     // yes
        "A174": "management / self-employed / highly qualified employee / officer" // yes
      }
    },
    {
      "nombre": "Attribute 18: Number of people being liable to provide maintenance for",
      "tipo": "numérico",
      "descripcion_valores": "Número de personas a las que se debe manutención"
    },
    {
      "nombre": "Attribute 19: Telephone",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A191": "none",                                    // no
        "A192": "yes, registered under the customers name" // yes
      }
    },
    {
      "nombre": "Attribute 20: foreign worker",
      "tipo": "cualitativo",
      "descripcion_valores": {
        "A201": "yes",                                     // yes
        "A202": "no"                                       // no
      }
    }
]
```


## References
* [Dataframe](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data)