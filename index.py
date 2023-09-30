import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
running = True
circle_radius= 50

pos = (800, 700)
hole_pos = {
    "x": 800,
    "y": 200,
}

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        # Create a surface for the obstacle
        self.image = pygame.Surface((width, height))
        self.image.fill(color)

        # Get the Rect object for the obstacle and set its position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


import pygame
import math

class Ball():
    max_speed = 20
    circle_radius = 50  # Adjust the radius as needed

    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = [-mx + x, -my + y]
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = [0, -1]
        else:
            self.dir = [self.dir[0]/length, self.dir[1]/length]
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.ball = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.ball, (0, 255, 0), (self.circle_radius, self.circle_radius), self.circle_radius)
        self.ball = pygame.transform.rotate(self.ball, angle)
        self.speed = 6
        self.rect = self.ball.get_rect()

    def update(self):  
        self.pos = (self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed)
        self.speed -= 0.08

    def draw(self, surf):
        ball_rect = self.ball.get_rect(center=self.pos)
        surf.blit(self.ball, (ball_rect.x, ball_rect.y))

    def setDirection(self):
        mx, my = pygame.mouse.get_pos()
        self.dir = [-mx + self.pos[0], -my + self.pos[1]]
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = [0, -1]
        else:
            self.dir = [self.dir[0]/length, self.dir[1]/length]
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.ball = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.ball, (0, 255, 0), (self.circle_radius, self.circle_radius), self.circle_radius)
        self.ball = pygame.transform.rotate(self.ball, angle)
        self.rect = self.ball.get_rect()
    
    def setSpeed(self):
        calculated_speed = math.sqrt((mx-self.pos[0])**2 + (my-self.pos[1])**2) / 10
        if calculated_speed > self.max_speed:
            self.speed = self.max_speed
        else:
            self.speed = calculated_speed

isBallMoving = False
shouldSetDirection = False
score = 0
ball = Ball(*pos)
obstacle = Obstacle(300, 200, 100, 100, (0, 0, 255))  # (x, y, width, height, color)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    clock.tick(60)  
    mx,my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            isBallMoving = True
            shouldSetDirection = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shouldSetDirection = True


    # fill the screen with a color to wipe away anything from last frame
    screen.fill("lightgrey")

    pygame.draw.circle(screen, (0, 0, 0), [hole_pos['x'], hole_pos['y']], 30, 0)

    
    screen.blit(obstacle.image, obstacle.rect)

    font = pygame.font.SysFont("Arial", 36)
    txtsurf = font.render(f'Score: {score}', True, 'black')
    screen.blit(txtsurf,(200 - txtsurf.get_width() // 2, 150 - txtsurf.get_height() // 2))
 

    # RENDER YOUR GAME HERE
    if isBallMoving:
        if ball.speed > 0:
            ball.update()

    if shouldSetDirection:
        ball.setDirection()
        ball.setSpeed()

    # if not screen.get_rect().collidepoint(ball.pos):
    screen_rect = screen.get_rect()
    if ball.pos[0] < screen_rect.left or ball.pos[0] > screen_rect.right:
        ball.dir[0] *= -1
    if ball.pos[1] < screen_rect.top or ball.pos[1] > screen_rect.bottom:
        ball.dir[1] *= -1

    obstacle_rect = obstacle.rect
    if ball.pos[0] <= obstacle_rect.right and ball.pos[1] <= obstacle_rect.bottom:
        ball.dir[0] *= -1
    # if pygame.Rect.colliderect(obstacle_rect, ball.rect):
    #     isBallMoving = False
    # if ball.pos[0] < screen_rect.left or ball.pos[0] > screen_rect.right:
    #     ball.dir[0] *= -1
    # if ball.pos[1] < screen_rect.top or ball.pos[1] > screen_rect.bottom:
    #     ball.dir[1] *= -1
        
    ball.draw(screen)

    if int(ball.pos[1]) == 200 and isBallMoving:
        print("Pot")
        score += 1
        isBallMoving = False
        # ball.pos[0] = 800
        # ball.pos[1] = 800

    pygame.display.flip()
# Draws the surface object to the screen.   
    # pygame.display.update()

pygame.quit()