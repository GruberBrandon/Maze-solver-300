import pygame


# This class holds all the functions related to creating, displaying and running the functions related specific buttons.
class Button:
    def __init__(self, txt, position, action, button_colour, font_colour, size, font_name, font_size):
        self.color = button_colour  # the static (normal) color
        self.bg = button_colour  # actual background color, can change on mouseover
        self.fg = font_colour  # text color
        self.size = size

        self.font = pygame.font.SysFont(font_name, font_size)
        self.txt = txt
        self.txt_surf = self.font.render(self.txt, True, self.fg)
        self.txt_rect = self.txt_surf.get_rect(center=[s // 2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=position)

        self.call_back_ = action

    # Function which when called creates the button in the GUI.
    def draw(self, screen):
        self.mouseover()
        self.surface.fill(self.bg)
        self.surface.blit(self.txt_surf, self.txt_rect)
        screen.blit(self.surface, self.rect)

    # Function which changes the background colour of the button when the user points the cursor over the button.
    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = (220, 220, 220)  # mouseover color

    # Function which calls the operation associated with the button when clicked.
    def call_back(self):
        self.call_back_()
