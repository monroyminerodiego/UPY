#include <stdio.h>
#include <stdlib.h>

int main(){
    system("cls");
    
    char nombre[23];
    int edad;
    printf("Hello world\nWhat's your name? ");
    
    scanf("%s",&nombre);
    printf("\nNice to meet you %s, How old are you?: ",nombre);
    
    scanf("%d",&edad);
    printf("\nIt's cool that you're %d, I'm 20 years old!",edad);

    return 0;
}