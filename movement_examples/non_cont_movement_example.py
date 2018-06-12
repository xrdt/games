import pygame

pygame.init()

size = [600, 600]
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

current_time = pygame.time.get_ticks()

screen.fill((255, 255, 255))

class Rectangle:
    def __init__(self, color, position):
        self.color = color
        self.position = position


    def render(self, screen):
        pygame.draw.rect(screen, self.color, self.position)
        pygame.display.flip()


    def move(self, update):
        new_position = (self.position[0] + update[0],
                        self.position[1] + update[1],
                        self.position[2], self.position[3])
        self.position = new_position

        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, self.color, new_position)
        pygame.display.flip()

rect = Rectangle((0, 0, 0), [0, 0, 10, 10])
rect.render(screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rect.move((-1, 0))

            if event.key == pygame.K_RIGHT:
                rect.move((1, 0))

            if event.key == pygame.K_UP:
                rect.move((0, -1))

            if event.key == pygame.K_DOWN:
                rect.move((0, 1))
