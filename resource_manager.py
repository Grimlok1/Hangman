import pygame
from engine import *
class ResourceManager: #not ready yet
    def __init__(self):
        #put textures here
        self.button_textures = {
            "alphabet_button" : create_button_textures("btn1_on.png", "btn1_hover.png", deactivated_file="btn1_off.png"),
        }

        self.button_text_surfaces = {
            "alphabet_button" : create_button_surfaces(TextSurface(20, "black"), TextSurface(20, "white"), deactivated_surf=TextSurface(30, "gray")),
            "main_menu_button" : create_button_surfaces(TextSurface(50, "white"), TextSurface(55, "yellow")),
        }
        self.textures = {
            "bg_play" : Texture("bg_play.png")
        }
        #put fonts here
        self.fonts = {
            "score_font" : pygame.font.Font(size=32),
            "main_menu_font" : pygame.font.Font(size=50),
            "game_over_font" : pygame.font.Font(None, 60)
        }
    def get_button_texture(self, texture):
        return self.button_textures[texture]

    def get_button_text_surfaces(self, surface):
        return self.button_text_surfaces[surface]

    def get_texture(self, texture):
        return self.textures[texture]

    def get_fonts(self, font):
        return self.fonts[font]
resource_manager = ResourceManager()