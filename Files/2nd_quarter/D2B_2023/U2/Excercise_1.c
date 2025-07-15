// Este programa funciona para dar la distancia entre dos puntos

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(){
    system("cls");
    int xp1, yp1, xp2, yp2;
    float resultado;

    printf("Ingresa el valor de x para el punto 1: "); //x en P1
    scanf("%d",&xp1);

    printf("Ingresa el valor de y para el punto 1: "); //y en P1 
    scanf("%d",&yp1);

    printf("\nIngresa el valor de x para el punto 2: "); //x en P2
    scanf("%d",&xp2);

    printf("Ingresa el valor de y para el punto 2: "); //y en P2
    scanf("%d",&yp2);

    resultado = sqrt(((pow((xp2 - xp1),2))+(pow((yp2 - yp1),2))));

    printf("\nEl resultado es: %.2f",resultado);

}