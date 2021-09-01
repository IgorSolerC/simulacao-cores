import pygame as pg
import variaveis as var
import menu as mn
import grid
import numpy as np
import copy

# Inicia a engine
pg.init()

# Variaveis
tabuleiro = grid.Tabuleiro()
mouseOverRect = 0
tabuleiro.cursorAparece = True
mouseForaTela = True

# Um slider de seleção de cor foi clicado?
sliderSelecionado = -1 # Nenhum selecionado

menu = mn.Menu(tabuleiro.gapLados)

mousePos = pg.mouse.get_pos()

# Abre uma nova janela
pg.display.set_caption("Inuminação") # Titulo da janela

# Deixa o cursor visível
pg.mouse.set_visible(True)

# ---------- MAIN LOOP ---------- 
jogoRodando = True
clock = pg.time.Clock() # Framerate (Velocidade que a tela da update)

while jogoRodando:
    # --------- MAIN EVENT (O usuario entrou algum input?)
    for evento in pg.event.get(): # User entrou um input
        if evento.type == pg.QUIT: # Se o jogador fechou o jogo
            jogoRodando = False

        # Mouse se moveu
        if evento.type == pg.MOUSEMOTION:
            mousePos = pg.mouse.get_pos()
            # Ve se o mouse está em cima de algum grid
            mouseOverRect = 0
            mouseForaTela = True
            tabuleiro.mouseForaTela = True
            if tabuleiro.rectGeral.collidepoint(mousePos):
                tabuleiro.mouseForaTela = False
                mouseOverRect = grid
                mouseRectLinha = tabuleiro.colisaoParticoesX(mousePos)
                mouseRectColuna = tabuleiro.colisaoParticoesY(mousePos)
                        
                tabuleiro.pontosMouse["posX"] = mouseRectLinha
                tabuleiro.pontosMouse["posY"] = mouseRectColuna
            else:
                tabuleiro.mouseForaTela = True

        # Mouse foi apertado
        if evento.type == pg.MOUSEBUTTONDOWN: # Jogador apertou botão do mouse
            mouseBotEsquerdo = pg.mouse.get_pressed()[0] # Update estado BEM
            mouseBotDireito = pg.mouse.get_pressed()[2] # Update estado BDM
            
            if mouseBotEsquerdo: # Botão esquerdo foi pressionado
                if mouseOverRect != 0 and (tabuleiro.cursorAparece or tabuleiro.pausado):
                    for ponto in tabuleiro.pontos:
                        if ponto["posX"] == mouseRectLinha and ponto["posY"] == mouseRectColuna:
                            tabuleiro.pontos.remove(ponto)
                    tabuleiro.pontos.append({"posX": mouseRectLinha, "posY": mouseRectColuna, "cor": copy.deepcopy(tabuleiro.corSelecionada)})

                if menu.rectGeral.collidepoint(mousePos): # Se o cursor foi clicado no menu 
                    for i in range(len(menu.sliders)): # Varre pelos 3 sliders
                        rect = menu.sliders[i].rectBase # hit box do slider
                        if rect.collidepoint(mousePos): # Checa se o click foi neste slider
                            sliderSelecionado = i # Atualiza posição do slider
                            
            if mouseBotDireito: # Botão direito foi pressionado
                if mouseOverRect != 0 and (tabuleiro.cursorAparece or tabuleiro.pausado): # Se o mouse está em cima de um quadrado, e o cursor habilitado
                    for ponto in tabuleiro.pontos:
                        if ponto["posX"] == mouseRectLinha and ponto["posY"] == mouseRectColuna:
                            tabuleiro.pontos.remove(ponto) # Remove o ponto que foi clicado

        if evento.type == pg.MOUSEBUTTONUP: # Jogador apertou botão do mouse
            mouseBotEsquerdo = pg.mouse.get_pressed()[0] # Update estado BEM
            if not mouseBotEsquerdo:
                sliderSelecionado = -1

        # Tecla foi apertada
        if evento.type == pg.KEYDOWN:
            if pg.key.get_pressed()[pg.K_RETURN]: # Escolhe entre mostrar ou não o cursor
                if tabuleiro.cursorAparece:
                    tabuleiro.cursorAparece = False
                else:
                    tabuleiro.cursorAparece = True
            if pg.key.get_pressed()[pg.K_SPACE]: # Pausa e despausa a simulação
                if tabuleiro.pausado:
                    tabuleiro.pausado = False
                else:
                    tabuleiro.pausado = True

        # Tamanho da tela foi mudado
        if evento.type == pg.VIDEORESIZE:
            var.TAMANHO_TELA = var.TELA.get_size()
            tabuleiro.defineTamanhoTela()
            menu.defineRectGeral()
            menu.atualizaPosSlider(tabuleiro.gapLados)
            
    # --------- GAME LOGIC (O que ocorre entre frames)

    # Atualiza sliders de cor
    if sliderSelecionado > -1:
        slider = menu.sliders[sliderSelecionado] # hit box do slider
        corSelecionada = mousePos[0] - slider.x # Atualiza cor selecionada do slider

        # Limita valor da cor:
        if corSelecionada < 0:
            corSelecionada = 0
        elif corSelecionada > 255:
            corSelecionada = 255
        
        slider.atualizarSlider(corSelecionada)
        tabuleiro.corSelecionada = menu.lerCorSelecionada()
        tabuleiro.pontosMouse["cor"] = tabuleiro.corSelecionada

    # Atualiza a cor de cada retangulo do Grid. 
    tabuleiro.attGrid()
    
    # --------- DRAWING CODE (Update da tela)
    var.TELA.fill(var.CINZA)
    
    tabuleiro.draw() # Desenha o tabuleiro

    menu.draw() # Desenha o menu de seleção de cor
    
    # --------- UPDATE SCREEN
    pg.display.flip()
    
    # --------- FRAME RATE
    clock.tick(var.FRAMES_POR_SEGUNDO)

# Para a engine quando o jogo para
pg.quit()
