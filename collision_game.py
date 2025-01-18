# incentive to move around : timer
# game over: restart game
import pygame
import random

pygame.init()

white = (255, 255, 255)
red = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
black = (0, 0, 0)

width = 650
height = 700

pixel = 64

fps = 60  # Target frames per second
clock = pygame.time.Clock()  # Create a clock object

screen = pygame.display.set_mode((width, height))

pygame.display.set_caption("corona scarper")

playerImageBig = pygame.image.load("icon.svg")
playerImage = pygame.transform.scale(playerImageBig, (64, 64))
playerXPosition = (width/2) - (pixel/2)
playerYPosition = height - pixel - 10
playerSpeed = 5


def player(x, y):
    # print("player.x "+str(x)+" player.y "+str(y))
    screen.blit(playerImage, (x, y))


enemyImageBig = pygame.image.load("apple.png")
enemyImage = pygame.transform.scale(enemyImageBig, (64, 64))
enemyXPositions = [random.randint(
    0, (width-pixel)), random.randint(0, (width-pixel)), random.randint(0, (width-pixel))]
enemyYPositions = [-pixel, -pixel, -pixel]
enemyXPositionChange = 0
enemyYPositionChange = 5


def enemy(x, y):
    # print("enemy.x "+str(x)+" enemy.y "+str(y))
    screen.blit(enemyImage, (x, y))


# lives setup
font = pygame.font.Font(None, 36)  # Default font with size 36
lives = 3


def show_lives_and_score(x, y, lives, score):
    lives_text = font.render(f"Lives: {lives}", True, white)
    scores_text = font.render(f"Score: {score}", True, white)
    screen.blit(lives_text, (x, y))
    screen.blit(scores_text, (x, y+40))


# bullets setup
bulletImage = pygame.transform.scale(enemyImageBig, (10, 30))
bullets = []
bulletSpeed = 20
last_bullet_time = 0  #


def fire_bullet(x, y):
    bullets.append([x, y])


def update_bullets():
    for bullet in bullets[:]:  # Iterate over a copy of the list
        bullet[1] -= bulletSpeed  # Move the bullet up

        # Remove bullets that go off-screen
        if bullet[1] < 0:
            bullets.remove(bullet)


def draw_bullets():
    for bullet in bullets:
        screen.blit(bulletImage, (bullet[0], bullet[1]))


# score setup
score = 0

# collision code


def check_bullet_collision():
    global score, enemyYPositionChange, playerSpeed
    hit_enemies = []
    for i in range(3):
        enemy_rect = pygame.Rect(
            enemyXPositions[i], enemyYPositions[i], 64, 64)
        for bullet in bullets[:]:
            bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 30)
            if bullet_rect.colliderect(enemy_rect):
                # print("collided")
                score += 1
                bullets.remove(bullet)
                # Ensure you always have 3 enemies
                hit_enemies.append(i)
                enemyXPositions.append(random.randint(0, width - pixel))
                enemyYPositions.append(-pixel)

                if score % 7 == 0:
                    enemyYPositionChange += 1
                    playerSpeed += 0.4

                    print("enemyYPositionChange is "+str(enemyYPositionChange) +
                          " and playerSpeed is "+str(playerSpeed))
                break

    for i in reversed(hit_enemies):
        enemyXPositions[i] = random.randint(0, width - pixel)
        enemyYPositions[i] = -pixel
        # Add a new enemy if necessary to maintain 3 enemies
        if len(enemyXPositions) < 3:
            enemyXPositions.append(random.randint(0, width - pixel))
            enemyYPositions.append(-pixel)


def display_score():
    global score
    scores_text = font.render(f"Score: {score}", True, white)
    screen.blit(scores_text, (width / 2 - 50, height/2 + 40))


def play_again_message():
    # x = width - 150, y = 10
    play_again_text = font.render(
        "Hit Enter To Play \n Hit Esc To Quit", True, white)
    screen.blit(play_again_text, (width / 2 - 200, height/2 - 20))
    return False


def check_collision():
    global lives, score
    player_rect = pygame.Rect(playerXPosition, playerYPosition, pixel, pixel)

    # check player bullet collision
    check_bullet_collision()

    # check player enemy collision
    for i in range(3):  # Iterate over each enemy
        enemy_rect = pygame.Rect(
            enemyXPositions[i], enemyYPositions[i], pixel, pixel)
        if player_rect.colliderect(enemy_rect):
            lives -= 1  # Decrease lives on collision
            # print(f"Lives left: {lives}")
            if lives <= 0:
                print("Game Over!")
                return play_again_message()  # End the game
            else:
                # Reset enemy position
                enemyYPositions[i] = -pixel
                enemyXPositions[i] = random.randint(0, width - pixel)
    return True


running = True
playing = False


def close_button_pressed():
    global lives, running, score, playerXPosition, playerYPosition, enemyYPositions, enemyXPositions, playing, enemyYPositionChange, playerSpeed
    for event in pygame.event.get():
        # check the quit condition
        if event.type == pygame.QUIT:
            # quit the game
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not playing:  # Restart game
                lives = 3
                score = 0
                enemyYPositionChange = 5
                playerSpeed = 5
                playerXPosition = (width / 2) - (pixel / 2)
                playerYPosition = height - pixel - 10
                enemyYPositions = [-pixel, -pixel, -pixel]
                enemyXPositions = [random.randint(
                    0, (width-pixel)), random.randint(0, (width-pixel)), random.randint(0, (width-pixel))]
                playing = True
            elif event.key == pygame.K_ESCAPE:
                running = False


game_iteration = 0
while running:
    clock.tick(fps)

    screen.fill(black)
    # set the image on screen object
    current_time = pygame.time.get_ticks()

    playerXPositionChange = 0
    # check for close event
    close_button_pressed()

    if playing:
        # handle movement key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            playerXPosition += playerSpeed
        elif keys[pygame.K_LEFT]:
            playerXPosition -= playerSpeed
        if keys[pygame.K_SPACE]:
            if current_time - last_bullet_time > 350:  # 1000 ms = 1 second
                fire_bullet(playerXPosition + pixel // 2 - 5, playerYPosition)
                last_bullet_time = current_time

        if playerXPosition < 0:
            playerXPosition = 0
        if playerXPosition > width - pixel:
            playerXPosition = width - pixel

        for i in range(3):
            enemyYPositions[i] += enemyYPositionChange
            # Reset enemy when it moves off-screen
            if enemyYPositions[i] > height:
                enemyYPositions[i] = -pixel
                enemyXPositions[i] = random.randint(0, width - pixel)

        playerXPosition = playerXPosition - playerXPositionChange

        playing = check_collision()
        if not playing:
            game_iteration += 1
        player(playerXPosition, playerYPosition)
        for i in range(3):
            enemy(enemyXPositions[i], enemyYPositions[i])
        update_bullets()
        draw_bullets()
        show_lives_and_score(width - 150, 10, lives, score)

        pygame.display.update()
    else:
        play_again_message()
        if game_iteration > 0:
            display_score()
        pygame.display.update()
