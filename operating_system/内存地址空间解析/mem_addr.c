#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

const int A = 0;    //global var
static int B = 0;    //static global var

int main(void) {

	int a = 0;      //local var
	printf("PID = %d\n",getpid());

	printf("location of code : %p\n", main);
	printf("location of date:\n");
	printf("const int A = 0         A_addr= %p\n",&A);
	printf("static int B = 0         B_addr= %p\n",&B);
	printf("location of stack:\n ");
	printf("int a = 0                a_addr= %p\n",&a);
	int *heap = malloc(100e6);
	printf("location of heap : %p\n", heap);
	while(1==1){}
//	pause();
	free(heap);
	return 0;
}

