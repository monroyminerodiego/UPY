// Este programa calcula la conversion de grados a radianes, imprime el tipo de angulo
// que se ingreso y valida que el input sea válido

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(){
    // Se limpia cualquier residuo de output en la consola
    system("cls");

    // Se declaran las variables
    float angle,radians;

    // Se imprime el titulo y se pide a usuario ingresar un angulo
    printf("-------------- EXCERCISE 2.- ANGLES --------------\nEnter an angle (0 - 360): ");
    scanf("%f",&angle);

    // Condicional que evalua si el angulo ingresado es valido
    if (angle>=0 & angle<=360){
        // Convierte el angulo a radianes e imprime en consola la conversion
        radians = (angle) * ((3.141592)/(180));
        printf("%.2f grades are equal to %.2f radians :D\n\n",angle,radians);

        // ------------ COMIENZA CONDICIONAL DE TIPO DE ANGULO ------------
        char* tipo; //Variable para guardar el tipo de angulo

        if (angle == 0){
            tipo = "Null";
        } else if (angle > 0 & angle < 90){
            tipo = "Acute";
        } else if (angle == 90){
            tipo = "Right";
        } else if (angle > 90 & angle < 180){
            tipo = "Obtuse";
        } else if (angle == 180){
            tipo = "Flat";
        } else if(angle>180 & angle<360){
            tipo = "Concave";
        } else {
            tipo = "Complete";
        }
        
        // Imprime que tipo de angulo es
        printf("Aaaaaaandd... the angle you enter is %s\n\n", tipo);

    } else {
        // Imprime en consola que no fue un angulo valido
        printf("Oh!, the angle has no classification :(\n\n");
    }


    return 0;
}