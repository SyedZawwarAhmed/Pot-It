import pygame
import math

pygame.init()
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()
running = True

pos = (800, 800)
hole_pos = {
    "x": 800,
    "y": 200,
}

class Ball:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (-mx + x, -my + y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((50, 50)).convert_alpha()
        self.bullet.fill((0, 255, 0))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 6

    def update(self):  
        self.pos = (self.pos[0]+self.dir[0]*self.speed, 
                    self.pos[1]+self.dir[1]*self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)  

    def setDirection(self):
        mx, my = pygame.mouse.get_pos()
        self.dir = (-mx + self.pos[0], -my + self.pos[1])
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0]/length, self.dir[1]/length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((50, 50)).convert_alpha()
        self.bullet.fill((0, 255, 0))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 6

isBallMoving = False
shouldSetDirection = False
score = 0
ball = Ball(*pos)
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

    pygame.draw.circle(screen, (0, 0, 0), [hole_pos['x'], hole_pos['y']], 50, 0)
    # pygame.draw.circle(screen, (0, 255, 0), [ball_pos['x'], ball_pos['y']], 50, 0)

    font = pygame.font.SysFont("Arial", 36)
    txtsurf = font.render(f'Score: {score}', True, 'black')
    screen.blit(txtsurf,(200 - txtsurf.get_width() // 2, 150 - txtsurf.get_height() // 2))
 

    # RENDER YOUR GAME HERE
    if isBallMoving:
        print('update')
        ball.update()

    if shouldSetDirection:
        ball.setDirection()

    if not screen.get_rect().collidepoint(ball.pos):
        isBallMoving = False

    ball.draw(screen)
    pygame.display.flip()


    if ball.pos[1] == hole_pos['y']:
        score += 1
        # ball.pos[0] = 800
        # ball.pos[1] = 800

# Draws the surface object to the screen.   
    pygame.display.update()

pygame.quit()