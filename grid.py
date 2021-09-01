import pygame as pg
import variaveis as var
from random import randint
import numpy as np
import copy

class Tabuleiro():
    def __init__(self):
        self.gapCima = var.TAMANHO_Y_MENU # Distancia entre o tabuleiro e o topo da janela
        self.gapLados = 0 # Distancia entre o tabuleiro e as bordas da janela
        self.gridCores = self.definirGrid(var.quantidadeGridX, var.quantidadeGridY)

        # Define as proporções dos objetos que pertencem ao tabuleiro
        self.defineTamanhoTela()

        self.pausado = True # Simulação pausada ou não
        self.cursorAparece = True # Cursor habilitado a aparecer ou não
        self.mouseForaTela = True # Mouse esta ou não colidindo com o tabuleiro
        
        self.corSelecionada = [255, 255, 255] # Cor atual selecionada
        self.pontosMouse = {"posX": 0, "posY": 0, "cor": self.corSelecionada} # Posição e cor do quadrado que segue o ponteiro do mouse

        self.pontos = [] # Pontos colocados no tabuleiro
        
        self.gridFuturo = self.definirGrid(var.quantidadeGridX, var.quantidadeGridY) # Usado para atualizar o self.gridCores sem interferir nos calculos de cor
        self.gridPartic = self.definirGrid(var.quantidadeGridX, var.quantidadeGridY) # Partições do grid. Usado para descobrir o posicionamento do mouse

    def defineTamanhoTela(self):
        # Define tamanho do retangulo do grid
        self.tamanhoRect = int(var.TAMANHO_TELA[0]/var.quantidadeGridY)
        if self.tamanhoRect*var.quantidadeGridY > (var.TAMANHO_TELA[1]-self.gapCima) or self.tamanhoRect*var.quantidadeGridX > var.TAMANHO_TELA[0]:
            self.tamanhoRect = int(var.TAMANHO_TELA[0]/var.quantidadeGridX)
        if self.tamanhoRect*var.quantidadeGridY > (var.TAMANHO_TELA[1]-self.gapCima) or self.tamanhoRect*var.quantidadeGridX > var.TAMANHO_TELA[0]:
            self.tamanhoRect = int((var.TAMANHO_TELA[1]-self.gapCima)/var.quantidadeGridY)
        if self.tamanhoRect*var.quantidadeGridY > (var.TAMANHO_TELA[1]-self.gapCima) or self.tamanhoRect*var.quantidadeGridX > var.TAMANHO_TELA[0]:
            self.tamanhoRect = int((var.TAMANHO_TELA[1]-self.gapCima)/var.quantidadeGridX)

        # Define tamanho do gapLados
        self.gapLados = int((var.TAMANHO_TELA[0] - (self.tamanhoRect*var.quantidadeGridX))/2)

        # Define tamanho da hitbox de cada retangulo do grid
        self.rects = self.definirRect()

        # Define tamanho do retangulo geral do grid
        x = self.gapLados
        y = self.gapCima
        tamanhoX = self.tamanhoRect*var.quantidadeGridX
        tamanhoY = self.tamanhoRect*var.quantidadeGridY
        self.rectGeral = pg.Rect((x, y), (tamanhoX, tamanhoY))
        
    def definirGrid(self, tamanhoX, tamanhoY):
        # Cria uma matriz do tamanho do tabuleiro
        matriz = [[[0, 0, 0] for linhas in range(tamanhoY)] for colunas in range(tamanhoX)]
        return matriz
    
    def definirRect(self):
        # Define a hitbox de cada quadrado que compõe o grid
        rects = self.definirGrid(var.quantidadeGridX, var.quantidadeGridY)
        for linha in range(var.quantidadeGridX):
            for coluna in range(var.quantidadeGridY):
                x = linha*self.tamanhoRect + self.gapLados
                y = coluna*self.tamanhoRect + self.gapCima
                rects[linha][coluna] = pg.Rect((x, y), (self.tamanhoRect, self.tamanhoRect))
        return rects

    def draw(self):
        # Desenha na tela o tabuleiro e seus quadrados.
        pg.draw.rect(var.TELA, var.PRETO, self.rectGeral, 3)
        for linha in range(len(self.rects)):
            for coluna in range(len(self.rects[linha])):
                pg.draw.rect(var.TELA, self.gridCores[linha][coluna], self.rects[linha][coluna], 0) # HIT BOX
        if (self.cursorAparece or self.pausado) and not self.mouseForaTela:
            pg.draw.rect(var.TELA, var.PRETO, self.rects[self.pontosMouse["posX"]][self.pontosMouse["posY"]], 3) # HIT BOX
            pg.draw.rect(var.TELA, var.BRANCO, self.rects[self.pontosMouse["posX"]][self.pontosMouse["posY"]], 1) # HIT BOX
        if self.pausado:
            for ponto in self.pontos:
                pg.draw.rect(var.TELA, var.PRETO, self.rects[ponto["posX"]][ponto["posY"]], 3) # HIT BOX
            for ponto in self.pontos:
                pg.draw.rect(var.TELA, var.BRANCO, self.rects[ponto["posX"]][ponto["posY"]], 1) # HIT BOX
        if (self.cursorAparece or self.pausado) and not self.mouseForaTela:
            pg.draw.rect(var.TELA, var.VERMELHO, self.rects[self.pontosMouse["posX"]][self.pontosMouse["posY"]], 1) # H
        pg.draw.rect(var.TELA, var.BRANCO, self.rectGeral, 1)

    def attGrid(self):
        if not self.pausado:
            for x in range(var.quantidadeGridX):
                for y in range(var.quantidadeGridY):
                    # "q" é diminutivo de quadrado
                    numQuadrados = 0
                    q1 = [0, 0, 0]
                    q2 = [0, 0, 0]
                    q3 = [0, 0, 0]
                    q4 = [0, 0, 0]
                    q0 = [0, 0, 0]
                    q0 = self.gridCores[x][y]
                    numQuadrados += 1
                    # Faz a média de cores dos 4 quadrados em volta do quadrado em questão
                    if y != var.quantidadeGridY-1: 
                        q1 = self.gridCores[x][y+1]
                        numQuadrados += 1
                    if x != var.quantidadeGridX-1:
                        q2 = self.gridCores[x+1][y]
                        numQuadrados += 1
                    if y != 0:
                        q3 = self.gridCores[x][y-1]
                        numQuadrados += 1
                    if x != 0:
                        q4 = self.gridCores[x-1][y]
                        numQuadrados += 1
                    qMedia = np.add(np.add(np.add(np.add(q0, q1), q2), q3), q4)/numQuadrados
                    # Substitui a cor do quadrado pela cor média
                    self.gridFuturo[x][y] = qMedia # Armazena a nova cor gerada no gridFuturo

        # Aplica o novo grid formado
        self.gridCores = copy.deepcopy(self.gridFuturo)
        for ponto in self.pontos:
            self.gridCores[ponto["posX"]][ponto["posY"]] = ponto["cor"]

        # Coloca o quadrado que corresponde ao ponteiro do mouse no gridCores
        if (self.cursorAparece or self.pausado) and not self.mouseForaTela:
            self.gridCores[self.pontosMouse["posX"]][self.pontosMouse["posY"]] = self.pontosMouse["cor"]

    # Checa em que indice X do retangulo o mouse colide
    # divisão para conquistar
    def colisaoParticoesX(self, mousePos, x=0, index=0, passo=1):
        # Caso base. Todos os indices X foram checados
        if 2**(passo-1) == var.quantidadeGridX:
            return index
        else:
            tamParticaoX = self.tamanhoRect*var.quantidadeGridX//(2**passo)
            tamParticaoY = self.tamanhoRect*var.quantidadeGridY
            particao = pg.Rect((x + self.gapLados, self.gapCima), (tamParticaoX, tamParticaoY))
            
            if not particao.collidepoint(mousePos):
                index += var.quantidadeGridX//(2**passo)
                
            passo += 1
            x = self.tamanhoRect * index
            return self.colisaoParticoesX(mousePos, x, index, passo)

    # Checa em que indice Y do retangulo o mouse colide
    # divisão para conquistar
    def colisaoParticoesY(self, mousePos, y=0, index=0, passo=1):
        # Caso base. Todos os indices Y foram checados
        if 2**(passo-1) == var.quantidadeGridY:
            return index
        else:
            tamParticaoX = self.tamanhoRect*var.quantidadeGridX
            tamParticaoY = self.tamanhoRect*var.quantidadeGridY//(2**passo)
            particao = pg.Rect((self.gapLados, y + self.gapCima), (tamParticaoX, tamParticaoY))
            
            if not particao.collidepoint(mousePos):
                index += var.quantidadeGridY//(2**passo)
                
            passo += 1
            y = self.tamanhoRect * index
            return self.colisaoParticoesY(mousePos, y, index, passo)

