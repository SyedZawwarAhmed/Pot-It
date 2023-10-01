import pygame
import math

pygame.init()
screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
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
        # Create a surface for the obstacle
        self.image = pygame.Rect(x, y, 100, 400)
        # self.image.fill(color)

        # Get the Rect object for the obstacle and set its position
        self.rect = self.image
        self.rect.x = x
        self.rect.y = y

class Hole:
    def __init__(self, x, y, width, height):
        # Create a surface for the obstacle
        self.image = pygame.Rect(x, y, width, height)
        # self.image.fill(color)

        # Get the Rect object for the obstacle and set its position
        self.rect = self.image
        self.rect.x = x
        self.rect.y = y


class Ball():
    max_speed = 30
    circle_radius = 50  # Adjust the radius as needed

    def __init__(self, x, y):
        self.pos = (x, y)
        self.speed = 0
        mx, my = pygame.mouse.get_pos()
        self.dir = [-mx + x, -my + y]
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = [0, -1]
        else:
            self.dir = [self.dir[0]/length, self.dir[1]/length]

        # self.ball = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2), pygame.SRCALPHA)
        # pygame.draw.circle(self.ball, (0, 255, 0), (self.circle_radius, self.circle_radius), self.circle_radius)
        
        # self.rect = self.ball.get_rect(center=self.pos)

        self.ball = pygame.Rect(self.pos[0], self.pos[1], 50, 50)

    def update(self):  
        self.pos = (self.pos[0] + self.dir[0] * self.speed, self.pos[1] + self.dir[1] * self.speed)
        self.speed -= 0.08
        self.ball = pygame.Rect(self.pos[0], self.pos[1], 50, 50)


    def setDirection(self):
        print("Hello world")
        mx, my = pygame.mouse.get_pos()
        self.dir = [-mx + self.pos[0], -my + self.pos[1]]
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = [0, -1]
        else:
            self.dir = [self.dir[0]/length, self.dir[1]/length]

        # self.ball = pygame.Surface((self.circle_radius * 2, self.circle_radius * 2), pygame.SRCALPHA)
        # pygame.draw.circle(self.ball, (0, 255, 0), (self.circle_radius, self.circle_radius), self.circle_radius)
        # self.rect = self.ball.get_rect(center=self.pos)
        self.ball = pygame.Rect(self.pos[0], self.pos[1], 50, 50)

    # def draw(self):
    #     self.ball = pygame.Rect(self.pos[0], self.pos[1], 50, 50)

    
    def setSpeed(self):
        mx, my = pygame.mouse.get_pos()
        calculated_speed = math.sqrt((mx-self.pos[0])**2 + (my-self.pos[1])**2) / 10
        if calculated_speed > self.max_speed:
            self.speed = self.max_speed
        else:
            self.speed = calculated_speed

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
obstacle = Obstacle(300, 200, 100, 100, (58.8, 29.4, 0))  # (x, y, width, height, color)
hole = Hole(800, 200, 60, 60)
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

    pygame.draw.rect(screen, (58.8, 29.4, 0), obstacle.image)
    pygame.draw.rect(screen, (0,0,0), hole.image)

    font = pygame.font.SysFont("Arial", 36)
    txtsurf = font.render(f'Score: {score}', True, 'black')
    screen.blit(txtsurf,(200 - txtsurf.get_width() // 2, 150 - txtsurf.get_height() // 2))
 
    if isBallMoving:
        if ball.speed > 0:
            ball.update()

    if shouldSetDirection:
        ball.setSpeed()
        ball.setDirection()

    # if not screen.get_rect().collidepoint(ball.pos):
    screen_rect = screen.get_rect()
    ball_rect = ball.ball
    if ball_rect.right >= screen_width or ball_rect.left <= 0:
        ball.dir[0] *= -1
    if ball_rect.bottom >= screen_height or ball_rect.top <= 0:
        ball.dir[1] *= -1

    obstacle_rect = obstacle.rect
    check_collision(ball_rect, obstacle_rect, 25)

    pot_tolerance = 50
    hole_rect = hole.rect
    if ball_rect.collidepoint(hole_rect.center):
        isBallMoving = False
        # score += 1

    # if int(ball.pos[1]) == 200 and isBallMoving:
    #     print("Pot")
    #     score += 1
    #     isBallMoving = False
        # ball.pos[0] = 800
        # ball.pos[1] = 800

    pygame.draw.rect(screen, (0, 255, 0), ball.ball)
    pygame.display.flip()

pygame.quit()