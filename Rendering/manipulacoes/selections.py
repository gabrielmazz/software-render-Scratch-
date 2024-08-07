import os
import Rendering.software.SoftwareRender as sr

from Rendering.software.colors import *


def select_color(color):
    
    # Declara a paleta de cores
    paleta = Colors()
    
    if color == 1:
        color = paleta.BLACK
    elif color == 2:
        color = paleta.WHITE
    elif color == 3:
        color = paleta.RED
    elif color == 4:
        color = paleta.GREEN
    elif color == 5:
        color = paleta.BLUE
    elif color == 6:
        color = paleta.YELLOW
    elif color == 7:
        color = paleta.CYAN
    elif color == 8:
        color = paleta.MAGENTA
    elif color == 9:
        color = paleta.SILVER
    elif color == 10:
        color = paleta.GRAY
    elif color == 11:
        color = paleta.MAROON
    elif color == 12:
        color = paleta.DARK_GREEN
    elif color == 13:
        color = paleta.PURPLE
    elif color == 14:
        color = paleta.NAVY
    elif color == 15:
        color = paleta.ORANGE
    elif color == 16:
        color = paleta.BROWN
    elif color == 17:
        color = paleta.LIME
    elif color == 18:
        color = paleta.PINK
    elif color == 19:
        color = None
        
    return color
    
def options_menu():
    
    sr.clear_screen()
                
    print("Menu de cores")
    print("1 - Preto")
    print("2 - Branco")
    print("3 - Vermelho")
    print("4 - Verde")
    print("5 - Azul")
    print("6 - Amarelo")
    print("7 - Ciano")
    print("8 - Magenta")
    print("9 - Prata")
    print("10 - Cinza")
    print("11 - Marrom")
    print("12 - Verde escuro")
    print("13 - Roxo")
    print("14 - Azul marinho")
    print("15 - Laranja")
    print("16 - Marrom")
    print("17 - Limão")
    print("18 - Rosa\n")
    print("Digite a opção desejada: ")

    color = int(input())
    
    color = select_color(color)
               
    return color