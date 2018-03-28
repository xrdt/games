# Author: Bianca Yang
import pygame

# An implementation of tic tac toe.

pygame.init()

# COLORS
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
BLUE =  (  0,   0, 255)
RED =   (255,   0,   0)


size = [600, 600]
screen = pygame.display.set_mode(size)

radius = 90

def find_boundaries(center, radius):
    # Find coordinates of bounding rectangle
    upper_left = (center[0] - radius, center[1] - radius)
    lower_right = (center[0] + radius, center[1] + radius)
    upper_right = (center[0] + radius, center[1] - radius)
    lower_left = (center[0] - radius, center[1] + radius)

    return ([upper_left[0], upper_left[1]],
            [lower_right[0], lower_right[1]],
            [upper_right[0], upper_right[1]],
            [lower_left[0], lower_left[1]])


def find_ellipse_rect(center, radius):
    # Find the rectangle definition for the ellipse
    return center[0] - radius, center[1] - radius, radius * 2, radius * 2


def handle_placement(player, mouse_pos, filled_boxes):
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
        if filled_boxes[0][0] != 0:
            return False
        draw_item((98, 98), player)
        filled_boxes[0][0] = player
    # Upper middle box
    elif mouse_pos[0] <= 397 and mouse_pos[1] <= 197:
        if filled_boxes[0][1] != 0:
            return False
        draw_item((297, 98), player)
        filled_boxes[0][1] = player
    # Upper right box
    elif mouse_pos[0] <= 600 and mouse_pos[1] <= 197:
        if filled_boxes[0][2] != 0:
            return False
        draw_item((500, 98), player)
        filled_boxes[0][2] = player
    # Middle left box
    elif mouse_pos[0] <= 197 and mouse_pos[1] <= 397:
        if filled_boxes[1][0] != 0:
            return False
        draw_item((98, 297), player)
        filled_boxes[1][0] = player
    # Middle middle box
    elif mouse_pos[0] <= 397 and mouse_pos[1] <= 397:
        if filled_boxes[1][1] != 0:
            return False
        draw_item((297, 297), player)
        filled_boxes[1][1] = player
    # Middle right box
    elif mouse_pos[0] <= 600 and mouse_pos[1] <= 397:
        if filled_boxes[1][2] != 0:
            return False
        draw_item((500, 297), player)
        filled_boxes[1][2] = player
    # Lower left box
    elif mouse_pos[0] <= 197 and mouse_pos[1] <= 600:
        if filled_boxes[2][0] != 0:
            return False
        draw_item((98, 500), player)
        filled_boxes[2][0] = player
    # Lower middle box
    elif mouse_pos[0] <= 397 and mouse_pos[1] <= 600:
        if filled_boxes[2][1] != 0:
            return False
        draw_item((297, 500), player)
        filled_boxes[2][1] = player
    # Lower right box
    else:
        if filled_boxes[2][2] != 0:
            return False
        draw_item((500, 500), player)
        filled_boxes[2][2] = player

    if player == 1:
        return 2, filled_boxes
    else:
        return 1, filled_boxes


def draw_item(center, player):
    # Drawing red circle for player 1
    #     boundaries = find_ellipse_rect((500, 500), 90)
    #     pygame.draw.ellipse(screen, RED, boundaries, 3)

    # Drawing blue x for player 2
    #     boundaries2 = find_boundaries((500, 500), 90)
    #     pygame.draw.line(screen, BLUE, boundaries2[0], boundaries2[1], 5)
    #     pygame.draw.line(screen, BLUE, boundaries2[2], boundaries2[3], 5)

    # Red circle
    if player == 1:
        boundaries = find_ellipse_rect(center, radius)
        pygame.draw.ellipse(screen, RED, boundaries, 3)
    # Blue X
    else:
        boundaries2 = find_boundaries(center, radius)
        pygame.draw.line(screen, BLUE, boundaries2[0], boundaries2[1], 5)
        pygame.draw.line(screen, BLUE, boundaries2[2], boundaries2[3], 5)

    pygame.display.update(pygame.Rect(center[0]-radius, center[1]-radius,
                                      radius*2, radius*2))


def check_win(filled_boxes):
    # Check if a player has won the board
    for i in range(3):
        # horizontal
        if filled_boxes[i] == [1, 1, 1] or filled_boxes[i] == [2, 2, 2]:
            return filled_boxes[i][0]
        # vertical
        if filled_boxes[0][i] == filled_boxes[1][i] == filled_boxes[2][i]:
            return filled_boxes[0][i]

    # Diagonal /
    if filled_boxes[2][0] == filled_boxes[1][1] == filled_boxes[0][2]:
        return filled_boxes[2][0]

    # Diagonal \
    if filled_boxes[0][0] == filled_boxes[1][1] == filled_boxes[2][2]:
        return filled_boxes[1][1]

    # Draw
    if 0 not in [j for i in filled_boxes for j in i]:
        return 'draw'


screen.fill(WHITE)

# vertical lines
pygame.draw.line(screen, BLACK, [197, 0], [197, 600], 5)
pygame.draw.line(screen, BLACK, [397, 0], [397, 600], 5)

# horizontal lines
pygame.draw.line(screen, BLACK, [0, 197], [600, 197], 5)
pygame.draw.line(screen, BLACK, [0, 397], [600, 397], 5)
pygame.display.flip()

done = False
player = 1
filled_boxes = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
played = False


while not done:
    if played:
        winner = check_win(filled_boxes)
        if winner:
            print(winner)
            done = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            return_val = handle_placement(player, pygame.mouse.get_pos(),
                                          filled_boxes)
            if return_val is False:
                continue
            else:
                player, filled_boxes = return_val

    played = True
