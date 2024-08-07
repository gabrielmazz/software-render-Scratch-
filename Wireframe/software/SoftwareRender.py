import pygame as pg
import os

import Wireframe.points_object.object as obj
from Rendering.software.colors import *
from Rendering.software.SoftwareRender import *

color = Colors()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear') # Limpa a tela

class SoftwareWireframe():
    
    def __init__(self):
        
        pg.init()                                                           # Inicializa o pygame
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900                      # Resolução da janela (WIDTH, HEIGHT) -> (Largura, Altura)
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2     # Meio da tela, para centralizar os objetos na tela
        self.FPS = 120                                                      # Frames por segundo da janela
        self.screen = pg.display.set_mode(self.RES)                         # Cria a janela com a resolução definida 
        self.clock = pg.time.Clock()                                        # Cria um relogio para controlar o FPS
    
        self.CELL_SIZE = 20                                                 # Tamanho do grid
    
    # Função que exibe o FPS na tela
    def display_fps(self):
        fps_text = str(int(self.clock.get_fps()))
        fps_font = pg.font.Font(None, 24)
        fps_surface = fps_font.render(fps_text, True, color.GREEN)
        
        return fps_surface
    
    # Função que exibe a versão do software na tela, no cantor inferior direito
    # da tela, com uma fonte de tamanho 10 e preto transparente
    def display_version(self):
            
        version = "CG_Software_Rendering v1.05"
        version_font = pg.font.Font(None, 12)
        version_surface = version_font.render(version, True, color.BLACK)
        
        return version_surface
    
    def grid_points(self, x, y, width, height, space):
        
        # Em cima dos pontos do grid, desenha os números correspondentes a 
        # posição x e y
        for i in range(0, width, space):
            pg.draw.line(self.screen, (0, 0, 0), (i, 0), (i, 10))
            text = pg.font.Font(None, 12).render(str(i), True, (0, 0, 0))
            self.screen.blit(text, (i, 0))
        for i in range(0, height, space):
            pg.draw.line(self.screen, (0, 0, 0), (0, i), (10, i))
            text = pg.font.Font(None, 12).render(str(i), True, (0, 0, 0))
            self.screen.blit(text, (0, i))
            
        # Desenha as linhas do grid
        for i in range(0, width, space):
            pg.draw.line(self.screen, (0, 0, 0), (i, 0), (i, height))
        for i in range(0, height, space):
            pg.draw.line(self.screen, (0, 0, 0), (0, i), (width, i))
            
    def click_grid(self, pos):
        
        # Pega a posição do mouse separadamente
        x, y = pos
        
        # Pega a posição do mouse no grid
        snap_x = (x // self.CELL_SIZE) * self.CELL_SIZE + self.CELL_SIZE // 2
        snap_y = (y // self.CELL_SIZE) * self.CELL_SIZE + self.CELL_SIZE // 2
        
        return snap_x, snap_y
        
    def draw_lines(self, points):
        
        # Verifica se tem mais ou igual a dois pontos para fazer a linha
        if len(points) >= 2:
            pg.draw.lines(self.screen, (0, 0, 0), True, points, 3)
            
            # Desenha os pontos fixados no grid
            for point in points:
                pg.draw.circle(self.screen, (0, 0, 0), point, 5)
                
            # Mostra em cima do ponto a posição x e y
            for point in points:
                text = pg.font.Font(None, 12).render(f'{point}', True, (0, 0, 0))
                self.screen.blit(text, point)

    def draw(self, points, screen_color='white'):
        self.screen.fill(screen_color)
        self.grid_points(self.H_WIDTH, self.H_HEIGHT, self.WIDTH, self.HEIGHT, self.CELL_SIZE)
        self.draw_lines(points.points_line)
        
        fps_surface = self.display_fps()
        version_surface = self.display_version()
        
        self.screen.blit(fps_surface, (10, 10))
        self.screen.blit(version_surface, (self.WIDTH - 120, self.HEIGHT - 10))
            
    def run(self):
        
        clear_screen()
        
        # Instancia o pseudo objeto
        points = obj.Points_Object()
        
        while True:
            
            self.draw(points)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                
                elif event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
                    pg.quit()
                
                # Evento para limpar os pontos e o canvas
                elif event.type == pg.KEYDOWN and event.key == pg.K_c:
                    points.clear_points()
                    
                # Evento principal, quando o usuario já tiver os pontos que deseja, clicar
                # o botão 1 do mouse, ira fazer a técnica de revolução, isso ira fechar 
                # a tela do programa, para que a parte do rendering possa ser executada
                # criando uma nova tela do pygame
                elif event.type == pg.KEYDOWN and event.key == pg.K_1:
                    
                    points.revolucion()
                
                    pg.quit()
                    return
                
                # Adiciona os pontos no objeto manualmente, o usuário pode definir
                # manualmente o x e y dos pontos
                elif event.type == pg.KEYDOWN and event.key == pg.K_2:
                    
                    print("Digite o valor de x e y dos pontos, separados por espaço")
                    print("Exemplo: 100 100")
                    print("Digite 'sair' para sair")
                    
                    while True:
                        user_input = input("Digite o valor de x e y: ")
                        
                        if user_input == 'sair':
                            break
                            
                        x, y = user_input.split()
                        points.append_points((int(x), int(y)))
                
                # Evento para pegar o clique do mouse, botao esquerdo
                # determina aonde o usuario clicou na tela e da append nos pontos
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        
                        # Pega a posição do mouse
                        pos = pg.mouse.get_pos()
                        
                        # Pega a posição no grid
                        pos_grid = self.click_grid(pos)
                        
                        # Adiciona os pontos no objeto
                        points.append_points(pos_grid)
                        
            pg.display.set_caption(f'Wireframe')
            pg.display.flip()
            self.clock.tick(self.FPS)
            