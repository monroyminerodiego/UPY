/* ------------------ Program in charge of Create, Read, Update and Delete (CRUD) the inventory of a PC store ------------------ */

// Declaration of the headers
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Declaration of the structure of the list of the inventory
struct inventory {
    int id, stock;
    char *name;
    float price;
    int status;
    struct inventory *next;
};
// Create the list of the inventory
struct inventory *head = NULL;

void create(int id, int stock, char name_u[50], float price);
void read();
void update();
void delete();



// Declaration of the main function
int main(){
    // Variable in charge of repeating the script in a loop
    char repeat[] = "";

    // Declaration of the pre-builded inventory
    create(4,51,"Ryzen_5_5500",1489.4);
    create(3,45,"Intel_Core_i3-12100F",1679.4);
    create(2,41,"Ryzen_3_3200G",1821.4);
    create(1,47,"Ryzen_5_5600X",2469.4);

    // Do - While Loop to start the menu at least 1 time, then it enters the loop every time the user asks for it
    do{
        // Declaration to clean the console
        system("cls");
        
        // Declaration of a variable to manage the election of the user
        char election[] = "";
        printf("---------------------- PC store inventory ----------------------\n\nC) Create new item\nR) Review the inventory\nU) Update an item\nD) Delete an item\n\nPlease, select an option: ");
        scanf("%s",&election);
        // While loop to manage the wrong inputs of users
        while ((strcmp(election,"c") != 0) & (strcmp(election,"r") != 0) & (strcmp(election,"u") != 0) & (strcmp(election,"d") != 0) & (strcmp(election,"C") != 0) & (strcmp(election,"R") != 0) & (strcmp(election,"U") != 0) & (strcmp(election,"D") != 0)){
            printf("Sorry, that's not a valid option. Please enter a valid option of the menu: ");
            scanf("%s",&election);
        }

        // Conditional to select the function according to user's selecction
        if ((strcmp(election,"C")==0) || (strcmp(election,"c") == 0)){
            // Do - While loop to ask user if they want to add a new item
            do {
                // Declaration to clear the console and then print a title with the function name 
                system("cls");
                printf("---------------------- PC store inventory (Create new item) ----------------------\n\n");
                int id, stock;
                char name[100];
                float price;

                printf("Please, enter the name of the item (Remember not to put spaces between): ");
                scanf("%s",&name);

                printf("Please, enter the price of the item: ");
                scanf("%f",&price);

                printf("Please, enter the stock of the item: ");
                scanf("%d",&stock);

                struct inventory *last_node(struct inventory *head);
                struct inventory *current = head;
                while (current->next != NULL){
                    current = current->next;
                }

                id = (current->id)+1;
                create(id, stock, name, price);


                printf("Do you want to add another item? (y/n):");
                scanf("%s",&repeat);
                // While loop to manage the wrong inputs of users
                while ((strcmp(repeat,"y") != 0) & (strcmp(repeat,"n") != 0) & (strcmp(repeat,"Y") != 0) & (strcmp(repeat,"N") != 0)){
                    printf("Sorry, that's not a valid option. Please enter a valid option: ");
                    scanf("%s",&repeat);
                }
            } while ((strcmp(repeat,"y") == 0) || (strcmp(repeat,"Y") == 0));
        
        } else if ((strcmp(election,"R")==0) || (strcmp(election,"r") == 0)){
            // Declaration to clear the console and then print a title with the function name 
            system("cls");
            printf("---------------------- PC store inventory (Review the inventory) ----------------------\n\n\n");
            read();
        
        } else if ((strcmp(election,"U")==0) || (strcmp(election,"u") == 0)){
            // Do - While loop to ask user if they want to update a new item
            do {
                // Declaration to clear the console and then print a title with the function name 
                system("cls");
                printf("---------------------- PC store inventory (Update an item) ----------------------\n\n");
                update();
                printf("Do you want to update another item? (y/n)");
                scanf("%s",&repeat);
                // While loop to manage the wrong inputs of users
                while ((strcmp(repeat,"y") != 0) & (strcmp(repeat,"n") != 0) & (strcmp(repeat,"Y") != 0) & (strcmp(repeat,"N") != 0)){
                    printf("Sorry, that's not a valid option. Please enter a valid option: ");
                    scanf("%s",&repeat);
                }
            } while ((strcmp(repeat,"y") == 0) || (strcmp(repeat,"Y") == 0));
        
        } else if ((strcmp(election,"D")==0) || (strcmp(election,"d") == 0)){
            // Do - While loop to ask user if they want to delete a new item
            do {
                // Declaration to clear the console and then print a title with the function name 
                system("cls");
                printf("---------------------- PC store inventory (Delete an item) ----------------------\n\n");
                delete();
                printf("Do you want to delete another item? (y/n)");
                scanf("%s",&repeat);
                // While loop to manage the wrong inputs of users
                while ((strcmp(repeat,"y") != 0) & (strcmp(repeat,"n") != 0) & (strcmp(repeat,"Y") != 0) & (strcmp(repeat,"N") != 0)){
                    printf("Sorry, that's not a valid option. Please enter a valid option: ");
                    scanf("%s",&repeat);
                }
            } while ((strcmp(repeat,"y") == 0) || (strcmp(repeat,"Y") == 0));
        }

        // Ask user if they want to do something else
        printf("\n\nDo something else? (y/n): ");
        scanf("%s",&repeat);
        // While loop to manage the wrong inputs of users
        while ((strcmp(repeat,"y") != 0) & (strcmp(repeat,"n") != 0) & (strcmp(repeat,"Y") != 0) & (strcmp(repeat,"N") != 0)){
            printf("Sorry, that's not a valid option. Please enter a valid option: ");
            scanf("%s",&repeat);
        }

    } while ((strcmp(repeat,"y") == 0) || (strcmp(repeat,"Y") == 0));


    // Visual confirmation of the exit of the CRUD
    printf("\n\n\n\nBye bye...!!! :D\n");
    // End of the script
    return 0;
}


// Development of the functions
void create(int id, int stock, char name_u[50], float price) {

    struct inventory *new_item = malloc(sizeof(struct inventory));
    new_item->id = id;
    new_item->stock = stock;
    new_item->name = name_u;
    new_item->price = price;
    new_item->next = head;
    new_item->status = 1;
    head = new_item;

    printf("'%s' added succesfully!\n\n",name_u);
}

void read() {
    struct inventory *current = head;
    printf("ID ----- NAME ----- PRICE ----- STOCK\n\n");
    while (current != NULL) {
        if (current->status == 1){
            printf("%d ----- %s ----- %.2f ----- %d\n",current->id,current->name,current->price,current->stock);
            current = current->next;
        } else {
            current = current->next;
            continue;
        }
    }
}

void update(){
    read();
    int id_update,new_stock;
    float new_price;
    char new_name[100];
    printf("\n\nThis is the inventory. Please select the ID of the item you want to update: ");
    scanf("%d",&id_update);

    struct inventory *current_node = head;
    while(current_node->id != id_update){
        current_node = current_node->next;
    }
    
    printf("Please, enter the update of the name of the item (Remember not to put spaces between): ");
    scanf("%s",&new_name);

    printf("Please, enter the update of the price of the item: ");
    scanf("%f",&new_price);

    printf("Please, enter the update of the stock of the item: ");
    scanf("%d",&new_stock);

    strcpy(current_node->name,new_name);
    current_node->price = new_price;
    current_node->stock = new_stock;

    printf("\n'%s' updated succesfully!\n\n",new_name);
}

void delete(){
    read();
    int id_delete;
    printf("\n\nThis is the inventory. Please select the ID of the item you want to delete: ");
    scanf("%d",&id_delete);
    
    struct inventory *current_node = head;
    while (current_node->id != id_delete){
        current_node = current_node->next;
    }
    current_node->status = 0;

    system("cls");
    printf("---------------------- PC store inventory (Delete an item) ----------------------\n\n");
    printf("Item deleted succesfully!\n\n");

}
