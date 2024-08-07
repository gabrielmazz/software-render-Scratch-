import math
import numpy as np

# Class que realiza a projeção de um objeto 3D para a tela, utilizando a matriz de projeção, método que é utilizado
# para a renderização de objetos 3D em uma tela 2D.

# A matriz de projeção em computação gráfica é uma matriz utilizada para transformar pontos tridimensionais em um espaço 3D 
# para um espaço 2D, como a tela do computador. Essa transformação é necessária para simular a perspectiva e a profundidade 
# em uma cena tridimensional quando renderizada em uma tela plana.

class Projection:
    
    def __init__(self, render):
        
        # Exemplo de como é feito e os parametros para o plano de projeção
        #   - software/img/projeção no plano.png
        NEAR = render.camera.near_plane             # Plano de projeção mais próximo
        FAR = render.camera.far_plane               # Plano de projeção mais distante
        RIGHT = math.tan(render.camera.h_fov / 2)   # Plano de projeção mais a direita
        LEFT = -RIGHT                               # Plano de projeção mais a esquerda
        TOP = math.tan(render.camera.v_fov / 2)     # Plano de projeção mais a cima
        BOTTOM = -TOP                               # Plano de projeção mais a baixo
        
        # Matriz de projeção, composição da mesma
        m00 = 2 / (RIGHT - LEFT)    
        m11 = 2 / (TOP - BOTTOM)
        m22 = (FAR + NEAR) / (FAR - NEAR)
        m32 = -2 * NEAR * FAR / (FAR - NEAR)
        self.projection_matrix = np.array([
            [m00, 0, 0, 0],
            [0, m11, 0, 0],
            [0, 0, m22, 1],
            [0, 0, m32, 0]
        ])
        
        # Matriz de projeção para a tela, composição da mesma
        # A matriz em si é uma projeção ortográfica. Em gráficos 3D, uma matriz de projeção ortográfica 
        # é usada para transformar coordenadas 3D em coordenadas 2D de uma maneira que preserva a relação 
        # de distância entre os pontos (ou seja, objetos não ficam menores à medida que se afastam).
        HW, HH = render.H_WIDTH, render.H_HEIGHT
        
        self.to_screen_matrix = np.array([
            [HW, 0, 0, 0],
            [0, -HH, 0, 0],
            [0, 0, 1, 0],
            [HW, HH, 0, 1]
        ])
        