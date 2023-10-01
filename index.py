import pygame
from Hole import Hole
from Ball import Ball
from RetryButton import RetryButton
from levels import obstacles

ball_image = pygame.image.load("assets/ball.png") 
ball_image = pygame.transform.scale(ball_image, (100, 100))
hole_image = pygame.image.load("assets/hole.png") 
hole_image = pygame.transform.scale(hole_image, (100, 100))

pygame.init()
screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

pos = (800, 700)
hole_pos = {
    "x": 800,
    "y": 200,
}


def check_collision(ball_rect, obstacle_rect, collision_tolerance):
    if ball_rect.colliderect(obstacle_rect):
        if abs(obstacle_rect.top - ball_rect.bottom) < collision_tolerance and ball.dir[1] > 0:
            ball.dir[1] *= -1
        if abs(obstacle_rect.bottom - ball_rect.top) < collision_tolerance  and ball.dir[1] < 0:
            ball.dir[1] *= -1
        if abs(obstacle_rect.right - ball_rect.left) < collision_tolerance and ball.dir[0] < 0:
            ball.dir[0] *= -1
        if abs(obstacle_rect.left - ball_rect.right) < collision_tolerance and ball.dir[0] > 0:
            ball.dir[0] *= -1

isBallMoving = False
shouldSetDirection = False
score = 0
ball = Ball(*pos)
obstacle_color = (58.8, 29.4, 0)
level = 1
hole = Hole(800, 200, 60, 60)

obstaclesList = []
max_level = 10
retry_button = RetryButton(screen_width - 150, screen_height - 150, 100, 100, "assets/retry.png")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    clock.tick(60)  
    obstaclesList = obstacles[level - 1]

    mx,my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not retry_button.rect.collidepoint(event.pos):
                isBallMoving = True
                shouldSetDirection = False
        if event.type == pygame.MOUSEBUTTONDOWN:         
            if retry_button.rect.collidepoint(event.pos):
                    # Reset the game when the retry button is clicked
                    ball = Ball(*pos)
                    isBallMoving = False
                    shouldSetDirection = False
            else:
                shouldSetDirection = True


    # fill the screen with a color to wipe away anything from last frame
    screen.fill((105,171,81))

    ball_rect = ball.ball   
    pot_tolerance = 50
    hole_rect = hole.rect
    screen.blit(hole_image, hole.rect)

    screen_rect = screen.get_rect()
    
    if ball_rect.right >= screen_width or ball_rect.left <= 0:
        ball.dir[0] *= -1
    if ball_rect.bottom >= screen_height or ball_rect.top <= 0:
        ball.dir[1] *= -1


    if abs(ball_rect.x - hole_rect.x) < 50 and abs(ball_rect.y - hole_rect.y) < 50:
        isBallMoving = False
        if level != max_level:
            level += 1
            ball = Ball(*pos)
    else:
        screen.blit(ball_image, ball.ball)

    for obstacle in obstaclesList:
        pygame.draw.rect(screen, obstacle_color, obstacle.image)

    font = pygame.font.SysFont("Arial", 36)
    txtsurf = font.render(f'Level: {level}', True, 'black')
    screen.blit(txtsurf,(200 - txtsurf.get_width() // 2, 150 - txtsurf.get_height() // 2))
 
    if isBallMoving:
        if ball.speed > 0:
            ball.update()

    if shouldSetDirection:
        ball.setSpeed()
        ball.setDirection()

    for obstacle in obstaclesList:
        obstacle_rect = obstacle.rect
        check_collision(ball_rect, obstacle_rect, 50)

    if not isBallMoving or ball.speed <= 0:
        retry_button.draw(screen)

        # score += 1

    # if int(ball.pos[1]) == 200 and isBallMoving:
    #     print("Pot")
    #     score += 1
    #     isBallMoving = False
        # ball.pos[0] = 800
        # ball.pos[1] = 800

    # pygame.draw.rect(screen, (0, 255, 0), ball.ball)
    pygame.display.flip()

pygame.quit()