import Menu.software.SoftwareRender as sr_menu
import Wireframe.software.SoftwareRender as sr_wireframe
import Rendering.software.SoftwareRender as sr_rendering
import pygame as pg

if __name__ == '__main__':
    
    # Menu
    app_menu = sr_menu.SoftwareMenu()
    opcao = app_menu.run()
    
    # Na primeira opção, o usuário pode escolher entre um wireframe, que será 
    # possivel desenhar um objeto em 2D e será feito uma renderização (revolução)
    # para 3D, ou um objeto que será rasterizado, como um cubo, piramide, etc.
    if opcao == 1:
        
        # Wireframe
        app_wireframe = sr_wireframe.SoftwareWireframe()
        app_wireframe.run()
           
        sr_rendering.clear_screen()
        
        app = sr_rendering.SoftwareRender(opcao=1)
        app.run()
    
    # Nesta opção, objetos que que são especificados pelo usuário, seram 
    # rasterizados, como um cubo, piramide, etc. A classe tem uma leve diferença
    # pois nela mesma, temos coordenadas dos vertices e faces
    elif opcao == 2:
    
        # Rendering
        app = sr_rendering.SoftwareRender(opcao=2)
        app.run()
       
    # Aqui será chamado um método para pegar objetos de um arquivo .obj, que são 
    # objetos são modelados em um software 3D podendo ser importados para o 
    # programa, qualquer objeto baixado na internet 
    elif opcao == 3:
        
        # Rendering
        app = sr_rendering.SoftwareRender(opcao=3)
        app.run()