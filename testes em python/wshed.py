# -*- coding: utf-8 -*-
import numpy as np
from PIL import Image
from scipy.misc import imsave

# Retorna a lista de vizinhos-8 do ponto p
# ----------------------------------------
# Descrição: Dado um ponto p, retorna uma lista com seus vizinhos-8
#
# Entradas: p       coordenada linear do ponto
#           m       quantidade de linhas da imagem
#           n       quantidade de colunas da imagem
#
# Saídas:   lista de vizinhos-8 do ponto p
def vizinhos(p, m, n):
    if (p == 0):
        return [p + 1, p + n, p + n + 1]

    if (p == (n - 1)):
        return [p - 1, p + n - 1, p + n]

    if (p == (n * (m - 1))):
        return [p - n, p - n + 1, p + 1]

    if (p == ((n * m) - 1)):
        return [p - n - 1, p - n, p - 1]

    for i in range(1, n - 1):
        if (p == i):
            return [p - 1, p + 1, p + n - 1, p + n, p + n + 1]

    for i in range((n * (m - 1)) + 1, (n * m) - 1):
        if (p == i):
            return [p - n - 1, p - n, p - n + 1, p - 1, p + 1]

    for i in range(n, n * (m - 1), n):
        if (p == i):
            return [p - n, p - n + 1, p + 1, p + n, p + n + 1]
        if (p == i + (n - 1)):
            return [p - n - 1, p - n, p - 1, p + n - 1, p + n]

    return [p - n - 1, p - n, p - n + 1, p - 1, p + 1, p + n - 1, p + n, p + n + 1]


# Calcula o histograma de uma imagem
# ----------------------------------
# Entradas: matriz da imagem
#
# Saídas: histograma da imagem; valor de mínimo e máximo de cinza
def hist(im_in):
    # inicializa o vetor de histograma
    histograma = np.zeros(256)

    # inicializa os valores de mínimo e máximo do histograma
    min = max = im_in[0, 0];

    # cria o histograma e acha os valores de mínimo e máximo
    for i in range(im_in.shape[0]):
        for j in range(im_in.shape[1]):
            aux = im_in[i, j]
            histograma[aux] += 1
            if (aux < min): min = aux
            if (aux > max): max = aux

    return histograma, min, max


# Calcula o vetor de endereços da imagem utilizando seu histograma cumulativo
# ----------------------------------
# Entradas: matriz da imagem
#
# Saídas: vetor de endereços, valores mínimo e máximo de cinza
def cumul(im_in):
    # inicializa o vetor do histograma cumulativo
    cumulativo = np.zeros(256)
    ims = np.zeros(im_in.shape[0] * im_in.shape[1]);
    histograma, min, max = hist(im_in)

    for i in range(min+1 , max + 2):
        cumulativo[i] = cumulativo[i-1 ] + histograma[i-1 ]

    v = vetoriza(im_in)

    # calcula o histograma cumulativo e o vetor de endereços
    for i in range(v.shape[0]):
        print('aqui0')
        ims[ cumulativo[v[i]] ] = i
        print ('aqui')
        cumulativo[v[i]] += 1
        print('aqui2')

    return ims, min, max


# Ordena o vetor da imagem por seus níveis de cinza, em ordem crescente
# ---------------------------------------------------------------------
# Entradas: matriz da imagem
#
# Saídas: vetor ordenado, valores mínimo e máximo de cinza
def ordena(im_in):
    enderecos, min, max = cumul(im_in)
    original = vetoriza(im_in)
    saida = vetoriza(np.zeros(im_in.shape))

    for i in range(len(saida)):
        saida[i] = original[enderecos[i]]

    return saida, min, max


# Retorna a representação linear da rasterização (left-right, up-down) da matriz
# ------------------------------------------------------------------------------
# Entradas: matriz da imagem
#
# Saídas: representação linear da matriz
def vetoriza(im_in):
    im_vet = np.array(np.zeros(im_in.shape[0] * im_in.shape[1]))
    count = 0

    for i in range(im_in.shape[0]):
        for j in range(im_in.shape[1]):
            im_vet[count] = im_in[i, j]
            count += 1

    return im_vet.astype(int)


# Operação inversa de vetoriza()
# ------------------------------
# Entradas: representação linear; dimensão m e n da matriz
#
# Saídas: representação matricial
def devetoriza(vet, m, n):
    im_out = np.zeros((m, n))
    cont = 0

    for i in range(m):
        for j in range(n):
            im_out[i, j] = vet[cont]
            cont += 1

    return im_out


# Calcula a transformada de Watershed
# -----------------------------------
# Descrição: Dada uma imagem, calcula sua imagem rotulada, ou seja
#            desenha as linhas divisoras de água
#
# Entradas: im_in   matriz da imagem a ser segmentada
#
# Saídas:   im_out  matriz da imagem rotulada
def wshed(im_in):
    mask = -2  # valor inicial para cada nível de cinza
    wshed = 0  # valor dos pontos que pertencem ao watershed
    init = -1  # valor inicial dos pontos de im_out
    ficticio = -4  # ponto fictício
    curlab = 0  # rótulo corrente

    # inicializa a fila FIFO
    fila = []

    # cria o vetor da a imagem de saída (g) e a aux. de distância (dist)
    rotu = vetoriza(np.zeros(im_in.shape))
    dist = vetoriza(np.zeros(im_in.shape))

    # inicializa g e dist
    for p in range(len(rotu)):
        rotu[p] = init
        dist[p] = 0

    #
    # PARTE 1: ordenação dos pontos por seus níveis de cinza
    #

    # vetor de pontos ordenado e valores de mínimo e máximo de cinza

    x1=vetoriza(im_in)
    ordenados=np.sort(x1)
    hmin = ordenados[0]
    hmax = ordenados[len(ordenados)-1]
    #ordenados, hmin, hmax = ordena(im_in)

    #
    # PARTE 2: alagamento para cada nível h de cinza
    #

    # para cada nível h de cinza...
    for h in range(hmin, hmax + 1):

        # e para cada ponto com nível de cinza h...
        for p in range(len(ordenados)):
            if ordenados[p] == h:
                # todo ponto inicial com o rotulo igual a mask
                rotu[p] = mask
                # seus vizinhos-8 são analizados
                for q in vizinhos(p, im_in.shape[0], im_in.shape[1]):
                    # se algum vizinho já tiver sido analisado ou for wshed...
                    if (rotu[q] > 0) or (rotu[q] == wshed):
                        # ...propaga a dist. geodésica e inclui o ponto na fila
                        dist[p] = 1
                        fila.append(p)

        curdist = 1
        fila.append(ficticio)

        # propaga a bacia
        while (True):
            p = fila.pop(0)
            if (p == ficticio):
                if (len(fila) == 0):
                    break
                else:
                    fila.append(ficticio)
                    curdist += 1
                    p = fila.pop(0)

            # rotula p baseando-se no rótulo dos vizinhos
            for q in vizinhos(p, im_in.shape[0], im_in.shape[1]):
                if (dist[q] < curdist) and (rotu[q] > 0 or rotu[q] == wshed):
                    # vizinho q pertence a uma bacia existente ou é watershed
                    if rotu[q] > 0:
                        if (rotu[p] == mask) or (rotu[p] == wshed):
                            rotu[p] = rotu[q]
                        elif rotu[p] != rotu[q]:
                            rotu[p] = wshed
                    elif rotu[p] == mask:
                        rotu[p] = wshed
                # q é um ponto de um plateau
                elif (rotu[q] == mask) and (dist[q] == 0):
                    dist[q] = curdist + 1
                    fila.append(q)

        # detecta e processa os novos mínimos no nível h
        for p in range(len(ordenados)):
            if ordenados[p] == h:
                # reseta a distância para zero
                dist[p] = 0
                # p está dentro de um novo mínimo
                if (rotu[p] == mask):
                    curlab += 1
                    # cria um novo rótulo
                    fila.append(p)
                    rotu[p] = curlab
                    while (len(fila) != 0):
                        q = fila.pop(0)
                        # inspeciona os vizinhos de q
                        for r in vizinhos(q, im_in.shape[0], im_in.shape[1]):
                            if (rotu[r] == mask):
                                fila.append(r)
                                rotu[r] = curlab

    return devetoriza(rotu, im_in.shape[0], im_in.shape[1])

image = np.array(Image.open('lena2.png'))
x=wshed(image)
imsave('olho.png',x)

