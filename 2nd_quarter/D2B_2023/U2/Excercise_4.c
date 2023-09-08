#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(){
    // Se limpia consola
    system("cls");

    // Se declaran variables a usar y se pregunta por el número total de datos del array
    int elements;
    printf("-------------- EXCERCISE 4.1 - NUMBERS BETWEEN 15 & 50 --------------\nHow many numbers are you going to enter: ");
    scanf("%i",&elements);
    printf("\n");
    int list[elements];


    // Se van pidiendo los valores de la lista
    for(int ind = 1; ind<=elements; ind++){
        int value;
        printf("\nEnter the %i number: ",ind);
        scanf("%i",&value);
        // Se evalua que el número sea positivo
        while (value<0){
            printf("Oops...! The number must be a positive integer :(\nTry again...!: ");
            scanf("%i",&value);
        }
        
        list[ind-1] = value;
    }

    // Se obtiene el size del array
    int size = sizeof(list)/sizeof(list[0]);

    // Se imprime la lista introducida por usuario
    printf("\nThe array is from %i numbers: {",size);
    for (int i = 0; i < size; i++){
        printf("%i,",list[i]);
    }
    printf("}");

    // Se hace un bucle con el len del array y se declaran las variables
    int menor_quince = 0, mayor_cincuenta = 0, enmedio = 0;
    for (int i = 0; i < size; i++){
        if (list[i]<15){
            menor_quince += 1;
        } else if (list[i]>=15 & list[i]<=30){
            enmedio += 1;
        } else {
            mayor_cincuenta += 1;
        }
    } 

    // Se imprime el contador final del array
    printf("\n- There's %i numbers < 15\n- There's %i numbers between 15 and 50 (Including them)\n- There's %i numbers > 50\n\n\n\n\n",menor_quince,enmedio,mayor_cincuenta);


    // Se vuelve a imprimir el titulo para el otro ejercicio
    printf("-------------- EXCERCISE 4.2 - HEIGHTS --------------\n");

    // Se declaran las variables
    int alturas[5];
    int mas_170 = 0;
    float promedio = 0.00;

    // Se declara un bucle for para ir pidiendo las alturas
    for (int i = 0; i < 5; i++){
        int altura;
        printf("\nHeight of the %i student: ",i+1);
        scanf("%i",&altura);

        while (altura < 110 || altura > 220){
            printf("Oops...! The height must be an integer between 110 - 220 :(\nTry again...!: ");
            scanf("%i",&altura);
        } 
        
        if (altura > 170){
            mas_170 += 1;
        }

        alturas[i] = altura;
    }

    // Bucle para sacar la estatura promedio del grupo con un bucle for
    for (int i = 0; i < 5; i++){
        promedio += alturas[i];
    }
    promedio = promedio/5;

    // Se imprimen toda la información
    printf("\nThe heights of the students are {");
    for (int i = 0; i <5; i++){
        printf("%i, ",alturas[i]);
    }
    printf("}, Which:\n- %i are taller than 170 :p\n- %.2f is the average height... :O\n\n\n\n\n",mas_170,promedio);

    // Fin del programa
    return 0;
}