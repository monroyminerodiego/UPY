// PROGRAMA QUE CALCULA LA POLIZA DE UN SEGURO DEPENDIENDO 3 DIVERSOS FACTORES
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>

int main(){
    system("cls");

    // Se declaran variables necesarias
    char plan[1], alcohol[1];
    int edad, poliza, diez, ocho;

    // Se imprime el titulo y las preguntas
    printf("--------------- EJERCICIO 5.- POLIZA DE SEGUROS ---------------\nSelecciona tu poliza...\nA) Cobertura Amplia\tB) Da\xF1os a Terceros\n");
    scanf("%s",&plan);

    while(strcmp(plan,"a")!=0 & strcmp(plan,"A")!=0 & strcmp(plan,"b")!=0 & strcmp(plan,"B")!=0){
        printf("Ooops...! Elige una opcion entre A o B\nIntenta de nuevo...!:",plan);
        scanf("%s",&plan);
    }

    printf("\nIngresa tu edad (0 - 99): ");
    scanf("%i",&edad);
    while(edad < 0 || edad > 99){
        printf("Ooops...! La edad debe ser un entero ente 0 y 99\nIntenta de nuevo...!:");
        scanf("%i",&edad);
    }
    
    printf("\nAcostumbras a beber alcohol? (Y/N): ");
    scanf("%s",&alcohol);
    while(strcmp(alcohol,"y")!=0 & strcmp(alcohol,"Y")!=0 & strcmp(alcohol,"n")!=0 & strcmp(alcohol,"N")!=0){
        printf("Ooops...! Y - Si\tN - No\nIntenta de nuevo...!: ");
        scanf("%s",&alcohol);
    }

    // Se preparan los costos para hacer la suma total
    if (plan == "a" || plan == "A"){
        poliza = 1200;
        diez = 120;
        ocho = 96;
    } else {
        poliza = 950;
        diez = 95;
        ocho = 76;
    }

    // Se validan las condiciones
    if (alcohol == "y" || alcohol == "Y"){
        poliza == poliza+diez;
    }
    if (edad > 50){
        poliza == poliza+ocho;
    }

    // Se imprime el output
    printf("\n\nTomando en cuenta las preguntas previas, la contratacion de la poliza seria por un total de $%i",poliza);

    // Fin del programa
    return 0;
}