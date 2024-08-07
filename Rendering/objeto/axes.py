import numpy as np
import pygame as pg

from Rendering.manipulacoes.matrix_functions import *
from Rendering.software.camera import *
from Rendering.objeto.object_3d import *

class Axes(Object3D):
    
    def __init__(self, render):
        super().__init__(render)
        self.vertexes = np.array([(0, 0, 0, 1), (1, 0, 0, 1), (0, 1, 0, 1), (0, 0, 1, 1)])
        self.faces = np.array([(0, 1), (0, 2), (0, 3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]
        self.draw_vertexes = False
        self.label = 'XYZ'
        
    def screen_projection_axes(self):
        
        vertexes = self.vertexes @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]
        
        for index, color_face in enumerate(self.color_faces):
            
            color, face = color_face
            
            polygon = vertexes[face]
            
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.line(self.render.screen, color, polygon[0], polygon[1], 2)
                
                if self.label:
                    text = self.font.render(self.label[index], True, color)
                    self.render.screen.blit(text, polygon[-1])