import pygame as pg
import os
from Rendering.software.colors import *

color = Colors()

class SoftwareMenu():
    
    def __init__(self):
        
        pg.init()                                                           # Inicializa o pygame
        self.RES = self.WIDTH, self.HEIGHT = 1600, 900                      # Resolução da janela (WIDTH, HEIGHT) -> (Largura, Altura)
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2     # Meio da tela, para centralizar os objetos na tela
        self.FPS = 120                                                      # Frames por segundo da janela
        self.screen = pg.display.set_mode(self.RES)                         # Cria a janela com a resolução definida 
        self.clock = pg.time.Clock()                                        # Cria um relogio para controlar o FPS
        
        self.constants()
        self.create_button()
        self.logo()
        
    def constants(self):
        
        self.BUTTOL_COLOR = color.WHITE
        self.BUTTON_HOVER_COLOR = (100, 100, 100)
        self.BUTTON_FONT_COLOR = color.BLACK
        self.BUTTON_FONT = 'Arial'
        self.BUTTON_FONT_SIZE = 24
        self.BUTTON_MARGIN = self.H_WIDTH - 100
        self.BUTTON_SPACING = 20
        self.BUTTON_WIDTH = 200
        self.BUTTON_HEIGHT = 50
      
    def create_button(self):
        
        # Create the buttons
        self.button1 = pg.Rect(self.BUTTON_MARGIN, self.HEIGHT // 2 - self.BUTTON_HEIGHT // 2 - self.BUTTON_SPACING, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.button2 = pg.Rect(self.BUTTON_MARGIN, self.HEIGHT // 2 + self.BUTTON_SPACING, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        self.button3 = pg.Rect(self.BUTTON_MARGIN, self.HEIGHT // 2 + self.BUTTON_HEIGHT + self.BUTTON_SPACING * 2, self.BUTTON_WIDTH, self.BUTTON_HEIGHT)
        
        # Create the text
        font = pg.font.Font(None, 20)
        
        text1 = font.render("Rederização por revolução", True, color.BLACK)
        text2 = font.render("Rederização direta", True, color.BLACK)
        text3 = font.render("Objetos importados", True, color.BLACK)

        # Center the text
        text_rect1 = text1.get_rect(center=(self.button1.centerx, self.button1.centery))
        text_rect2 = text2.get_rect(center=(self.button2.centerx, self.button2.centery))
        text_rect3 = text3.get_rect(center=(self.button3.centerx, self.button3.centery))

        return text1, text2, text_rect1, text_rect2, text3, text_rect3

    def draw(self):
        
        # Draw the buttons
        pg.draw.rect(self.screen, self.BUTTOL_COLOR, self.button1)
        pg.draw.rect(self.screen, self.BUTTOL_COLOR, self.button2)
        pg.draw.rect(self.screen, self.BUTTOL_COLOR, self.button3)
        
        # Draw the logo
        self.screen.blit(self.img, (self.H_WIDTH - 200, 100))
        
        # Escreve em baixo da logo a versão do software
        font = pg.font.Font(None, 20)
        text = font.render("CG_Software_Rendering v1.05", True, color.WHITE)
        self.screen.blit(text, (self.H_WIDTH - 100, 310))
        
        # Mostra os textos nos botões
        text1, text2, text_rect1, text_rect2, text3, text_rect3 = self.create_button()
        self.screen.blit(text1, text_rect1)
        self.screen.blit(text2, text_rect2)
        self.screen.blit(text3, text_rect3)

    def logo(self):
        
        # Pega o path aonde esta o arquivo object.obj por meio do os
        current_directory = os.getcwd()
        self.img = pg.image.load(current_directory + "/Menu/img/logo.png")
        
        # Redimensiona a imagem
        self.img = pg.transform.scale(self.img, (self.img.get_width() // 2, self.img.get_height() // 2))
        
    def run(self):
            
        while True:
            
            self.screen.fill(color.BLACK)
            self.draw()
            
            for event in pg.event.get():
                
                if event.type == pg.QUIT:
                    pg.quit()
                    return
                
                # Check for mouse button events
                elif event.type == pg.MOUSEBUTTONDOWN:
                    
                    # Check which button was clicked
                    mouse_pos = pg.mouse.get_pos()
                    
                    if self.button1.collidepoint(mouse_pos):
                        return 1
                        
                    elif self.button2.collidepoint(mouse_pos):
                        return 2
                    
                    elif self.button3.collidepoint(mouse_pos):
                        return 3
                        
                elif event.type == pg.KEYDOWN and event.key == pg.K_DELETE:
                    pg.quit()
                        
            
            pg.display.set_caption(f'Menu')
            pg.display.flip()
            self.clock.tick(self.FPS)