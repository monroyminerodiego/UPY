/*PROGRAMA PARA GENERAR UN NÚMERO AL AZAR Y PEDIR QUE USUARIO LO ADIVINE*/
// Se declaran las librerias
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Se declara la variable de repeticion para el bucle while
char repetir[1] = "s";

// Se declara el main
int main(){

    // Se declara el bucle while para repetir el juego cuantas veces desee el usuario
    while (strcmp(repetir,"s") == 0){
        // Se limpia consola para jugar
        system("cls");

        // Se declaran las variables necesarias
        int numero = rand()%31, adivinanza, intentos = 1;
        char pista[6];

        // Se imprime el titulo del programa y se pide al usuario que ingrese su adivinanza
        printf("--------------- NUMERO AL AZAR ---------------\nIngresa un numero del 1 al 30: ");
        scanf("%d",&adivinanza);

        /*Se hace un condicional para evaluar si el número que ingreso usuario es correcto.
        En caso de que no lo sea, le da 3 oportunidades más para adivinar*/
        if (numero == adivinanza){
            printf("Felicidades, adivinaste al primer intento...!!! :D");
        } else {
            // Bucle para darle en total los 4 intentos
            while ((numero != adivinanza) & (intentos < 4)){
                // Condicional para evaluar si es mayor o menor la adivinanza que el número
                if (numero > adivinanza){
                    strcpy(pista,"mayor");
                } else{
                    strcpy(pista,"menor");
                }
                // Imprime que esta equivocado, te da la pista y vuelve a pedir el número
                printf("Equivocado, el numero es %s.\tTe quedan %d intentos\nVuelve a intentar: ",pista,4-intentos);
                scanf("%d",&adivinanza);
                intentos ++;
            }

            /*Si se adivino el número, entonces imprime los intentos,
            Sino, imprime el número*/
            if (numero == adivinanza){
                printf("\nTe costo %d intentos para adivinar :o",intentos);
            } else if (intentos>3){
                printf("\nJAJAJAJA no pudiste ganarme :/\nMi numero era %d",numero);
            }
        }

        // Se pregunta a usuario si desea seguir jugando
        printf("\n\n\nQuieres volver a jugar? (s/n): ");
        scanf("%s",&repetir);
    }


    // Fin del programa
    return 0;
}