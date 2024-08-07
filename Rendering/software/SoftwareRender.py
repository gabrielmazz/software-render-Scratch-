import pygame as pg
import os
import numpy as np
import time 

import Rendering.manipulacoes.selections as sl
from Rendering.objeto.object_3d import *
from Rendering.software.camera import *
from Rendering.software.projection import *
from Rendering.software.colors import *
from Rendering.objeto.axes import *
from Rendering.objeto.graph import *

# Determina objetos já modelados, mas não sendo .obj
from Rendering.objeto.objetos_prontos.modelos import *

# Importa a classe de cores
from Rendering.software.colors import *

# Variável global para a cor do fundo da tela
global screen_color

# Variáveis globais para flags
global button_state_edges
global button_state_vertices
global button_state_axes

# Importa a classe de cores
color = Colors()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela

# A classe SoftwareRender é responsável por criar a janela e chamar os objetos, nele é criado os parametros da janela
# e os objetos que serão renderizados
class SoftwareRender():
    
    def __init__(self, opcao):
        
        pg.init()                                                           # Inicializa o pygame
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900                      # Resolução da janela (WIDTH, HEIGHT) -> (Largura, Altura)
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2     # Meio da tela, para centralizar os objetos na tela
        self.FPS = 120                                                      # Frames por segundo da janela
        self.screen = pg.display.set_mode(self.RES)                         # Cria a janela com a resolução definida 
        self.clock = pg.time.Clock()                                        # Cria um relogio para controlar o FPS
        
        # Cria os objetos que serão renderizados, de acordo com a opção escolhida
        # caso seja 1, será renderizado um objeto .obj, caso seja 2, será renderizado um objeto
        # definido pelo usuario
        self.create_objects(opcao)
    
    # Função que exibe o FPS na tela
    def display_fps(self):
        fps_text = str(int(self.clock.get_fps()))
        fps_font = pg.font.Font(None, 24)
        fps_surface = fps_font.render(fps_text, True, color.GREEN)
        
        return fps_surface
     
    # Função que exibe o ponto de mira na tela
    def display_aim(self):
        aim_font = pg.font.Font(None, 24)
        aim_surface = aim_font.render('+', True, color.PURPLE)
        
        return aim_surface
    
    # Função que exibe os atalhos do programa em baixo do FPS mostrado na tela
    # no caso, será exibido no canto superior esquerdo da tela
    def display_shortcuts(self):
        
        shortcut1 = "(WASD) - Movimentar a câmera"
        shortcut2 = "(QE) - Subir e descer a câmera"
        shortcut3 = "(Setas) - Rotacionar a câmera"
        shortcut4 = "(DEL) - Sair do programa"
        shortcut5 = "(M) - Menu de opções"
        shortcut6 = "(R) - Reseta a posição da câmera"
        shortcut7 = "(P|I) - Plotar e Fechar gráfico"
        
        # Lista de atalhos
        shortcuts = [shortcut1, shortcut2, shortcut3, shortcut4, shortcut5, shortcut6, shortcut7]

        return shortcuts
    
    def display_menu(self):
        
        shortcut1 = "(1) - Mostrar | Esconder arestas"
        shortcut2 = "(2) - Mostrar | Esconder vértices"
        shortcut3 = "(3) - Mostrar | Esconder eixos"
        shortcut4 = "(4) - Randomizar cor do objeto"

        shortcuts = [shortcut1, shortcut2, shortcut3, shortcut4]
        
        return shortcuts
        
    # Função que exibe a versão do software na tela, no cantor inferior direito
    # da tela, com uma fonte de tamanho 10 e preto transparente
    def display_version(self):
            
        version = "CG_Software_Rendering v1.05"
        version_font = pg.font.Font(None, 12)
        version_surface = version_font.render(version, True, color.BLACK)
        
        return version_surface
    
    # Função que exibe o gráfico do objeto na tela
    def display_graph(self):
        
        # Pega o path aonde esta o arquivo object.obj por meio do os
        current_directory = os.getcwd()
        
        # Mostra a imagem "Plot.png" no meio da tela
        plot = pg.image.load(current_directory + '/Rendering/software/img/Plot.png')
        self.screen.blit(plot, (self.H_WIDTH - 600, self.H_HEIGHT - 300))
    
    # Menu de teclas de atalho para simplificar o uso do menu geral
    def menu_buttons(self):
        
        # Obtém o estado atual do teclado
        key = pg.key.get_pressed()
        
        # Botão 1 - Modifica as arestas do objeto, mostrando ou não. Com o mesmo botão, é possível mostrar ou não os vertices
        if key[pg.K_1]:
            
            global button_state_edges
            
            time.sleep(0.2)
            
            if not button_state_edges:
                self.object.just_edges_faces(True)
                button_state_edges = True
            else:
                self.object.just_edges_faces(False)
                button_state_edges = False
                
        if key[pg.K_2]:
            
            global button_state_vertices
            
            time.sleep(0.2)
            
            if not button_state_vertices:
                self.object.show_vertexes(True)
                button_state_vertices = True
            else:
                self.object.show_vertexes(False)
                button_state_vertices = False
                
        # Botão 3 - Mostra ou não os eixos do mundo
        if key[pg.K_3]:
            
            global button_state_axes
            
            time.sleep(0.2)
            
            if not button_state_axes:
                self.world_axes.draw_vertexes = True
                button_state_axes = True
            else:
                self.world_axes.draw_vertexes = False
                button_state_axes = False
                
        # Botão 4 - Randomiza a cor do objeto
        if key[pg.K_4]:
            
            time.sleep(0.2)
            
            random_color = color.random_color()
            self.object.define_color(random_color)
              
    # Função que cria os objetos que serão renderizados, ele chama as classes indicadas para o objeto dependendo do arquivo
    def create_objects(self, opcao):
        
        # Na primeira opção, o usuário pode escolher entre um wireframe, que será 
        # possivel desenhar um objeto em 2D e será feito uma renderização (revolução)
        # para 3D, ou um objeto que será rasterizado, como um cubo, piramide, etc.
        if opcao == 1:
            self.camera = Camera(self, [-5, 5, -50])
            self.projection = Projection(self)
            
            # Pega o path aonde esta o arquivo object.obj por meio do os
            current_directory = os.getcwd()
            
            self.object = self.get_object_from_file(current_directory + '/Rendering/resources/object.obj')
            
            # Diminui o objeto para caber na tela
            #self.object.scale(0.9)
            
            # Translada o objeto para o 0, 0, 0
            self.object.translate([0.0001, 0.0001, 0.0001])
            
            # Cria os eixos do mundo
            self.world_axes = Axes(self)
            
            # Aumenta o tamanho dos eixos para que fique parelho com o objeto
            self.world_axes.scale(3000)
            
            # Cria o gráfico
            self.graph = Graph(self.object.x, self.object.y, self.object.zn, self.object.xn, self.object.yn)
            
 
        # Nesta opção, objetos que que são especificados pelo usuário, seram 
        # rasterizados, como um cubo, piramide, etc. A classe tem uma leve diferença
        # pois nela mesma, temos coordenadas dos vertices e faces
        elif opcao == 2:
            self.camera = Camera(self, (0.5, 0.5, -5))
            self.projection = Projection(self)
            
            # Criando um objeto cubo
            self.object = Object_Cubo(self)
            
            self.world_axes = Axes(self)
            self.world_axes.translate([0.0001, 0.0001, 0.0001])
            self.world_axes.scale(2.5)
            
            # Diminui a velocidade de movimento da camera porque os
            # objetos são menores quando criados manualmente
            self.camera.moving_speed = 0.08
            
            self.graph = Graph(self.object.x, self.object.y, self.object.zn, self.object.xn, self.object.yn)

        elif opcao == 3:
            
            self.camera = Camera(self, (0.5, 0.5, -5))
            self.projection = Projection(self)
            
            # Gera uma lista com os objetos que podem ser renderizados, mas eles devem estar na pasta 'resources'
            # para que possam ser renderizados. A lista é exibida para o usuário escolher qual objeto ele deseja
        
            # Pega o path aonde esta o arquivo object.obj por meio do os
            current_directory = os.getcwd()
        
            arquivos = os.listdir(current_directory + '/Rendering/resources')
            
            # Apaga da lista os arquivos que não são .obj
            arquivos = [arquivo for arquivo in arquivos if arquivo.endswith('.obj')]
            
            # Retira o arquivo 'object.obj' da lista
            arquivos = [arquivo for arquivo in arquivos if arquivo != 'object.obj']
            
            print("Escolha um dos objetos abaixo para renderizar: ")
            
            for i, arquivo in enumerate(arquivos):
                print(f"{i + 1} - {arquivo}")
                
            opcao = int(input())
            
            clear_screen()
            
            self.object = self.get_object_from_file(current_directory + '/Rendering/resources/' + arquivos[opcao - 1])
            
            # Cria os eixos do mundo
            self.world_axes = Axes(self)
            
            # Aumenta o tamanho dos eixos para que fique parelho com o objeto
            self.world_axes.scale(10)
            
            # Diminui a velocidade de movimento da camera porque os
            # objetos são menores quando criados manualmente
            self.camera.moving_speed = 1
            
            # Cria o gráfico
            self.graph = Graph(self.object.x, self.object.y, self.object.zn, self.object.xn, self.object.yn)
            
    # Função que pega os objetos de um arquivo .obj, e retorna um objeto 3D com as coordenadas dos vertices e faces,
    # ele passara por todo o arquivo .obj que tem uma indexação unica para indicar as posições indicadas
    def get_object_from_file(self, filename):
        
        vertex, faces = [], []
        
        x, y = [], []
        
        xn, yn, zn = [], [], []
        
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):   # Vertices
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):  # Faces
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])
        
        # Pega o path aonde esta o arquivo object.obj por meio do os
        current_directory = os.getcwd()
        
        xn = np.loadtxt(current_directory + '/Rendering/resources/coord_wireframe/xn.txt', delimiter=',') 
        yn = np.loadtxt(current_directory + '/Rendering/resources/coord_wireframe/yn.txt', delimiter=',')
        zn = np.loadtxt(current_directory + '/Rendering/resources/coord_wireframe/zn.txt', delimiter=',')
        
        x = np.loadtxt(current_directory + '/Rendering/resources/coord_wireframe/x.txt', delimiter=',')
        y = np.loadtxt(current_directory + '/Rendering/resources/coord_wireframe/y.txt', delimiter=',')
        
        return Object3D(self, vertex, faces, x, y, xn, yn, zn)

    # Função que desenha os objetos na tela, sendo a função de certa forma primordial para a renderização já que sem ela,
    # não é possivel motrar os objetos na tela
    def draw(self, screen_color):
        self.screen.fill(screen_color)              # Preenche a tela com a cor indicada
        self.object.draw()                          # Desenha o objeto na tela, esta função está na propria classe do objeto

        # Exibe o FPS na tela
        fps_surface = self.display_fps()
        self.screen.blit(fps_surface, (10, 10))
            
        # Exibe o ponto de mira
        aim_surface = self.display_aim()
        self.screen.blit(aim_surface, (self.H_WIDTH - 10, self.H_HEIGHT - 10))    
        
        # Exibe os atalhos do programa
        shortcuts = self.display_shortcuts()
        for i, shortcut in enumerate(reversed(shortcuts)):
            shortcut_surface = pg.font.Font(None, 24).render(shortcut, True, color.BLACK)
            self.screen.blit(shortcut_surface, (10, self.HEIGHT - 10 - 24 * (i + 1)))
        
        # Exibe o menu de atalhos
        menu = self.display_menu()
        for i, shortcut in enumerate(reversed(menu)):
            shortcut_surface = pg.font.Font(None, 24).render(shortcut, True, color.BLACK)
            self.screen.blit(shortcut_surface, (self.WIDTH - 300, self.HEIGHT - 10 - 24 * (i + 1)))
            
        # Exibe a versão do software na tela
        version_surface = self.display_version()
        self.screen.blit(version_surface, (self.WIDTH - 120, self.HEIGHT - 10))

        # Plota o gráfico na tela
        if self.graph.flag_graph:
            self.display_graph()
        
        # Desenha os eixos do mundo
        if self.world_axes.draw_vertexes:
            self.world_axes.screen_projection_axes()
        
    # Função que roda o programa, ele chama a função draw, controla a camera e atualiza a tela
    # aqui é o bloco básico para o funcionamento do pygame
    def run(self):
        
        clear_screen()
        
        # Cor do fundo da tela (Padrao)
        screen_color = 'darkgray'
            
        # Flags
        global button_state_edges
        global button_state_vertices
        global button_state_axes
        
        button_state_edges = False
        button_state_vertices = False
        button_state_axes = False
            
        while True:
            
            self.draw(screen_color)                                         # Chama a função draw, que desenha o objeto na tela
            self.camera.control()                                           # Controla a camera, movendo ela para os lados, cima, baixo, etc
            self.object.control_object()                                    # Movimenta o objeto, rotacionando ele
            self.graph.control_graph()                                      # Controla o gráfico
            self.menu_buttons()                                             # Menu de botões
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                
                elif event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
                    pg.quit()
                
                # Evento para abrir um menu de opções para manipular o objeto
                # Botao 1
                elif event.type == pg.KEYDOWN and event.key == pg.K_m:
                    
                    print("1 - Modificação nas cores")
                    print("2 - Modificação na composição do objeto")
                    print("3 - Mostrar e esconder eixos")

                    print("Digite a opção desejada: ")
                    opcao = int(input())

                    clear_screen()

                    match opcao:
                        case 1:

                            print("1 - Mudar a cor do fundo")
                            print("2 - Mudar a cor do objeto")

                            print("Digite a opção desejada: ")

                            opcao_1 = int(input())

                            match opcao_1:

                                case 1: # Mudar a cor do fundo
                                    screen_color = sl.options_menu()

                                case 2: # Mudar a cor do objeto
                                    self.object.define_color(sl.options_menu())

                        case 2:

                                print("1 - Vertices")
                                print("2 - Arestas")

                                print("Digite a opção desejada: ")

                                opcao_2 = int(input())

                                clear_screen()

                                match opcao_2:

                                    case 1:

                                        print ("1 - Mostrar vertices")
                                        print ("2 - Não mostrar vertices")

                                        print("Digite a opção desejada: ")

                                        opcao_2_1 = int(input())

                                        match opcao_2_1:

                                            case 1:
                                                self.object.show_vertexes(True)

                                            case 2:
                                                self.object.show_vertexes(False)

                                    case 2:

                                        print ("1 - Apenas arestas")
                                        print ("2 - Apenas faces")

                                        print("Digite a opção desejada: ")

                                        opcao_2_2 = int(input())

                                        match opcao_2_2:

                                            case 1:
                                                self.object.just_edges_faces(True)

                                            case 2:
                                                self.object.just_edges_faces(False)

                        case 3:

                            print("1 - Mostrar eixos")
                            print("2 - Não mostrar eixos")

                            print("Digite a opção desejada: ")

                            opcao_3 = int(input())

                            match opcao_3:

                                case 1:
                                    #self.axes.movement_flag = True
                                    self.world_axes.draw_vertexes = True

                                case 2:
                                    #self.axes.movement_flag = False
                                    self.world_axes.draw_vertexes = False     


                    
            #clear_screen()
                
            pg.display.set_caption('Software Rendering')                    # Titulo da janela
            pg.display.flip()                                               # Atualiza a tela
            self.clock.tick(self.FPS)                                       # Controla o FPS do programa
            
