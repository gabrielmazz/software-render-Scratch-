import pygame as pg
import numpy as np
import numba as nb

from Rendering.manipulacoes.matrix_functions import *
from Rendering.software.camera import *

# Herda as funções para nao repetir tudo novamente
from Rendering.objeto.object_3d import *

class Object_Cubo(Object3D):
    def __init__(self, render):
        
        self.render = render
        
        self.vertexes = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                                  (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)])
        
        self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), 
                               (1, 2, 6, 5), (0, 3, 7, 4)])
        
        self.font = pg.font.SysFont('Arial', 30, bold=True)
        self.color_faces = [(pg.Color('orange'), face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, False
        self.label = ''
        
        self.drawing_method = 0
        
        # Apenas por conveniência e nao dar problemas na aplicação quando
        # é escolhido a opção 2
        self.x = 0
        self.y = 0
        self.xn = 0
        self.yn = 0
        self.zn = 0
       
     
    def draw(self):
        Object3D.draw(self)
     
    def define_color(self, color):
        Object3D.define_color(self, color)
    
    def show_vertexes(self, bool):
        Object3D.show_vertexes(self, bool) 
        
    def just_edges_faces(self, bool):
        Object3D.just_edges_faces(self, bool)
    
    def movement(self):
        Object3D.movement(self)
        
    def screen_projection(self):
        Object3D.screen_projection(self)
             
    def translate(self, pos):
        Object3D.translate(self, pos)
        
    def scale(self, scale_to):
        Object3D.scale(self, scale_to)
        
    def rotate_x(self, angle):  
        Object3D.rotate_x(self, angle)
        
    def rotate_y(self, angle):
        Object3D.rotate_y(self, angle)
        
    def rotate_z(self, angle):
        Object3D.rotate_z(self, angle)
        
    def control_object(self):
        Object3D.control_object(self)
        