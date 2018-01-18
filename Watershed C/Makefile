all: watershed.e

watershed.e: main.o img.o fila.o wshed.o
	gcc -o watershed.e main.o img.o fila.o wshed.o

main: main.c lib.h
	gcc -o main.o -c main.c

img: img.c lib.h
	gcc -o img.o -c img.c

fila: fila.c lib.h
	gcc -o fila.o -c fila.c

wshed: wshed.c lib.h
	gcc -o wshed.o -c wshed.c

clear:
	rm -f watershed.e *.o