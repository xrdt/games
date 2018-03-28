import pygame
import random


class Game:
    def __init__(self, scene, size):
        self.current = scene
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        self.play()

    def play(self):
        self.current.render(self.screen)

        current_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    result = self.current.clicked(pygame.mouse.get_pos())
                    if result:
                        self.current = result
                        self.current.render(self.screen)

            clock.tick(10)


class AISelection:
    def __init__(self, shape):
        # This is player one's shape
        self.shape = shape


    def render(self, screen):
        screen.fill([255, 255, 255])
        Shape().text(screen, 'Would you Like to Play Against an AI?', 300, 150,
                   pygame.font.SysFont('Times New Roman', 30), (0, 0, 0), True)

        self.yes = Button((0, 0, 0), 'Yes', 100, 200, [150, 300],
                          5, pygame.font.SysFont('Times New Roman',
                                                 30))
        self.yes.render(screen)

        self.no = Button((0, 0, 0), 'No', 100, 200, [450, 300],
                           5, pygame.font.SysFont('Times New Roman',
                                                  30))
        self.no.render(screen)
        pygame.display.flip()


    def clicked(self, position):
        if self.yes.clicked(position):
            starter = random.choice([1, 'AI'])
            return PlayerChoice(self.shape, starter, True)
        elif self.no.clicked(position):
            starter = random.choice([1, 2])
            return PlayerChoice(self.shape, starter, False)


class PlayerChoice:
    def __init__(self, shape, starter, AI):
        self.starter = starter
        self.shape = shape
        self.ai = AI

    def render(self, screen):
        screen.fill((255, 255, 255))
        font = pygame.font.SysFont('Times New Roman', 30)
        if self.ai:
            if self.starter == 1:
                other = 'AI'
            else:
                other = 1
        else:
            if self.starter == 1:
                other = 2
            else:
                other = 1

        Shape().text(screen, 'Player {0} will begin against Player {1}'.format(self.starter, other), 300, 300, font, (0, 0, 0), True)
        Shape().text(screen, 'Click to Continue', 300, 400, font, (0, 0, 0),
                     True)
        pygame.display.flip()

    def clicked(self, position):
        return Main(self.shape, self.ai, self.starter)


class AI:
    def play(self, board):
        choice = self.minimax(board, [], 'AI')
        cells = {0: (98, 98), 1: (297, 98), 2: (500, 98), 3: (98, 297),
                 4: (297, 297), 5: (500, 297), 6: (98, 500), 7: (297, 500),
                 8: (500, 500)}
        return cells[choice]


    def minimax(self, board, scores, player):
        # Currently using the random AI
        return self.random_move(board)


    def random_move(self, board):
        return random.choice(self.available_moves(board))


    def available_moves(self, board):
        available = []
        count = 0
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    available.append(count)
                count += 1

        return available


    def winner(self, board):
        # Check if a player has won the board
        for i in range(3):
            # horizontal
            if self.filled_boxes[i] == [1, 1, 1] or \
               self.filled_boxes[i] == [2, 2, 2] and \
               (0 not in self.filled_boxes[i]):
                if i == 0:
                    return self.filled_boxes[i][0]
                elif i == 1:
                    return self.filled_boxes[i][0]
                else:
                    return self.filled_boxes[i][0]
            # vertical
            if self.filled_boxes[0][i] == self.filled_boxes[1][i] \
                                       == self.filled_boxes[2][i] and \
               (self.filled_boxes[0][i] != 0 and self.filled_boxes[1][i] != 0 \
                and self.filled_boxes[2][i] != 0):
                return self.filled_boxes[0][i]

        # Diagonal /
        if self.filled_boxes[2][0] == self.filled_boxes[1][1] \
                                   == self.filled_boxes[0][2] and \
           (self.filled_boxes[2][0] != 0 and self.filled_boxes[1][1] != 0 and \
            self.filled_boxes[0][2] != 0):
            return self.filled_boxes[2][0]

        # Diagonal \
        if (self.filled_boxes[0][0] == self.filled_boxes[1][1] \
                                   == self.filled_boxes[2][2]) and \
           (self.filled_boxes[0][0] != 0 and self.filled_boxes[1][1] != 0 and \
            self.filled_boxes[2][2] != 0):
            return self.filled_boxes[0][0]

        # Draw
        if 0 not in [j for i in self.filled_boxes for j in i]:
            return 0

        return None


class Welcome:
    def __init__(self, message, x, y, font, color, background, centered,
                 button):
        self.message = message
        self.x = x
        self.y = y
        self.font = font
        self.color = color
        self.background = background
        self.centered = centered
        self.button = button


    def render(self, screen):
        screen.fill(self.background)
        pygame.display.flip()
        Shape().text(screen, self.message, self.x, self.y,
                     self.font, self.color, self.centered)
        self.button.render(screen)


    def clicked(self, position):
        if self.button.clicked(position):
            return ShapeSelection()
        return False


class Shape:
    def line(self, screen, color, start, end, thickness):
        pygame.draw.line(screen, color, start, end, thickness)
        height = end[1] - start[1]
        width = end[0] - start[0]
        pygame.display.update([start[0], start[1], height, width])


    def cross(self, screen, color, center, length, thickness):
        boundaries = self.find_boundaries(center, length)
        pygame.draw.line(screen, (0, 0, 255), boundaries[0],
                         boundaries[1], thickness)
        pygame.draw.line(screen, (0, 0, 255), boundaries[2], boundaries[3],
                         thickness)

        pygame.display.update(pygame.Rect(center[0]-length, center[1]-length,
                                          length*2, length*2))


    def circle(self, screen, color, center, radius, thickness):
        boundaries = self.find_ellipse_rect(center, radius)
        pygame.draw.ellipse(screen, color, boundaries, thickness)
        pygame.display.update([boundaries])


    def find_ellipse_rect(self, center, radius):
        # Find the rectangle definition for the ellipse
        return center[0] - radius, center[1] - radius, radius * 2, radius * 2


    def find_boundaries(self, center, radius):
        # Find coordinates of bounding rectangle
        upper_left = (center[0] - radius, center[1] - radius)
        lower_right = (center[0] + radius, center[1] + radius)
        upper_right = (center[0] + radius, center[1] - radius)
        lower_left = (center[0] - radius, center[1] + radius)

        return ([upper_left[0], upper_left[1]],
                [lower_right[0], lower_right[1]],
                [upper_right[0], upper_right[1]],
                [lower_left[0], lower_left[1]])


    def text(self, screen, message, centerx, centery, font, color, centered):
        text = font.render(message, True, color)
        # Position passed in is where the center of the text should be if
        # centered is True
        if centered:
            rectangle = text.get_rect()
            width = rectangle.width
            height = rectangle.height
            top = centerx - width / 2
            left = centery - height / 2

        screen.blit(text, [top, left])
        pygame.display.update([top, left, width, height])


    def rectangle(self, screen, color, top, left, height, width,
                  thickness=None):
        if thickness:
            pygame.draw.rect(screen, color, [top, left, width, height],
                             thickness)
        else:
            pygame.draw.rect(screen, color, [top, left, width, height])

        pygame.display.update([top, left, width, height])


class Button:
    def __init__(self, color, text, height, width, center, thickness, font):
        # Buttons will always be rectangular in this game
        self.text = text
        self.height = height
        self.width = width
        self.center = center
        self.top = center[0] - width/2
        self.left = center[1] - height/2
        self.thickness = thickness
        self.font = font
        self.color = color


    def render(self, screen):
        Shape().rectangle(screen, self.color, self.top, self.left, self.height,
                          self.width, self.thickness)
        Shape().text(screen, self.text, self.center[0], self.center[1],
                     self.font, self.color, True)


    def clicked(self, position):
        if self.within(position):
            return True
        return False


    def within(self, coordinates):
        if coordinates[0] <= (self.center[0] + self.width/2):
            if coordinates[0] >= (self.center[0] - self.width/2):
                if coordinates[1] >= (self.center[1] - self.height/2):
                    if coordinates[1] <= (self.center[1] + self.height/2):
                        return True
        return False


class ShapeSelection:
    def render(self, screen):
        screen.fill([255, 255, 255])
        Shape().text(screen, 'Choose a Shape for Player One', 300, 150,
                   pygame.font.SysFont('Times New Roman', 30), (0, 0, 0), True)
        self.blue= Button((0, 0, 255), 'Blue X', 100, 200, [150, 300],
                          5, pygame.font.SysFont('Times New Roman',
                                                 30))
        self.blue.render(screen)
        self.green = Button((0, 255, 0), 'Green O', 100, 200, [450, 300],
                           5, pygame.font.SysFont('Times New Roman',
                                                  30))
        self.green.render(screen)
        pygame.display.flip()


    def clicked(self, position):
        if self.blue.clicked(position):
            return AISelection('X')
        elif self.green.clicked(position):
            return AISelection('O')


class Main:
    def __init__(self, shape, AI, player):
        # Self.shape records shape for player 1
        self.shape = shape

        # Randomly choose a player to start
        self.player = player
        self.filled_boxes = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.ai = AI


    def render(self, screen):
        screen.fill((255, 255, 255))
        Shape().line(screen, (0, 0, 0), [197, 0], [197, 600], 5)
        Shape().line(screen, (0, 0, 0), [397, 0], [397, 600], 5)

        Shape().line(screen, (0, 0, 0), [0, 197], [600, 197], 5)
        Shape().line(screen, (0, 0, 0), [0, 397], [600, 397], 5)

        pygame.display.flip()

        self.screen = screen
        if self.player == 'AI':
            choice = AI().play(self.filled_boxes)

            clock = pygame.time.Clock()
            current_time = pygame.time.get_ticks()
            while True:
                for event in pygame.event.get():
                    pass

                if pygame.time.get_ticks() - current_time >= 150:
                    break
                clock.tick(5)

            self.handle_placement(choice)



    def clicked(self, position):
        self.handle_placement(position)

        result, player = self.handle_win()
        if result != False:
            if player == 1:
                if self.shape == 'O':
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
            else:
                if self.shape == 'O':
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)
            return End(color, result, player)

        if self.ai:
            choice = AI().play(self.filled_boxes)

            clock = pygame.time.Clock()
            current_time = pygame.time.get_ticks()
            while True:
                for event in pygame.event.get():
                    pass

                if pygame.time.get_ticks() - current_time >= 150:
                    break
                clock.tick(5)

            self.handle_placement(choice)

        result, player = self.handle_win()
        if result != False:
            if player == 1:
                if self.shape == 'O':
                    color = (0, 255, 0)
                else:
                    color = (0, 0, 255)
            else:
                if self.shape == 'O':
                    color = (0, 0, 255)
                else:
                    color = (0, 255, 0)
            return End(color, result, player)


    def handle_win(self):
        # Check if a player has won the board
        for i in range(3):
            # horizontal
            if self.filled_boxes[i] == [1, 1, 1] or \
               self.filled_boxes[i] == [2, 2, 2] and \
               (0 not in self.filled_boxes[i]):
                if i == 0:
                    return (0, 2), self.filled_boxes[i][0]
                elif i == 1:
                    return(3, 4), self.filled_boxes[i][0]
                else:
                    return (5, 7), self.filled_boxes[i][0]
            # vertical
            if self.filled_boxes[0][i] == self.filled_boxes[1][i] \
                                       == self.filled_boxes[2][i] and \
               (self.filled_boxes[0][i] != 0 and self.filled_boxes[1][i] != 0 \
                and self.filled_boxes[2][i] != 0):
                return (i, i + 5), self.filled_boxes[0][i]

        # Diagonal /
        if self.filled_boxes[2][0] == self.filled_boxes[1][1] \
                                   == self.filled_boxes[0][2] and \
           (self.filled_boxes[2][0] != 0 and self.filled_boxes[1][1] != 0 and \
            self.filled_boxes[0][2] != 0):
            return (5, 2), self.filled_boxes[2][0]

        # Diagonal \
        if (self.filled_boxes[0][0] == self.filled_boxes[1][1] \
                                   == self.filled_boxes[2][2]) and \
           (self.filled_boxes[0][0] != 0 and self.filled_boxes[1][1] != 0 and \
            self.filled_boxes[2][2] != 0):
            return (0, 7), self.filled_boxes[0][0]

        # Draw
        if 0 not in [j for i in self.filled_boxes for j in i]:
            return 'draw', None

        return False, None


    def handle_placement(self, mouse_pos):
        # All the box centers:
        # Upper left (98, 98)
        # Upper middle (297, 98)
        # Upper right (500, 98)
        # Middle left (98, 297)
        # Middle middle (297, 297)
        # Middle right (500, 297)
        # Lower left (98, 500)
        # Lower middle (297, 500)
        # Lower right (500, 500)

        # Upper left box
        if mouse_pos[0] <= 197 and mouse_pos[1] <= 197:
            if self.filled_boxes[0][0] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (98, 98), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (98, 98), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (98, 98), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (98, 98), 90, 5)
            self.filled_boxes[0][0] = self.player
        # Upper middle box
        elif mouse_pos[0] <= 397 and mouse_pos[1] <= 197:
            if self.filled_boxes[0][1] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (297, 98), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (297, 98), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (297, 98), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (297, 98), 90, 5)
            self.filled_boxes[0][1] = self.player
        # Upper right box
        elif mouse_pos[0] <= 600 and mouse_pos[1] <= 197:
            if self.filled_boxes[0][2] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (500, 98), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (500, 98), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (500, 98), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (500, 98), 90, 5)
            self.filled_boxes[0][2] = self.player
        # Middle left box
        elif mouse_pos[0] <= 197 and mouse_pos[1] <= 397:
            if self.filled_boxes[1][0] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (98, 297), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (98, 297), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (98, 297), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (98, 297), 90, 5)
            self.filled_boxes[1][0] = self.player
        # Middle middle box
        elif mouse_pos[0] <= 397 and mouse_pos[1] <= 397:
            if self.filled_boxes[1][1] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (297, 297), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (297, 297), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (297, 297), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (297, 297), 90, 5)
            self.filled_boxes[1][1] = self.player
        # Middle right box
        elif mouse_pos[0] <= 600 and mouse_pos[1] <= 397:
            if self.filled_boxes[1][2] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (500, 297), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (500, 297), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (500, 297), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (500, 297), 90, 5)
            self.filled_boxes[1][2] = self.player
        # Lower left box
        elif mouse_pos[0] <= 197 and mouse_pos[1] <= 600:
            if self.filled_boxes[2][0] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (98, 500), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (98, 500), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (98, 500), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (98, 500), 90, 5)
            self.filled_boxes[2][0] = self.player
        # Lower middle box
        elif mouse_pos[0] <= 397 and mouse_pos[1] <= 600:
            if self.filled_boxes[2][1] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (297, 500), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (297, 500), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (297, 500), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (297, 500), 90, 5)
            self.filled_boxes[2][1] = self.player
        # Lower right box
        else:
            if self.filled_boxes[2][2] != 0:
                return False
            if self.player == 1:
                if self.shape == 'X':
                    Shape().cross(self.screen, (255, 0, 0), (500, 500), 90, 3)
                else:
                    Shape().circle(self.screen, (0, 255, 0), (500, 500), 90, 5)
            else:
                if self.shape == 'X':
                    Shape().circle(self.screen, (0, 255, 0), (500, 500), 90, 5)
                else:
                    Shape().cross(self.screen, (0, 255, 0), (500, 500), 90, 5)
            self.filled_boxes[2][2] = self.player

        if self.ai:
            if self.player == 1:
                self.player = 'AI'
            else:
                self.player = 1
        else:
            self.player = (self.player % 2) + 1



class End:
    def __init__(self, color, boxes, player):
        self.color = color
        self.boxes = boxes
        self.player = player

    def render(self, screen):
        # Draw a line through the win
        if self.boxes == 'draw':
            # Middle: (297, 297)
            Shape().rectangle(screen, (255, 255, 255), 242, 277, 40, 110)
            Shape().text(screen, 'DRAW!', 297, 297,
                         pygame.font.SysFont('Times New Roman', 30),
                         (0, 0, 0), True)
        else:
            start, end = self.end_line()
            Shape().line(screen, self.color, start, end, 5)
            Shape().rectangle(screen, (255, 255, 255), 207, 277, 40, 180)
            Shape().text(screen, 'Player {0} Wins!'.format(self.player), 297,
                         297, pygame.font.SysFont('Times New Roman', 30),
                         (0, 0, 0), True)

        # Play Again Button
        Shape().rectangle(screen, (255, 255, 255), 207, 460, 80, 180)
        self.button = Button((0, 0, 0), 'Play Again?', 80, 180, (297, 500), 3,
               pygame.font.SysFont('Times New Roman', 30))
        self.button.render(screen)


    def end_line(self):
        # Figure out the parameters for the winning line
        centers = {0: (98, 98), 1: (297, 98), 2: (500, 98), 3: (98, 297),
                4: (500, 297), 5: (98, 500), 6: (297, 500), 7: (500, 500)}
        return centers[self.boxes[0]], centers[self.boxes[1]]


    def clicked(self, position):
        if self.button.clicked(position):
            return ShapeSelection()


if __name__ == '__main__':
    pygame.init()
    standard_font = pygame.font.SysFont('Times New Roman', 30)
    Game(Welcome('Tic Tac Toe', 300, 250,
                 standard_font, (255, 0, 0),
                 (255, 255, 255), True, Button([0, 0, 0], 'Start Game', 80,
                 500, (300, 350), 3, standard_font)),
          [600, 600])
