#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

//aloca uma nova fila.
Fila* criar_fila() {
	Fila *fl = (Fila*) malloc(sizeof(Fila));
	fl->inicio = NULL;
	fl->tamanho = 0;
	return fl;
}

int main() {
	Fila *fl = criar_fila();
	inserir_final(fl, 15);
	inserir_final(fl, 16);
	inserir_final(fl, 17);
	imprimir_fila(fl);
	remover_inicio(fl);
	imprimir_fila(fl);

	return 0;
}

//insere um valor no final da fila.
void inserir_final(Fila *fl, int valor) {
	No *novo_no = (No*) malloc(sizeof(No));
	novo_no->valor = valor;
	novo_no->prox = NULL;
	if(fila_vazia(fl)) {
		fl->inicio = novo_no;
		fl->tamanho++;
	} else {
		ultimo_no(fl)->prox = novo_no;
		fl->tamanho++;
	}
}

//remove um valor da fila, de acordo com FIFO.
int remover_inicio(Fila *fl) {
	int valor_removido;
	No *aux1 = fl->inicio;
	No *aux2 = fl->inicio->prox;
	fl->inicio = aux2;
	valor_removido = aux1->valor;
	free(aux1);
	fl->tamanho--;
	return valor_removido;
}

//retorna o ultimo ponteiro da fila.
No* ultimo_no(Fila *fl) {
	No *aux = fl->inicio;
	while(aux->prox != NULL) {
		aux = aux->prox;
	}
	return aux;
}

//retorna 1 (true) ou 0 (false), indicando se a fila está vazia.
int fila_vazia(Fila *fl) {
	return (fl->inicio == NULL);
}

//esvazia a fila e libera a memória alocada.
void liberar_fila(Fila *fl) {
	No *aux1;
	No *aux2;
	while(aux2 != NULL) {
		aux1 = fl->inicio;
		aux2 = fl->inicio->prox;
		fl->inicio = aux2;
		free(aux1);
		fl->tamanho--;
	}
	free(aux2);
}

//imprime a fila.
void imprimir_fila(Fila *fl) {
	No *aux = fl->inicio;
	while(aux != NULL) {
		printf("%d --> ", aux->valor);
		aux = aux->prox;
	}
	printf("\n");
}