'''
Modelled on One-Dimensional Quantum Tunneling

QUANTUM SNAKE
A classic snake game with a quantum twist, featuring the following:
1) A classical snake
2) Potential barriers with constant potential throughout
3) A quantum food particle, whose motion is constrained in one dimension at a time

Developed by by Kishal Tandel on April 23, 2025.

Read more about One-Dimensional Quantum Tunneling: https://docs.google.com/viewerng/viewer?url=https://raw.githubusercontent.com/KishalTandel/Papers/refs/heads/main/One-Dimensional+Quantum+Tunneling.pdf

'''


# Importing Modules
import pygame 
import random
import numpy as np


# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
FOOD_RADIUS = GRID_SIZE // 4


# Game Initialization 
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Snake Game")
clock = pygame.time.Clock()


# Colors 
BG_COLOR = (34, 34, 42)
SNAKE_COLOR = (255, 152, 0)
FOOD_COLOR = (240, 17, 17)
BARRIER_RGBA = (3, 169, 176, 120)
SEGMENT_COLOR = (150, 150, 150)
TEXT_COLOR = (255, 255, 255)


# Fonts 
font = pygame.font.SysFont("Roboto Condensed", 24, bold=True)


# Game State 
snake = [[300, 300]]
direction = None
score = 0
high_score = 0


# Food
food_pos = [random.randint(GRID_SIZE, (WIDTH - 2*GRID_SIZE)//GRID_SIZE)*GRID_SIZE,
            random.randint(GRID_SIZE, (HEIGHT - 2*GRID_SIZE)//GRID_SIZE)*GRID_SIZE]
food_direction = random.choice(["horizontal", "vertical"])
food_velocity = GRID_SIZE if random.choice([True, False]) else -GRID_SIZE


# Barriers
barriers = []
barrier_surface = pygame.Surface((GRID_SIZE * 4, GRID_SIZE * 4), pygame.SRCALPHA)
barrier_surface.fill(BARRIER_RGBA)


# Timer Events 
SNAKE_MOVE_EVENT = pygame.USEREVENT + 1
FOOD_MOVE_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SNAKE_MOVE_EVENT, 100)
pygame.time.set_timer(FOOD_MOVE_EVENT, 300)


# Functions 
def spawn_barriers():
    global barriers
    barriers = []
    while len(barriers) <6:
        x = random.randint(0, (WIDTH - GRID_SIZE * 4) // GRID_SIZE) * GRID_SIZE
        y = random.randint(0, (HEIGHT - GRID_SIZE * 4) // GRID_SIZE) * GRID_SIZE
        if (x <= 300 or 320 <= x <= 520) and (y <= 300 or 320 <= y <= 520) and all(abs(x - bx) >= 70 and abs(y - by) >= 70 for bx, by in barriers):
            barriers.append([x, y])


def draw_snake():
    for idx, segment in enumerate(snake):
        color = SNAKE_COLOR if idx == 0 else SEGMENT_COLOR
        pygame.draw.rect(screen, color, (*segment, GRID_SIZE, GRID_SIZE))


def draw_food():
    pygame.draw.circle(screen, FOOD_COLOR,
                       (food_pos[0] + GRID_SIZE // 2, food_pos[1] + GRID_SIZE // 2), FOOD_RADIUS)


def draw_barriers():
    for bx, by in barriers:
        screen.blit(barrier_surface, (bx, by))


def draw_score():
    score_text = font.render(f"Score : {score}  Highest Score : {high_score}", True, TEXT_COLOR)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))


def reset_game():
    global snake, direction, score
    snake = [[300, 300]]
    direction = None
    spawn_barriers()
    spawn_food()
    score = 0


def move_snake():
    global score, high_score,food_velocity

    if not direction:
        return
    
    head = snake[0][:]

    if direction == "UP":
        head[1] -= GRID_SIZE
    elif direction == "DOWN":
        head[1] += GRID_SIZE
    elif direction == "LEFT":
        head[0] -= GRID_SIZE
    elif direction == "RIGHT":
        head[0] += GRID_SIZE

    snake.insert(0, head)

    if head == food_pos:
        spawn_food()
        score += 10
        high_score = max(high_score, score)
    else:
        snake.pop()    


    # Collision with wall
    if direction=='UP':
        if head[1] <= -GRID_SIZE:
            reset_game()
    elif direction=='DOWN':
        if head[1] >= HEIGHT:
            reset_game()
    elif direction=='LEFT':
        if head[0] <= -GRID_SIZE:
            reset_game()
    elif direction=='RIGHT':
        if head[0] >= WIDTH:
            reset_game()


    # Collision with body segment        
    if head in snake[1:]:
        reset_game()

    # Collision with barrier 
    for bx, by in barriers:
        if bx <= head[0] < bx + GRID_SIZE * 4 and by <= head[1] < by + GRID_SIZE * 4:
            reset_game()


def spawn_food():
    global food_pos, food_direction, food_velocity

    while True:
        new_x = random.randint(GRID_SIZE, (WIDTH - 2 * GRID_SIZE) // GRID_SIZE) * GRID_SIZE
        new_y = random.randint(GRID_SIZE, (HEIGHT - 2 * GRID_SIZE) // GRID_SIZE) * GRID_SIZE

        # Check overlap with barriers
        overlapping_barrier = any(
            bx <= new_x < bx + GRID_SIZE * 4 and by <= new_y < by + GRID_SIZE * 4
            for bx, by in barriers
        )

        # Check overlap with snake segments
        overlapping_snake = any(
            segment[0] == new_x and segment[1] == new_y
            for segment in snake
        )

        if not overlapping_barrier and not overlapping_snake:
            food_pos = [new_x, new_y]
            break

    food_direction = random.choice(["horizontal", "vertical"])
    food_velocity = GRID_SIZE if random.choice([True, False]) else -GRID_SIZE



# Quantum tunneling math: returns True if food tunnels
def attempt_tunnel():
    m=9.1*10**(-31)                # mass of electron (kg)
    a= 10**(-9)                    # barrier width (m)
    V0 = 1.6*10**(-19)             # potential (J)
    eta = random.uniform(0,3)      # eta=E/V0
    hbar=1.055*10**(-34)           # Reduced Planck's constant (J.s)
    
    # For clarity, read the paper: 'One-Dimensional Quantum Tunneling' at https://docs.google.com/viewerng/viewer?url=https://raw.githubusercontent.com/KishalTandel/Papers/refs/heads/main/One-Dimensional+Quantum+Tunneling.pdf
    if eta < 1:
        kappa = np.sqrt(2 * m * V0 * (1 - eta)) / hbar
        T = 1 / (1 + (np.sinh(kappa * a))**2 / (4 * eta * (1 - eta)))

    elif eta == 1:
        k = np.sqrt(2 * m * V0) / hbar
        T = 1 / (1 + (k * a / 2)**2)

    else:  # eta > 1
        alpha = np.sqrt(2 * m * V0 * (eta - 1)) / hbar
        T = 1 / (1 + (np.sin(alpha * a))**2 / (4 * eta * (eta - 1)))

    return T>=random.uniform(0,1)


def move_food():
    global food_velocity,food_direction

    next_x = food_pos[0]
    next_y = food_pos[1]

    if food_direction == "horizontal":
        next_x += food_velocity
    else:
        next_y += food_velocity 
    

    # Bounce off on collision with snake segments
    if snake[1:]:
        if food_direction=='horizontal':
                for segment in snake[1:]:
                    seg_rect = pygame.Rect(*segment, GRID_SIZE, GRID_SIZE)
                    food_rect = pygame.Rect(next_x, food_pos[1], GRID_SIZE, GRID_SIZE)
                    if seg_rect.colliderect(food_rect):
                        food_velocity*=-1
                        return
        elif food_direction=='vertical':
                for segment in snake[1:]:
                    seg_rect = pygame.Rect(*segment, GRID_SIZE, GRID_SIZE)
                    food_rect = pygame.Rect(food_pos[0], next_y, GRID_SIZE, GRID_SIZE)
                    if seg_rect.colliderect(food_rect):
                        food_velocity*=-1
                        return


    # Tunneling/Reflection Check 
    for bx, by in barriers:
        bx1, by1 = bx, by
        bx2, by2 = bx + GRID_SIZE * 4, by + GRID_SIZE * 4

        if food_direction == "horizontal":
            if food_velocity > 0 and food_pos[0] + FOOD_RADIUS <= bx1 and next_x + FOOD_RADIUS > bx1 and  by1 < food_pos[1] - FOOD_RADIUS and by2 > food_pos[1] + FOOD_RADIUS:
                if not attempt_tunnel():
                    food_velocity *= -1
                    return
            elif food_velocity < 0 and food_pos[0] + FOOD_RADIUS >= bx2 and next_x + FOOD_RADIUS < bx2 and by1 < food_pos[1] - FOOD_RADIUS and by2 > food_pos[1] + FOOD_RADIUS:
                if not attempt_tunnel():
                    food_velocity *= -1
                    return

        elif food_direction == "vertical":
            if food_velocity > 0 and food_pos[1] + FOOD_RADIUS <= by1 and next_y + FOOD_RADIUS > by1 and bx1 < food_pos[0] - FOOD_RADIUS and bx2 > food_pos[0] + FOOD_RADIUS:
                if not attempt_tunnel():
                    food_velocity *= -1
                    return
            elif food_velocity < 0 and food_pos[1] + FOOD_RADIUS >= by2 and next_y + FOOD_RADIUS < by2 and  bx1 < food_pos[0] - FOOD_RADIUS and bx2 > food_pos[0] + FOOD_RADIUS:
                if not attempt_tunnel():
                    food_velocity *= -1
                    return


    # Move food
    food_pos[0] = next_x if food_direction == "horizontal" else food_pos[0]
    food_pos[1] = next_y if food_direction == "vertical" else food_pos[1]

    # Bounce off walls
    if food_pos[0] - FOOD_RADIUS < 0 or food_pos[0] + GRID_SIZE >= WIDTH :
        food_velocity *= -1
    if food_pos[1] - FOOD_RADIUS < 0 or food_pos[1] + GRID_SIZE >= HEIGHT:
        food_velocity *= -1


# Game Setup 
spawn_barriers()
spawn_food()

# Game Loop
running = True
while running:
    screen.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == SNAKE_MOVE_EVENT:
            move_snake()
        elif event.type == FOOD_MOVE_EVENT:
            move_food()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_s and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_a and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_d and direction != "LEFT":
                direction = "RIGHT"

    draw_snake()
    draw_food()
    draw_barriers()
    draw_score()
    pygame.display.update()
    clock.tick(60)


pygame.quit()