from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import math
import shutil
import os

INPUT_VALUE = None

def tkinter_input():
    
    def get_input():
        
        global INPUT_VALUE
        
        INPUT_VALUE = entry.get()
        
        window.destroy()

    window = tk.Tk()
    window.title("Quantidade de fatias desejadas:")
    window.geometry("300x100")

    entry = tk.Entry(window)
    entry.pack(pady=20)

    button = tk.Button(window, text="OK", command=get_input)
    button.pack()

    window.mainloop()

class Points_Object():
    
    def __init__(self):
        
        # Pontos no campo 2D
        self.points_line = []    
        self.x = []
        self.y = []
        
        # Pontos no campo 3D
        
        self.points_x = []
        self.points_y = []
        self.points_z = []
        
        # Revolução
        self.slices = None
        self.theta = None
        self.xn = None
        self.yn = None
        self.zn = None
            
    # 2D
    def append_points(self, points):
        self.points_line.append(points)
        print(self.points_line)
        
    def clear_points(self):
        self.points_line.clear()    
    
    def print_points(self):
        print(self.points_line)
     
    def points_x_2d(self):
        return np.array([point[0] for point in self.points_line])
    
    def points_y_2d(self):  
        return np.array([point[1] for point in self.points_line])
    
    def reverse_points(self, points):
        return points[::-1]
    
    # 3D    
    def revolucion(self):
        
        
        # Define os pontos no eixo x e y
        self.x = self.points_x_2d()
        self.y = self.points_y_2d()

        # Salva as coordenadas do ponto inicial
        initial_point = (self.x[0], self.y[0])

        # Translada os pontos para que o ponto inicial esteja na origem
        self.x = [x - initial_point[0] for x in self.x]
        self.y = [y - initial_point[1] for y in self.y]

        # Passa o valor do INPUT_VALUE para slices
        self.slices = tkinter_input()

        self.slices = int(INPUT_VALUE)

        # Parametriza
        self.theta = np.linspace(0, np.pi * 2, self.slices)

        # Adicionar um ponto extra na base para fechar a parte inferior
        self.x.append(0)
        self.y.append(min(self.y))

        # Parametriza x, y
        self.xn = np.outer(self.x, np.cos(self.theta))
        self.yn = np.outer(self.x, np.sin(self.theta))

        # Cria uma array z vazia do shape de x / y
        self.zn = np.zeros_like(self.xn)

        # Cria uma array vazia para o z
        # Copia os valores de y do plano 2D para o circulo de revolução
        for i in range(len(self.x)):
            self.zn[i:i+1, :] = np.full_like(self.zn[0, :], self.y[i])

        # Ajustar as matrizes para criar apenas 4 faces
        self.xn = np.column_stack((self.xn, self.xn[:, 0]))
        self.yn = np.column_stack((self.yn, self.yn[:, 0]))
        self.zn = np.column_stack((self.zn, self.zn[:, 0]))

        # Translada os pontos de volta à sua posição original
        self.xn = self.xn + initial_point[0]
        self.yn = self.yn + initial_point[1]
    
        # Cria o objeto
        self.create_object()
                     
    def create_object(self):

        # Define o nome do arquivo
        self.obj_filename = 'object.obj'
        
        # Abre o arquivo
        with open(self.obj_filename, 'w') as f:
                
            # Escreve os pontos todos os pontos de X, Y e Z
            for i in range(len(self.xn)):
                for j in range(self.slices):
                    f.write(f'v {self.xn[i][j]} {self.yn[i][j]} {self.zn[i][j]}\n')
                    
            # Escreve as faces
            for i in range(len(self.xn)-1):
                for j in range(self.slices-1):
                    f.write(f'f {i*self.slices+j+1} {i*self.slices+j+2} {i*self.slices+j+2+self.slices}\n')
                    f.write(f'f {i*self.slices+j+1} {i*self.slices+j+1+self.slices} {i*self.slices+j+2+self.slices}\n')
            
        # Salva os pontos em outro arquivo .txt usando numpy
        np.savetxt('xn.txt', self.xn, delimiter=',')
        np.savetxt('yn.txt', self.yn, delimiter=',')
        np.savetxt('zn.txt', self.zn, delimiter=',')
        
        np.savetxt('x.txt', self.x, delimiter=',')
        np.savetxt('y.txt', self.y, delimiter=',')

        # Pega o path aonde esta o arquivo object.obj por meio do os
        current_directory = os.getcwd()

        # Transfere o arquivo para a pasta Rendering/resources
        arquivo_origem = current_directory + '/object.obj'
        pasta_destino = current_directory + '/Rendering/resources'
        
        # Deleta o arquivo antigo na pasta destino
        if os.path.exists(f'{pasta_destino}/{self.obj_filename}'):
            os.remove(f'{pasta_destino}/{self.obj_filename}')
        
        shutil.move(arquivo_origem, pasta_destino)
        
        # Transfere os arquivos .txt para a pasta Rendering/resources/coord_wireframe
        arquivo_origem_x = current_directory + '/xn.txt'
        arquivo_origem_y = current_directory + '/yn.txt'
        arquivo_origem_z = current_directory + '/zn.txt'

        pasta_destino = current_directory + '/Rendering/resources/coord_wireframe'
        
        # Deleta os arquivos antigos na pasta destino
        if os.path.exists(f'{pasta_destino}/xn.txt'):
            os.remove(f'{pasta_destino}/xn.txt')
            
        if os.path.exists(f'{pasta_destino}/yn.txt'):
            os.remove(f'{pasta_destino}/yn.txt')
            
        if os.path.exists(f'{pasta_destino}/zn.txt'):
            os.remove(f'{pasta_destino}/zn.txt')
        
        shutil.move(arquivo_origem_x, pasta_destino)
        shutil.move(arquivo_origem_y, pasta_destino)
        shutil.move(arquivo_origem_z, pasta_destino)
        
        # Transfere os arquivos .txt para a pasta Rendering/resources/coord_wireframe
        arquivo_origem_x = current_directory + '/x.txt'
        arquivo_origem_y = current_directory + '/y.txt'
        
        pasta_destino = current_directory + '/Rendering/resources/coord_wireframe'
        
        # Deleta os arquivos antigos na pasta destino
        if os.path.exists(f'{pasta_destino}/x.txt'):
            os.remove(f'{pasta_destino}/x.txt')
            
        if os.path.exists(f'{pasta_destino}/y.txt'):
            os.remove(f'{pasta_destino}/y.txt')
            
        shutil.move(arquivo_origem_x, pasta_destino)
        shutil.move(arquivo_origem_y, pasta_destino)