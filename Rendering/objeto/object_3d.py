import pygame as pg
import numpy as np
import numba as nb
import time
from Rendering.manipulacoes.matrix_functions import *
from Rendering.software.camera import *

@nb.njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))

class Object3D:
    
    def __init__(self, render, vertexes='', faces='', x='', y='', xn='', yn='', zn=''):
        
        self.render = render

        self.vertexes = np.array(vertexes)
        self.faces = faces
        
        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, False
        self.label = ''
        
        self.drawing_method = 0
        
        self.x = x
        self.y = y
        
        self.xn = xn
        self.yn = yn
        self.zn = zn
            
    def draw(self):
        self.screen_projection()
     
    def define_color(self, color):
        self.color_faces = [(color, face) for face in self.faces]
     
    def show_vertexes(self, bool):
        self.draw_vertexes = bool 
    
    def just_edges_faces(self, bool):
        self.drawing_method = 1 if bool else 0
    
    def movement(self):
        if self.movement_flag:
            self.rotate_x(pg.time.get_ticks() % 0.005)
        
    def screen_projection(self):
        
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for index, color_face in enumerate(self.color_faces):
            
            color, face = color_face
            
            polygon = vertexes[face]
            
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pg.draw.polygon(self.render.screen, color, polygon, self.drawing_method)              # Desenha o poligono na tela           
                
                if self.label:
                    text = self.font.render(self.label[index], True, pg.Color('white'))
                    self.render.screen.blit(text, polygon[-1])

        if self.draw_vertexes:
            for vertex in vertexes:
                if not any_func(vertex, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 2)         
          
    # Transladar, no contexto de gráficos de computador e modelagem 3D, 
    # refere-se ao processo de mover um objeto de um lugar para outro sem 
    # alterar sua orientação ou tamanho. 
    def translate(self, pos):
        self.vertexes = self.vertexes @ translate(pos)
        
    def scale(self, scale_to):
        self.vertexes = self.vertexes @ scale(scale_to)
        
    def rotate_x(self, angle):
        self.vertexes = self.vertexes @ rotate_x(angle)
        
    def rotate_y(self, angle):
        self.vertexes = self.vertexes @ rotate_y(angle)
        
    def rotate_z(self, angle):
        self.vertexes = self.vertexes @ rotate_z(angle)

    def control_object(self):
        
        # Pega as teclas pressionadas
        key = pg.key.get_pressed()
        
        # Movimentação do objeto
        # I - Translação para cima
        # K - Translação para baixo
        # J - Translação para esquer
        # L - Translação para direita
        
        if key[pg.K_i]:
            self.translate((0, -1, 0))
        if key[pg.K_k]:
            self.translate((0, 1, 0))
        if key[pg.K_j]:
            self.translate((-1, 0, 0))
        if key[pg.K_l]:
            self.translate((1, 0, 0))
            
