import pygame
import random
import math
from pygame import mixer

# Initialise the pregame
pygame.init()

# Create The Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('project.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('alien.png')
playerX = 370
playerY = 480
playerX_Change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_Change = []
enemyY_Change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_Change.append(2)
    enemyY_Change.append(40)

# Bullet
# Read-you cant see the bullet
# Fire-the bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_Change = 0
bulletY_Change = 7
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game_Over_Text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score:" + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER !!! ", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def iscollison(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # RGB=RED,GREEN,BLUE
    screen.fill((100, 100, 100))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Taking key strokes to move Spaceship
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_Change = -5
            if event.key == pygame.K_RIGHT:
                playerX_Change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":  # Get the current x coordinate of the spaceship
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_Change = 0

    playerX += playerX_Change

    # Creating the Boundaries for Spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # GameOver
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_Change[i]
        # Creating the Boundaries for Enemy
        if enemyX[i] <= 0:
            enemyX_Change[i] = 2
            enemyY[i] += enemyY_Change[i]  # Changing the enemy movement down when hitting the boundaries
        elif enemyX[i] >= 736:
            enemyX_Change[i] = -2
            enemyY[i] += enemyY_Change[i]  # Changing the enemy movement down when hitting the boundaries
        # Collision
        collision = iscollison(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_Change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
