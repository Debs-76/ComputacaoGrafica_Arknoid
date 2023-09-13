from tkinter import *
from constantes import *
import random

from retangulo import Retangulo
from bola import Bola

class Jogo(object):
    def __init__(self):

        #Criar área principal do Jogo
        self.root = Tk()
        self.root.geometry('%ix%i' %(LARGURA, ALTURA))
        self.root.resizable(False, False)
        self.root.title('ARKNOID')

        #frame para conter o canvas
        self.frame = Frame(bg="blue")
        self.frame.pack()

        #codigo de criação do canvas
        self.canvas = Canvas(self.frame, bg="black", width=CANVAS_L, height=CANVAS_A, cursor = 'target')
        foto = PhotoImage(file = "fundo/fundo.gif")
        self.canvas.create_image(CANVAS_L/2, CANVAS_A/2, image=foto)
        self.canvas.pack()

        #criando objetos dentro do canvas
        #self.canvas.create_line(10,10,350,350, fill='white')
        #self.canvas.create_polygon((100, 200), (150, 250), (250, 250), (300, 200), (300, 100), (250, 50), (150, 50), (100, 100), fill = 'white')
       
        self.comecar = Button(self.root, text='INCIAR', command=self.começa)
        self.comecar.focus_force()
        self.comecar.pack()

        self.comecar.bind('<Return>', self.começa)
        self.carregaImagens()
        self.novoJogo()
          
        self.root.mainloop()


    def carregaImagens(self):
        
        self.spritesheet = []
        for i in range(1,9):
            
            self.spritesheet.append(PhotoImage(file = "fundo/%.2i.gif"%i))
 
        self.number_of_sprite = 0
        self.limite = len(self.spritesheet) - 1

          


    def novoJogo(self):
        
        #Criação dos elementos do jogo - PLAYER
        self.player = Retangulo(largura = 100, altura = 20, cor = 'white', pos = (LARGURA//2 + 360, 380), vel = (15, 15), tag = 'player')
        self.player.desenhar(self.canvas)
        self.canvas.bind('<Motion>', self.move_player)
        
        #criar a bolinha do jogo
        self.bola = Bola(raio = 30, cor = 'red', pos = (100, 200), vel = (3, 3))
        
        
        
        #lista dos retangulos
        self.r = []
        l, c, e = 5, 8, 2   #linhas, colunas e espaçamentos
        b, h, y0 = 48, 20, 50   #base, altura e posicao inicial

        for i in range(l):
            cor = random.choice(['black', 'orange', 'white', 'lightgray', 'yellow', 'green', 'purple'])
            for j in range(c):
                r = Retangulo(b, h, cor, (b*j+(j+1)*e, i*h+(i+1)*e + y0), (0, 0), 'rect')
                self.r.append(r)
        self.canvas.create_text(CANVAS_L/2, CANVAS_A/2, text = 'Bem Vindos!!', fill='white', font='Verdana, 12')

        #mudar o estado para jogando
        self.jogando = True

    def começa(self):
        #iniciar o jogo
        self.jogar()

    def jogar(self):
        #Vai ser executando enquanto o jogador estiver jogando
        if self.jogando:
            self.update()
            self.desenhar()
            
            if len(self.r) == 0:
                self.jogando = False
                self.msg = "VOCÊ GANHOU!!"
            if self.bola.y > CANVAS_A:
                self.jogando = False
                self.msg = "VOCÊ PERDEU!!"
                
            self.root.after(10, self.jogar)
        else:
            self.acabou(self.msg)


    def move_player(self, event):
        #Movimentação do meu player - rebatedor
        if event.x > 0 and event.x < CANVAS_L - self.player.b:
            self.player.x = event.x

    def update(self):
        #movimento da bola
        self.bola.update(self)
        
        self.number_of_sprite += 1
        if self.number_of_sprite > self.limite:
            self.number_of_sprite = 0
        
    def recomeça(self):
        self.novoJogo()
        self.comecar['text'] = 'INICIAR'
        self.jogar()


    def acabou(self, msg):
        self.canvas.delete(ALL)
        self.canvas.create_text(CANVAS_L/2, CANVAS_A/2, text= msg, fill='white')
        self.comecar['text'] = 'Reiniciar'
        self.comecar['command'] = self.recomeça


    def desenhar(self):
        """
        Método para redesenhar a tela do jogo
        """
        #primeiro apagamos tudo que há no canvas
        self.canvas.delete(ALL)

        #inserir imagens no canvas
        self.canvas.create_image((CANVAS_L/2,CANVAS_A/2), image = self.spritesheet[self.number_of_sprite])
 
        #e o player
        self.player.desenhar(self.canvas)
 
        #E por fim todos os retângulos
        for r in self.r:
            r.desenhar(self.canvas)
 
        #depois desenhamos a bola
        self.bola.desenhar(self.canvas)
         
        
 


    def verificaColisao(self):
        #Criar uma bouding box para a bola
        coord = self.canvas.bbox('bola')
        #x1, y1, x2, y2

        #Pegar informações os objetos que colidem com a bola
        colisoes = self.canvas.find_overlapping(*coord)

        #se o numero de colisões é diferente de 0
        if len(colisoes) != 0:
            #verificar se o id do objeto colidido é diferente do id do objeto player
            if colisoes[0] != self.player:
                #Vamos colocar para que a colisao ocorra com o objeto mais proximo do topo esquerdo
                m_p = self.canvas.find_closest(coord[0], coord[1])
                #identificar com qual retangulo ocorreu a colisao
                for r in self.r:
                    #tendo encontrado um retangulo
                    if r == m_p[0]:
                        self.r.remove(r)   #removendo o retangulo do jogo
                        self.canvas.delete(r)
                        #inverter o sentido da velocidade da bola
                        self.b_vy *= -1
                        return

                        

if __name__ == '__main__':
    Jogo()       



        
