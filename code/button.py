import pygame

# Definindo cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (65,105,225)

# Definindo a classe Button
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.Font("fonts/ARCADE_I.TTF", 25)
        self.current_color = WHITE

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)

        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.is_clicked(event.pos):
                self.current_color = BLUE
            else:
                self.current_color = WHITE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.is_hovered(event.pos):
                self.action()

