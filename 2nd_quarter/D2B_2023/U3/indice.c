#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

float imc(float peso, float estatura);
char* estado(float indice);

int main(){
    system("cls");

    /*Declaracion de variables*/
    float peso, estatura;

    /*Recopilacion de información de usuario*/
    printf("---------- Indice Masa Corporal (IMC) ----------\nIngresa el peso en kg: ");
    scanf("%f",&peso);
    printf("Ingresa la estatura en metros: ");
    scanf("%f",&estatura);

    /*Impresion de resultados en pantalla*/
    float indice = imc(peso,estatura);
    char* consideracion = estado(indice);
    printf("\nEl IMC es de %.2f y eso es considerado: %s",indice,consideracion);

    /*Fin de programa*/
    return 0;
}

float imc(float peso, float estatura){
    return (peso)/pow(estatura,2);
}

char* estado(float indice){
    if (indice < 18.0){
        return "Peso Bajo";
        // strcpy(detalle,"Peso Bajo");
    }else if (indice >= 18.0 & indice <= 24.9){
        return "Normal";
        // strcpy(detalle,"Normal");
    }else if (indice >= 25.0 & indice <= 26.9){
        return "Sobrepeso";
        // strcpy(detalle,"Sobrepeso");
    }else if (indice >= 27 & indice <= 29.9 ){
        return "Obesidad Grado I";
        // strcpy(detalle,"Obesidad Grado I");
    }else if (indice >= 30 & indice <= 39.9 ){
        return "Obesidad Grado II";
        // strcpy(detalle,"Obesidad Grado II");
    }else{
        return "Obesidad Grado III";
        // strcpy(detalle,"Obesidad Grado III");
    }
}