/*Programa que puede calcular el area y el perimetro de una circunferencia a partir del valor del radio*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*Declaracion de las funciones a usar*/
float area(float radio);
float perimetro(float radio);

/*Declaracion del Main*/
int main(){
    
    /*Declaracion de las variables necesarias para que el programa funcione*/
    float radio;
    char repetir[1], eleccion[1];


    /*Bucle para repetir el proceso cuantas veces quiera el usuario*/
    do{
        /*En cada bucle se limpia la consola*/
        system("cls");

        /*Se piden los datos necesarios de usuario*/
        printf("---------- AREA / PERIMETRO A PARTIR DEL RADIO DE UNA CIRCUNFERENCIA----------\na) Area\np) Perimetro\nSelecciona una opcion: ");
        scanf("%s",&eleccion);
        while (strcmp(eleccion,"a") != 0 & strcmp(eleccion,"A") != 0 & strcmp(eleccion,"p") != 0 & strcmp(eleccion,"P")){
            printf("Eleccion incorrecta... Vuelve a intentarlo: ");
            scanf("%s",&eleccion);
        }
        
        printf("\nIngresa el radio: ");
        scanf("%f",&radio);

        /*Condicional para mostrar el resultado a usuario*/
        if (strcmp(eleccion,"a") == 0 || strcmp(eleccion,"A") == 0){
            printf("\nEl area de la circunferencia con un radio de %.2f unidades es: %.2f",radio,area(radio));
        }else if (strcmp(eleccion,"p") == 0 || strcmp(eleccion,"P") == 0){
            printf("\nEl perimetro de la circunferencia con un radio de %.2f unidades es: %.2f",radio,perimetro(radio));
        }

        /*Validacion para condicion de bucle DO - WHILE*/
        printf("\n\nVolver a hacer un calculo (s/n): ");
        scanf("%s",&repetir);
        if (strcmp(repetir,"s") != 0 & strcmp(repetir,"S") != 0 & strcmp(repetir,"n") != 0 & strcmp(repetir,"N") != 0){
            printf("Tomare eso como un no...");
        }

    } while (strcmp(repetir,"s") == 0 || strcmp(eleccion,"S") == 0);


    /*Fin del programa*/
    printf("\n\n\nHasta luego...!!! ;*");
    return 0;
}

/*Declaracion de la funcion que calcula el area*/
float area(float radio){
    /*Declaracion de las variables que usaremos*/
    #define PI 3.14159
    return PI * radio * radio;
}

/*Declaracion de la funcion que calcula el area*/
float perimetro(float radio){
    /*Declaracion de las variables que usaremos*/
    #define PI 3.14159
    return 2 * PI * radio;   
}