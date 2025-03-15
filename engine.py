import pygame

#STATEMACHINE AND STATES ###############################################################
class StateMachine:
    def __init__(self, screen):
        self.states = None
        self.screen = screen
        self.state = None

    def handle_events(self, event):
        self.state.handle_event(event)

    def process(self):
        self.state.process()

    def draw(self):
        self.state.draw()

    def transition_state(self, state):
        self.state = self.states[state]
        self.state.transition_state()

#STATE
class State:
    def __init__(self, state_machine):
        self.state_machine = state_machine  # Store reference to the state machine
        self.screen = self.state_machine.screen

    def handle_event(self, event):
        pass

    def transition_state(self):  # fired when you first transition to state
        pass

    def update(self):
        pass

    def process(self):
        pass

    def draw(self, screen):
        pass

#BUTTON PARENT CLASS ABSTRACT BUTTON
class Button:
    def __init__(self, size, pos, alignment, func):
        self.func = func
        self.state = "normal"
        self.rect = pygame.rect.Rect(pos, size)
        setattr(self.rect, alignment, pos)  # align rectangle here!

    def update(self):
        if self.state == "deactivated":  # skip
            return
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):  # should I change self.rect to self.textures[self.state].rect
            self.hover()
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.on_click()
        else:
            self.normal()  # return to normal

    def hover(self):
        self.state = "hover"

    def normal(self):
        self.state = "normal"

    def on_click(self):
        self.state = "clicked"
        if self.func:
            self.func()

    def draw(self, screen):
        pass
#TEXTBUTTON
class TextButton(Button):
    def __init__(self, pos, string, text_surfaces, alignment="topleft", func=None):
        self.text_surfaces = text_surfaces
        self.re_render_surfaces(string) #rerender text surface
        size = self.text_surfaces["normal"].rect.size
        super().__init__(size, pos, alignment, func)  # align rectangle here

    def re_render_surfaces(self, string):
        for key, text_surface in self.text_surfaces.items():
            if text_surface.string != "": #if string is empty replace it and re-render
                text_surface.re_render(string)

    def draw(self, screen):
        text_surface = self.text_surfaces[self.state]

        if text_surface.rect.center != self.rect.center:  # center text
            text_surface.rect.center = self.rect.center
        screen.blit(text_surface.surf, text_surface.rect)
#TEXTUREBUTTON
class TextureButton(Button):
    def __init__(self, pos, string, textures, text_surfaces, alignment="topleft", func=None):
        self.textures = textures
        self.text_surfaces = text_surfaces
        self.re_render_surfaces(string)
        size = self.textures["normal"].rect.size
        super().__init__(size, pos, alignment, func) #initialize parent class

    def re_render_surfaces(self, string):
        for key, text_surface in self.text_surfaces.items():
            if text_surface.string != "": #if string is empty replace it and re-render
                text_surface.re_render(string)

    def draw(self, screen):
        text_surface = self.text_surfaces[self.state]
        texture_obj = self.textures[self.state]

        if text_surface.rect.center != texture_obj.rect.center != self.rect.center:  # center text, and texture
            text_surface.rect.center = self.rect.center
            texture_obj.rect.center = self.rect.center

        screen.blit(texture_obj.surf, texture_obj.rect)
        screen.blit(text_surface.surf, text_surface.rect)

class Texture:
    def __init__(self, file_path):
        surf = pygame.image.load(file_path)
        self.surf = surf.convert()
        self.rect = self.surf.get_rect()

class TextSurface:
    def __init__(self, size, color, string="", font_file=None):
        self.string = string
        self.color = color
        self.font = pygame.font.Font(font_file, size)
        self.surf = self.font.render(self.string, False, self.color)
        self.rect = self.surf.get_rect()

    def re_render(self, new_string): #re_render surf with a new string
        self.surf = self.font.render(new_string, False, self.color)
        self.rect = self.surf.get_rect()


def create_button_textures(normal_file, hover_file=None, clicked_file=None, deactivated_file=None): #insert file paths here
    normal_texture = Texture(normal_file)
    hover_texture = Texture(hover_file) if hover_file else normal_texture  # Default to normal if not provided
    clicked_texture = Texture(clicked_file) if clicked_file else normal_texture  # Default to normal if not provided
    deactivated_texture = Texture(deactivated_file) if deactivated_file else normal_texture  # Default to normal if not provided

    button_textures = {
    "normal" : normal_texture,
    "hover" : hover_texture,
    "clicked" : clicked_texture,
    "deactivated" : deactivated_texture,
    }
    return button_textures
def create_button_surfaces(normal_surf, hover_surf=None, clicked_surf=None, deactivated_surf=None):
    button_surfs = {
        "normal": normal_surf,
        "hover": hover_surf or normal_surf,
        "clicked": clicked_surf or normal_surf,
        "deactivated": deactivated_surf or normal_surf,
    }
    return button_surfs

class Text1:
    def __init__(self, text, font, color):
        self.text = text
        self.color = color
        self.font = font
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect()

    def re_render(self, text):
        self.text = text
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect()

class PopUpMenu:
    def __init__(self, size, pos, alignment="topleft"):
        self.rect = pygame.rect.Rect(pos, size)
        setattr(self.rect, alignment, pos) #aling rect here!
        self.buttons = []

    def update_position(self, x, y, alignment="topleft"):
        setattr(self.rect, alignment, (x,y))
        old_x = self.rect.x
        old_y = self.rect.y
        x_offset = abs(old_x - x)
        y_offset = abs(old_y - y)
        for btn in self.buttons:
            btn.rect.x += x_offset
            btn.rect.y += y_offset

    def update(self):
        for btn in self.buttons:
            btn.update()

    def draw(self, screen): #0,0
        screen.fill("red", self.rect) #background placeholder
        for btn in self.buttons:
            btn.draw(screen) #draw button to screen

class Timer:
    def __init__(self):
        self.callback = None
        self.start_time = None
        self.running = False
        self.duration = None

    def set_callback(self, duration, callback):
       self.duration = duration * 1000 #convert to milliseconds
       self.callback = callback

    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True

    def stop(self):
        self.running = False

    def update(self):
        if not self.running:
            return

        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration: #if time is up stop the clock
            self.stop()
            if self.callback:
                self.callback()
class Text:
    def __init__(self, text, font, color, pos, anchor_point = "center"):
        self.text = text
        self.font = font
        self.color = color
        self.anchor_point = anchor_point
        self.pos = pos
        self.surf = None
        self.rect = None
        self.render()

    def render(self):
        self.surf = self.font.render(self.text, False, self.color)
        self.rect = self.surf.get_rect()
        setattr(self.rect, self.anchor_point, self.pos) #set position


    def blit(self, screen):
        screen.blit(self.surf, self.rect)


class Line:
    def __init__(self, color, start_pos, end_pos, width=1):
        self.color = color
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.width = width

    def draw(self, surf):
        pygame.draw.line(surf, self.color, self.start_pos, self.end_pos, self.width)

class Circle:
    def __init__(self, color, center, radius, width=1):
        self.color = color
        self.center = center
        self.radius = radius
        self.width = width

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.center, self.radius, self.width)

class MultilineText:
    def __init__(self, screen, text, font, color, pos):
        lines = text.splitlines()
        self.lines = []
        self.screen = screen
        x, y = pos
        line_size = font.get_linesize()
        for line in lines:
            surf = font.render(line, False, color)
            rect = surf.get_rect(center=(x, y))
            l = (surf, rect)
            self.lines.append(l)
            y += line_size
    def blit(self):
        for line in self.lines:
            self.screen.blit(line[0], line[1])