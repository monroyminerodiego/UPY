// Programa para convertir la temperatura en grados Fahrenheit a Celcius
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(){
    // Se limpia la consola
    system("cls");

    // Se declara la variable donde se guarda la temperatura ingresada por usuario
    float temp;
    
    // Se imprime el titulo y se hace la pregunta
    printf("-------------- EXCERCISE 3.- TEMPERATURE --------------\nEnter an temperature in Fahrenheit: ");
    scanf("%f",&temp);
    
    // Se hace la conversion de °C a °F
    temp = (temp - 32) * 5/9;

    // Se imprime el resultado de la conversion
    printf("\nThe temperature you enter is equal to %.2f Celcius degrees", temp);

    // Se hace un condicional para evaluar la temperatura e imprimir su clasificacion
    if (temp >= 20 & temp <= 25){
        printf("\nTemperature is Ideal! :D");
    } else if (temp>25 & temp <= 32 ){
        printf("\nTemperature is dangerous! :)");
    } else if (temp > 32) {
        printf("\nTemperature is contraindicated! :O");
    } else {
        printf("\nTemperature is not classified");
    }

    // Fin del programa
    return 0;
}