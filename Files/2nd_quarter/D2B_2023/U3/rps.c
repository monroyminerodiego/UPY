/*Programa que juega piedra papel o tijera con el usuario*/

// DECLARACION DE TITULOS
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// VARIABLE PARA REPETIR/ROMPER EL JUEGO
char repetir[1] = "y";

// DECLARACION DEL MAIN
int main(){
    // DECLARACION DEL BUCLE PARA JUGAR PIEDRA PAPEL Y TIJERAS
    while (strcmp(repetir,"y") == 0){
        // Se limpia consola para jugar
        system("cls");
        
        // Se declara la opcion del ordenador y con base en eso, se evalua
        int opcion = rand()%4;
        char computadora[8];
        if (opcion == 0){
            strcpy(computadora,"piedra");
        } else if (opcion == 1){
            strcpy(computadora,"papel");
        } else if (opcion == 2){
            strcpy(computadora,"tijeras");
        }
        // Se declara la variable de usuario junto con el titulo y se pide ingrese el valor
        char usuario[8];
        printf("--------------- PIEDRA / PAPEL / TIJERAS ---------------\nEscoge una opcion entre 'piedra', 'papel' O 'tijeras': ");
        scanf("%s",&usuario);
        while (strcmp(usuario,"piedra") != 0 & strcmp(usuario,"papel") != 0 & strcmp(usuario,"tijeras") != 0){
            printf("Opcion incorrecta, favor de volver a ingresar la opcion: ");
            scanf("%s",&usuario);
        }

        // Se declaran los condicionales para evaluar si el usuario ingreso una opción correcta y ver si gano
        if ((strcmp(usuario,"piedra") == 0 || strcmp(usuario,"papel") == 0 || strcmp(usuario,"tijeras") == 0) & ((strcmp(usuario,"piedra") == 0 & strcmp(computadora,"tijeras") == 0) || (strcmp(usuario,"papel") == 0 & strcmp(computadora,"piedra") == 0) || (strcmp(usuario,"tijeras") == 0 & strcmp(computadora,"papel") == 0))){
            printf("\nMi eleccion fue '%s'\n\nFelicidades, has ganado...!!! :D",computadora);
        }else if((strcmp(usuario,"piedra") == 0 || strcmp(usuario,"papel") == 0 || strcmp(usuario,"tijeras") == 0) & ((strcmp(usuario,"piedra") == 0 & strcmp(computadora,"papel") == 0) || (strcmp(usuario,"papel") == 0 & strcmp(computadora,"tijeras") == 0) || (strcmp(usuario,"tijeras") == 0 & strcmp(computadora,"piedra") == 0))){
            printf("\nMi eleccion fue '%s'\n\nJijiji, te ha ganado el ordenador...!!!",computadora);
        }else if((strcmp(usuario,"piedra") == 0 || strcmp(usuario,"papel") == 0 || strcmp(usuario,"tijeras") == 0) & ((strcmp(usuario,computadora) == 0) || (strcmp(usuario,computadora) == 0) || (strcmp(usuario,computadora) == 0))){
            printf("\nMi eleccion fue '%s'\n\nEmpateeeeee...!!!",computadora);
        } else {
            printf("\nUsuario: %s\nOrdenador: %s",usuario,computadora);
        }
        
        // Se pregunta a usuario si desea volver a jugar
        printf("\n\n\nDeseas volver a repetir el juego? (Y/N): ");
        scanf("%s",&repetir);
    } 

    // FIN DEL PROGRAMA
    return 0;
}