#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

int main(int argc, char **argv) {
	FILE *arq;
	PGM img;

	if(argc != 2) {
		printf("Uso: %s nome_da_imagem\n", *argv);
		exit(1);
	}

	if(!(arq = fopen(*(argv+1), "rb"))) {
		printf("Não foi possível abrir o arquivo.\n");
		exit(1);
	}

	img = ler_imagem(arq, img);

	imprimir_mtr(img.mtr, img.l, img.c);

	free(img.mtr);
	fclose(arq);

	return 0;
}