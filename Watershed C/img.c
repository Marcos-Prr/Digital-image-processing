#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

//decodifica uma imagem PGM.
PGM ler_imagem(FILE *arq, PGM img) {
	fscanf(arq, "%s", img.chave);
	fscanf(arq, "%hu %hu %hhu", &img.l, &img.c, &img.max);

	img.mtr = malloc(img.l * img.c * sizeof(unsigned char));
	if(!img.mtr) {
		printf("Não foi possível alocar memória para a matriz da imagem.\n");
		exit(1);
	}

	ler_matriz(arq, img);

	return img;
}

//lê a matriz de uma imagem PGM, de acordo com seu tipo.
void ler_matriz(FILE *arq, PGM img) {
	if((*(img.chave) == 'P') && (*(img.chave + 1) == '2')) {
		ler_mtr_p2(arq, img.mtr, img.l, img.c);
	} else if((*(img.chave) == 'P') && (*(img.chave + 1) == '5')) {
		ler_mtr_p5(arq, img.mtr, img.l, img.c);
	} else {
		printf("Formato inválido ou não identificado.\n");
		exit(1);
	}
}

//lê matriz P2 (ascii).
void ler_mtr_p2(FILE *arq, unsigned char *mtr, unsigned short l, unsigned short c) {
	register int i, j;
	for(i = 0; i < l; i++) {
		for(j = 0; j < c; j++) {
			fscanf(arq, "%hhu", (mtr + (i * c) + j));
		}
	}
}

//lê matriz P5 (bin).
void ler_mtr_p5(FILE *arq, unsigned char *mtr, unsigned short l, unsigned short c) {
	register int i, j;
	for(i = 0; i < l; i++) {
		for(j = 0; j < c; j++) {
			fread((mtr + (i * c) + j), 1, 1, arq);
		}
	}
}

//imprime a matriz de uma imagem PGM.
void imprimir_mtr(unsigned char *mtr, unsigned short l, unsigned short c) {
	register int i, j;
	for(i = 0; i < l; i++) {
		for(j = 0; j < c; j++) {
			printf("%3hhu ", *(mtr + (i * c) + j));
		}
		printf("\n");
	}
}