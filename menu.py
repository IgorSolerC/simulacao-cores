import pygame as pg
import variaveis as var

# Slider de cor. Usado para selecionar cores
class Slider():
    def __init__(self, x, y, indexCor):
        self.indexCor = indexCor # RGB. 0 = R, 1 = G e 2 = B
        
        self.x = x # Posição X da base slider
        self.y = y # Posição Y da base  slider
        
        self.larg = 256 # Largura da base do slider
        self.alt = 10#  Altura da base do slider

        self.rectBase = pg.Rect((self.x, self.y), (self.larg, self.alt)) # Hitbox da base do slider
        
        self.sliderX = self.x + 255 # Posição X da parte móvel do slider
        self.sliderY = self.y - 1 # Posição Y da parte móvel do slider

        self.sliderLarg = 5 # Largura da parte móvel do slider
        self.sliderAlt = self.alt + 2 # Altura da parte móvel do slider

        self.corSelecionada = self.sliderX - self.x # Cor atualmente selecionada no slider
        
        self.sliderRect = pg.Rect((self.sliderX, self.sliderY), (self.sliderLarg, self.sliderAlt)) # Hitbox da parte móvel do slider
        self.sliderRect.centerx = self.sliderX # Centro da parte móvel do slider

        self.particoesRect = self.definirParticoesRect()

    # Atualiza o posicionamento e cor da parte movel do slider
    def atualizarSlider(self, valor):
        self.sliderX = self.x + valor
        self.sliderRect = pg.Rect((self.sliderX, self.sliderY), (self.sliderLarg, self.sliderAlt))
        self.sliderRect.centerx = self.sliderX
        self.corSelecionada = self.sliderX - self.x

    # Define as hitboxes da base do slider
    # As multiplas hitboxes servem para que o slider possa ter uma cor gradiente
    def definirParticoesRect(self):
        rects = []
        self.sliderRect = pg.Rect((self.sliderX, self.sliderY), (self.sliderLarg, self.sliderAlt))
        for i in range(256):
            novoRect = pg.Rect((i + self.x, self.y), (1, self.alt))
            rects.append(novoRect)
        return rects

    # Desenha na tela o slider
    def draw(self):
        corRect = [0, 0, 0]
        for rect in self.particoesRect:
            pg.draw.rect(var.TELA, corRect, rect, 0)
            corRect[self.indexCor] += 1
        pg.draw.rect(var.TELA, var.PRETO, self.rectBase, 3)
        pg.draw.rect(var.TELA, var.BRANCO, self.rectBase, 1)

        corSlider = [0, 0, 0]
        corSlider[self.indexCor] = self.corSelecionada
        pg.draw.rect(var.TELA, corSlider, self.sliderRect, 0)
        pg.draw.rect(var.TELA, var.PRETO, self.sliderRect, 3)
        pg.draw.rect(var.TELA, var.BRANCO, self.sliderRect, 1)
        
        
class Menu():
    def __init__(self, gapLados):
        self.sliders = []
        for i in range(3):
            self.sliders.append(Slider(0, 10 + (15*i), i))
        self.atualizaPosSlider(gapLados)

        self.corSelecionada = self.lerCorSelecionada()
        
        self.defineRectGeral()
        
    def lerCorSelecionada(self):
        corSelecionada = []
        for i in range(3):
            corSelecionada.append(self.sliders[i].corSelecionada)
            self.corSelecionada = corSelecionada
        return corSelecionada
        
    def defineRectGeral(self):
        self.rectGeral = pg.Rect((0, 0), (var.TAMANHO_TELA[0], var.TAMANHO_Y_MENU))

    def atualizaPosSlider(self, gapLados):
        for i in range(3):
            self.sliders[i].x = gapLados
            self.sliders[i].sliderX = self.sliders[i].x + self.sliders[i].corSelecionada - 2
            self.sliders[i].particoesRect = self.sliders[i].definirParticoesRect()
            self.sliders[i].rectBase = pg.Rect((self.sliders[i].x, self.sliders[i].y), (self.sliders[i].larg, self.sliders[i].alt))
        self.rectCorSelecionada = pg.Rect((5 + 256 + self.sliders[0].x, 10), (15*3 - 5, 15*3 - 5))

    def draw(self):
        for slider in self.sliders:
            slider.draw()
        #pg.draw.rect(var.TELA, var.VERMELHO, self.rectGeral, 1)
        pg.draw.rect(var.TELA, self.corSelecionada, self.rectCorSelecionada, 0)
        pg.draw.rect(var.TELA, var.PRETO, self.rectCorSelecionada, 3)
        pg.draw.rect(var.TELA, var.BRANCO, self.rectCorSelecionada, 1)
            
