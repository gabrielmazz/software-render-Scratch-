import pygame as pg
import shutil
import os

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Graph:
    
    def __init__(self, x, y, zn, xn, yn):
        
        self.x = x
        self.y = y
        self.zn = zn
        self.xn = xn
        self.yn = yn
        
        self.flag_graph = False
    
    def control_graph(self):
        
        # Pega as teclas pressionadas
        key = pg.key.get_pressed()
        
        # Botão P para plotar o gráfico
        if key[pg.K_p]:
            self.plot_graph()
            self.flag_graph = True
        
        # Botão I para fechar o gráfico
        if key[pg.K_i]:
            self.flag_graph = False
 
    def plot_graph(self):
        
        # Cria a figura
        fig = plt.figure(figsize=(12,6))
        
        # Cria os subplots
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122,projection='3d')
        
        # Plota o gráfico 2D e 3D
        ax1.plot(self.x, self.y)
        ax2.plot_surface(self.xn, self.yn, self.zn)
        
        # Adiciona o título
        ax1.set_title('Gráfico 2D')
        ax2.set_title('Gráfico 3D')
        
        # No plot 2D adiciona o label x e y
        ax1.set_xlabel('X')
        ax1.set_ylabel('Y')
        
        # No plot 3D adiciona o label x, y e z
        ax2.set_xlabel('X')
        ax2.set_ylabel('Y')
        ax2.set_zlabel('Z')

        
        fig.savefig('Plot.png')
        
        # Pega o path aonde esta o arquivo object.obj por meio do os
        current_directory = os.getcwd()
        
        pasta_destino = current_directory + '/Rendering/software/img'
        
        # Deleta os arquivos antigos na pasta destino
        if os.path.exists(f'{pasta_destino}/Plot.png'):
            os.remove(f'{pasta_destino}/Plot.png')
        
        # Move o arquivo para a pasta de imagens
        shutil.move('Plot.png', pasta_destino)