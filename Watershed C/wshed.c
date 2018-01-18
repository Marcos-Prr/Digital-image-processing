#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

unsigned char* wshed(unsigned char *mtr, unsigned short l, unsigned short c) {
	int mask = -2;
	int wshd = 0;
	int init = -1;
	int inqe = -3;
	int levels = 256;
	int curlab = 0;
	int flag = 0;
	Fila *fifo = criar_fila();
	int *labels = (int*) malloc(l * c * sizeof(int));

	for(int i = 0; i < l; i++) {
		for(int j = 0; j < c; j++) {
			*(labels + (i * c) + j) = init;
		}
	}
	
}