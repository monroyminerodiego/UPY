# Data Imports

## Instructions given by teacher 
Ejercicio de importación de datos en múltiples plataformas y lenguajes:
Subir un reporte de instalación de las herramientas y evidencia de los datos importados.

Instalar las siguientes aplicaciones (cualquier versión y cuando aplique):
* Excel
* JavaScript
* PowerBI
* R
* SQL (Cualquier manejador de bases de datos)

## Development
### Excel
1. We need to download the app. We can download it from [Microsoft Excel](https://www.microsoft.com/es-mx/microsoft-365/excel):  
<img src='Excel/download.png'>  
<br>

2. Once it is installed, the first thing you'll see (after the initial configuration), is a screen like this:  
<img src='Excel/First_page.png'>  
Then we need to click on "Abrir" or "Open".  
<br>

3. The next interface you'll see is something like the next one, where we need to click in "Examinar" to open a File Explorer.  
<img src='Excel/Open.png'>  
<br>

4. Once we navigate to the directory where our CSV File is located, we select it.
<img src='Excel/Selected_file.png'>  
<br>

5. Finally, our information will be displayed and imported to Excel.
<img src='Excel/data_import.png'>  
<br>



### JS (JavaScript) - Node JS
1. We need to download Node JS. We can download ir from [Node JS | Download](https://nodejs.org/es):
<img src='JS/Images/download.png'>  
<br>

2. Once it is downloaded and installed, we need to open a terminal and navigate to the location of our project. With the following lines we initialize a project and we install the library 'csv-parse':  
``` cmd
<!-- Initializing a project -->
npm init -y

<!-- Installing 'csv-parse' -->
npm install csv-parse
```  
<br>

3. Once we install the required library, we can run the next script to make a Data Import:
``` js
// Sentence to print in console the header of the activity
console.log("First Data Import in JavaScript!\n\n") 

// Declaration of libraries
const { readFileSync } = require('fs') 
const { parse } = require('csv-parse/sync')

// Declaration of a variable with the data of our CSV File
const fileContent = parse(
    readFileSync('data_imports.csv','UTF-8'),{
    columns: true,
    cast: (value, context) => {
        if (context.column === 'Id') return Number(value)
        return value
        }
    }
)

// Sentence to print in console the data of our CSV File
console.log(fileContent)
```  
<br>

4. To run our script, we can do it from console:
``` cmd
node main.js
```  
<br>

5. The output of the script will be something like this:
<img src='JS/Images/output.png'>  
<br>



### PowerBi
1. We need to access to [Power Bi](https://powerbi.microsoft.com/es-mx/landing/free-account/?ef_id=_k_CjwKCAjw4P6oBhBsEiwAKYVkq8K6jcRKoTCI7a1Tk0wwfqI1ipRcbg2y5Nqe8MqiEXde2VmY1Ruk_RoCO7sQAvD_BwE_k_&OCID=AIDcmm2lib5waq_SEM__k_CjwKCAjw4P6oBhBsEiwAKYVkq8K6jcRKoTCI7a1Tk0wwfqI1ipRcbg2y5Nqe8MqiEXde2VmY1Ruk_RoCO7sQAvD_BwE_k_&gclid=CjwKCAjw4P6oBhBsEiwAKYVkq8K6jcRKoTCI7a1Tk0wwfqI1ipRcbg2y5Nqe8MqiEXde2VmY1Ruk_RoCO7sQAvD_BwE) and start a free trial:
<img src='PowerBi/Trial.png'>  
<br>

2. Then we create an account:
<img src='PowerBi/account.png'>  
<br>

3. Once we create an account, we will be redirected to their landing page:
<img src='PowerBi/First_page.png'>  
Then, we click on "Nuevo informe" to import data  
<br>

4. When clicked, a 
<img src='PowerBi/paste.png'>  
<br>

5. 
<img src='PowerBi/data_pasted.png'>  
<br>

## Made By
- Diego Monroy Minero