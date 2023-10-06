console.log("First Data Import in JavaScript!\n\n") 

const { readFileSync } = require('fs') 
const { parse } = require('csv-parse/sync')

const fileContent = parse(readFileSync('../../../../DataBases/data_imports.csv','UTF-8'),
{
    columns: true,
    cast: (value, context) => {
        if (context.column === 'Id') return Number(value)
        return value
    }
}
)

console.log(fileContent)