import pygame
from sys import exit
from random import uniform, randint

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

bricks = []
BRICK_WIDTH = 70
BRICK_HEIGHT = 30
rows = randint(2, 6)
cols = randint(3, 8)
current_chanel = 1
pygame.mixer.set_num_channels(rows * cols + 3)
max_channel = rows * cols + 3
print(rows, cols)
padding = 10
offset_x = 20
offset_y = 40
random_col_at_start = randint(1, 255), randint(1, 255), randint(1, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('arkanoid (temu version)')

clock = pygame.time.Clock()

#make rows from top mid
total_width = cols * BRICK_WIDTH + (cols - 1) * padding
start_x = (SCREEN_WIDTH - total_width) // 2
bricks = []
for row in range(rows):
    for col in range(cols):
        brick_x = start_x + col * (BRICK_WIDTH + padding)
        brick_y = offset_y + row * (BRICK_HEIGHT + padding)
        brick = pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT)
        bricks.append(brick)

# how to use: display_text("text", text_font, (R, G, B), x, y)
small_font = pygame.font.SysFont('Arial', 25)
text_font = pygame.font.SysFont('Arial', 30)
large_font = pygame.font.SysFont('Arial', 60)
def display_text(text, font, text_col, x, y):
    dr_text = font.render(text, True, text_col)
    screen.blit(dr_text, (x, y))

def events():
    global x
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def move_platform():
    global x
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_a]:
        x = max(0, x - 5)
    if pressed[pygame.K_d]:
        x = min(625, x + 5)
    return x

def cube_colision():
    global c_x, c_y, c_x_speed, c_y_speed, current_chanel

    if rect_cube.colliderect(rect_platform):
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("sound/platform_dink.mp3"))
        c_y = rect_platform.top - 50
        c_y_speed = -abs(c_y_speed)
        print("p_c col")

    for brick in bricks[:]:
        if rect_cube.colliderect(brick):
            print(f"block chanel:{current_chanel}")
            pygame.mixer.Channel(current_chanel).play(pygame.mixer.Sound("sound/block_dink.mp3"))
            current_chanel += 1
            print(f"hit brick:{brick}")
            bricks.remove(brick)
            c_y_speed *= -1
            break
    if c_x <= 0:
        c_x_speed = abs(c_x_speed)
    if c_x + 50 >= SCREEN_WIDTH:
        c_x_speed = -abs(c_x_speed)
    if c_y <= 0:
        c_y_speed = abs(c_y_speed)
    if c_y + 50 >= SCREEN_HEIGHT:
        you_lose()
    return c_x_speed, c_y_speed, current_chanel

def you_win():
    pygame.mixer.Channel(current_chanel + 1).play(pygame.mixer.Sound("sound/you_win.mp3"))
    win_bg = pygame.image.load("images/win_background.png")
    while True:
        events()
        screen.blit(win_bg, (0, 0))
        display_text("You win", large_font, (0, 255, 0), SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 120)
        display_text(":3", large_font, (0, 255, 0), SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60)
        pygame.display.flip()
        clock.tick(60)

def you_lose():
    pygame.mixer.Channel(current_chanel + 1).play(pygame.mixer.Sound("sound/you_lose.mp3"))
    lose_bg = pygame.image.load("images/lose_background.png")
    while True:
        events()
        screen.blit(lose_bg, (0, 0))
        display_text("You lose", large_font, (255, 0, 0), SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 120)
        display_text(":P", large_font, (255, 0, 0), SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 - 60)
        pygame.display.flip()
        clock.tick(60)

x, y = 325, 550
c_x, c_y = 350, 450
c_x_speed, c_y_speed = uniform(3, 5), uniform(3, 5)
pygame.mixer.music.load("sound/bg_wind.mp3") 
pygame.mixer.music.play(-1)

bg = pygame.image.load("images/background.png")
platform_image = pygame.image.load("images/pad.png").convert_alpha()
cube_image = pygame.image.load("images/ball.png").convert_alpha()
brick_image = pygame.image.load("images/brick.png").convert_alpha()
brick_image = pygame.transform.scale(brick_image, (BRICK_WIDTH, BRICK_HEIGHT))

while True:
    events()
    screen.blit(bg, (0, 0))
    move_platform()
    c_y += c_y_speed
    c_x += c_x_speed

    # bullshit to make the cube image go on screen
    rect_cube = pygame.Rect(c_x, c_y, 50, 50)
    cube_image = pygame.transform.scale(cube_image, (rect_cube.width, rect_cube.height))
    screen.blit(cube_image, rect_cube.topleft)

    # bullshit to make the platform image go on screen
    rect_platform = pygame.Rect(x, y, 175, 25)
    platform_image = pygame.transform.scale(platform_image, (rect_platform.width, rect_platform.height))
    screen.blit(platform_image, rect_platform.topleft)

    #draws the bricks in the bricks list
    for brick in bricks:
        screen.blit(brick_image, brick.topleft)
    
    cube_colision()
    if not bricks:
        you_win()
    clock.tick(60)
    display_text(f"x, y:{int(c_x)}, {int(c_y)}", small_font, (255, 255, 0), 0, 0)
    display_text(f"fps:{int(clock.get_fps())}", small_font, (255, 255, 0), 0, 30)
    pygame.display.flip()