/*
 * CYBERDUNE - heap0 (modified)
 * Author: Abrxs, pr1or1tyQ (modified)
 *
 * Changes:
 * - Replaced initial input string "pico" with "CYBERDUNE" label.
 * - Increased FLAGSIZE_MAX to allow longer flags.
 * - Added an automatic alarm to terminate the instance after 180 seconds (3 minutes).
 *
 * Note: This intentionally preserves the heap overflow vulnerability:
 *       scanf("%s", input_data) is unbounded for demonstration / challenge usage.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>

#define FLAGSIZE_MAX 128
/* amount of memory allocated for input_data */
#define INPUT_DATA_SIZE 5
/* amount of memory allocated for safe_var */
#define SAFE_VAR_SIZE 5

int num_allocs;
char *safe_var;
char *input_data;

void check_win() {
    if (strcmp(safe_var, "bico") != 0) {
        printf("\nYOU WIN\n");

        /* Print flag */
        char buf[FLAGSIZE_MAX];
        FILE *fd = fopen("flag.txt", "r");
        if (!fd) {
            printf("flag file missing\n");
            fflush(stdout);
            exit(0);
        }
        fgets(buf, FLAGSIZE_MAX, fd);
        printf("%s\n", buf);
        fflush(stdout);

        exit(0);
    } else {
        printf("Looks like everything is still secure!\n");
        printf("\nNo flage for you :(\n");
        fflush(stdout);
    }
}

void print_menu() {
    printf("\n1. Print Heap:\t\t(print the current state of the heap)"
           "\n2. Write to buffer:\t(write to your own personal block of data "
           "on the heap)"
           "\n3. Print safe_var:\t(I'll even let you look at my variable on "
           "the heap, "
           "I'm confident it can't be modified)"
           "\n4. Print Flag:\t\t(Try to print the flag, good luck)"
           "\n5. Exit\n\nEnter your choice: ");
    fflush(stdout);
}

void init() {
    printf("\nWelcome to CYBERDUNE - heap0!\n");
    printf(
        "I put my data on the heap so it should be safe from any tampering.\n");
    printf("Since my data isn't on the stack I'll even let you write whatever "
           "info you want to the heap, I already took care of using malloc for "
           "you.\n\n");
    printf("Note: This instance will auto-terminate after 180 seconds.\n\n");
    fflush(stdout);

    /* auto-terminate after 3 minutes to satisfy the 3-min requirement */
    alarm(180);

    input_data = malloc(INPUT_DATA_SIZE);
    strncpy(input_data, "CYBERDUNE", INPUT_DATA_SIZE);
    safe_var = malloc(SAFE_VAR_SIZE);
    strncpy(safe_var, "bico", SAFE_VAR_SIZE);
}

void write_buffer() {
    printf("Data for buffer: ");
    fflush(stdout);
    scanf("%s", input_data);
}

void print_heap() {
    printf("Heap State:\n");
    printf("+-------------+----------------+\n");
    printf("[*] Address   ->   Heap Data   \n");
    printf("+-------------+----------------+\n");
    printf("[*]   %p  ->   %s\n", input_data, input_data);
    printf("+-------------+----------------+\n");
    printf("[*]   %p  ->   %s\n", safe_var, safe_var);
    printf("+-------------+----------------+\n");
    fflush(stdout);
}

int main(void) {

    /* Setup */
    init();
    print_heap();

    int choice;

    while (1) {
        print_menu();
        int rval = scanf("%d", &choice);
        if (rval == EOF){
            exit(0);
        }
        if (rval != 1) {
            exit(0);
        }

        switch (choice) {
        case 1:
            /* print heap */
            print_heap();
            break;
        case 2:
            write_buffer();
            break;
        case 3:
            /* print safe_var */
            printf("\n\nTake a look at my variable: safe_var = %s\n\n",
                   safe_var);
            fflush(stdout);
            break;
        case 4:
            /* Check for win condition */
            check_win();
            break;
        case 5:
            /* exit */
            return 0;
        default:
            printf("Invalid choice\n");
            fflush(stdout);
        }
    }
}
