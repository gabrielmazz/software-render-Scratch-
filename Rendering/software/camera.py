import pygame as pg
import math
from Rendering.manipulacoes.matrix_functions import *

# Classe que fica responsável pela camera utilizada na cena 3D, para declarar a camera, são dado algumas informações
# necessarias para a criação da camera, como a posição inicial, a renderização que será utilizada e a velocidade de movimento
class Camera:
    
    def __init__(self, render, position):
        
        #software/img/sistema de camera sendo top view e side view.png
        
        self.render = render                                        # Renderização que será utilizada
        self.position = np.array([*position, 1.0])                  # Posição da camera É um vetor 4D, onde os três primeiros elementos são as coordenadas x, y, z 
                                                                    # e o último elemento é sempre 1.0 (usado para cálculos de transformação).
                                                                    
        # Vetores que representam a direção da camera que definem a orientação da câmera no espaço 3D.                                                   
        self.forward = np.array((0, 0, 1, 1))                       # Vetor que representa a direção para qual a câmera está "olhando"             
        self.up = np.array((0, 1, 0, 1))                            # Vetor que representa a direção para cima da câmera
        self.right = np.array((1, 0, 0, 1))                         # Vetor que representa a direção para a direita da câmera
        
        # Estes são os campos de visão horizontal e vertical da câmera, respectivamente. O campo de visão é o ângulo através do qual a câmera "vê" o mundo 3D.
        self.h_fov = math.pi / 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        
        # Estes definem a distância mínima e máxima, respectivamente, que a câmera pode "ver". Qualquer coisa mais próxima do que self.near_plane ou mais distante 
        # do que self.far_plane não será renderizada.
        self.near_plane = 0.001
        self.far_plane = 10000
        
        # Estas variaveis são usadas para controlar a velocidade de movimento e rotação da câmera, respectivamente. Presumivelmente, esses valores são usados 
        # quando a posição ou orientação da câmera é atualizada.
        self.moving_speed = 10
        self.rotation_speed = 0.01
    
    # Função que controla a movimentação da camera, onde é verificado se alguma tecla foi pressionada e se sim, a camera se movimenta
    # - A tecla 'a' faz a camera se mover para a esquerda
    # - A tecla 'd' faz a camera se mover para a direita
    # - A tecla 'w' faz a camera se mover para frente
    # - A tecla 's' faz a camera se mover para trás
    # - A tecla 'q' faz a camera subir
    # - A tecla 'e' faz a camera descer
    # - A tecla 'left' faz a camera rotacionar para a esquerda
    # - A tecla 'right' faz a camera rotacionar para a direita
    # - A tecla 'up' faz a camera rotacionar para cima
    # - A tecla 'down' faz a camera rotacionar para baixo
    def control(self):
        
        # Obtém o estado atual do teclado
        key = pg.key.get_pressed()
    
        
        if key[pg.K_a]:
            self.position -= self.right * self.moving_speed
            
        if key[pg.K_d]:
            self.position += self.right * self.moving_speed
            
        if key[pg.K_w]:
            self.position += self.forward * self.moving_speed
            
        if key[pg.K_s]:
            self.position -= self.forward * self.moving_speed
            
        if key[pg.K_q]:
            self.position += self.up * self.moving_speed
            
        if key[pg.K_e]:
            self.position -= self.up * self.moving_speed   
     
        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
            
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
            
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
            
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)
            
        # Ajusta a camera no eixo Y (Resetando a orientação da câmera para a orientação padrão)
        if key[pg.K_r]:
            self.forward = np.array((0, 0, 1, 1))
            self.up = np.array((0, 1, 0, 1))
            self.right = np.array((1, 0, 0, 1))

    # A função camera_yaw está rotacionando a câmera em torno do eixo Y por um ângulo especificado. 
    # Isso é conhecido como "guinada" (ou "yaw") em termos de rotação 3D.    
    # Utilizando a função rotate_y do arquivo matrix_functions.py para rotacionar a camera em torno do eixo Y
    def camera_yaw(self, angle):
        
        rotate = rotate_y(angle)                    # Rotaciona a camera em torno do eixo Y
        self.forward = self.forward @ rotate        # Atualiza o vetor forward -> direção para qual a câmera está "olhando"
        self.right = self.right @ rotate            # Atualiza o vetor right -> direção para a direita da câmera
        self.up = self.up @ rotate                  # Atualiza o vetor up -> direção para cima da câmera
     
    # A função camera_pitch está rotacionando a câmera em torno do eixo X por um ângulo especificado.
    # Isso é conhecido como "arremesso" (ou "pitch") em termos de rotação 3D.
    # Utilizando a função rotate_x do arquivo matrix_functions.py para rotacionar a camera em torno do eixo X 
    def camera_pitch(self, angle):
            
        rotate = rotate_x(angle)                    # Rotaciona a camera em torno do eixo X
        self.forward = self.forward @ rotate        # Atualiza o vetor forward -> direção para qual a câmera está "olhando"
        self.right = self.right @ rotate            # Atualiza o vetor right -> direção para a direita da câmera
        self.up = self.up @ rotate                  # Atualiza o vetor up -> direção para cima da câmera
     
    # A função cria uma matriz de translação 4x4 que é usada para mover a câmera para uma nova posição no espaço 3D.
    def translate_matrix(self):
        
        x, y, z, w = self.position
        
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])
      
    # A função cria uma matriz de rotação 4x4 que é usada para rotacionar a câmera em torno de seu eixo.  
    def rotate_matrix(self):
        
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])
      
    # Combina as matrizes de translação e rotação em uma única matriz de transformação da câmera. Esta matriz pode 
    # ser usada para transformar pontos do espaço do mundo para o espaço da câmera 
    def camera_matrix(self):
        return self.translate_matrix() @ self.rotate_matrix()