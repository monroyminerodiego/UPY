/*Declaracion de headers*/
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

/*Declaracion de funciones*/
float suma(float x,float y);
float resta(float x,float y);
float multi(float x,float y);
float divi(float x,float y);
float cuad(float x);

/*Declaracion de main*/
int main(){

    char repetir[1] = "y";
    do{
        system("cls");
        int eleccion;
        float x,y, resultado;
        printf("----- SUMA / RESTA / MULTIPLICACION / DIVISION / CUADRADO -----\n1) Sumar\n2) Restar\n3) Multiplicar\n4) Dividir\n5) Elevar al cuadrado\nSelecciona una opcion: ");
        scanf("%d",&eleccion);
        while (eleccion > 5 || eleccion < 1){
            printf("Opcion incorrecta. Favor de ingresar una opcion valida: ");
            scanf("%d",&eleccion);
        }

        if (eleccion <= 4){
            printf("\nInserta el valor del primer numero: ");
            scanf("%f",&x);
            printf("Inserta el valor del segundo numero: ");
            scanf("%f",&y);
        } else {
            printf("\nInserta el valor del primer numero: ");
            scanf("%f",&x);
        }

        switch (eleccion)
        {
        case 1:
            resultado = suma(x,y);
            break;
        case 2:
            resultado = resta(x,y);
            break;
        case 3:
            resultado = multi(x,y);
            break;
        case 4:
            resultado = divi(x,y);
            break;
        case 5:
            resultado = cuad(x);
            break;
        }

        printf("\nEl resultado es %.2f",resultado);

        printf("\n\n\nDesea hacer otra operacion? (y/n): ");
        scanf("%s",&repetir);

    } while (strcmp(repetir,"y") == 0);

    return 0;
}

float suma(float x,float y){
    return x+y;
}
float resta(float x,float y){
    return x-y;
}
float multi(float x,float y){
    return x*y;
}
float divi(float x,float y){
    return x/y;
}
float cuad(float x){
    return x*x;
}