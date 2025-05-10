import numpy as np
import pygame as pg
import sys





SCREEN_WIDTH = 900
SCREEN_HEIGHT = 480
SIMULATOR_WIDTH = 640

pg.init()
font = pg.font.SysFont("Helvetica", 20)
screen=pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pg.display.set_caption("Physics Engine")
clock = pg.time.Clock()

class Vector2():
    def __init__(self, x=0, y=0):
        self.xy = np.array([x, y], dtype=float)

    def __repr__(self):
        return f"({self.xy[0]},{self.xy[1]})"

    def dotP(self, other):
        return np.dot(self.xy, other.xy)
    
    def magnitude(self):
        return np.sqrt((self.xy[0] ** 2 ) + (self.xy[1] ** 2))
    
    @property
    def int(self):
        return tuple(self.xy.round().astype(int))

class Entity():
    def __init__(self, pos, vel, acel, corestitution, name):
        if acel is None:
            acel = Vector2(0,-9.81)
        else:
            acel.xy[1] -= 9.81
        self.pos = pos if pos is not None else Vector2()
        self.vel = vel if vel is not None else Vector2()
        self.acel = acel
        self.radius = 30
        self.name = name
        self.corestitution = corestitution
        self.draw()

    def draw(self):
        flippedY = SCREEN_HEIGHT - self.pos.xy[1]
        pg.draw.circle(screen, (255,0,0),( int(self.pos.xy[0]), int(flippedY)), self.radius, 0)

    def move(self, dt=1/10):
        self.vel.xy += self.acel.xy * dt
        
        if np.abs(self.vel.xy[0]) < 1 and np.abs(self.vel.xy[1]) < 1:
            self.vel.xy = np.array([0.0,0.0])
        else:
            self.pos.xy += self.vel.xy * dt


        self.checkCollision()

    def checkCollision(self):
        if self.pos.xy[0] - self.radius < 0:
            self.pos.xy[0] = self.radius
            self.vel.xy[0] = -self.vel.xy[0] * self.corestitution

        if self.pos.xy[0] + self.radius > SIMULATOR_WIDTH:
            self.pos.xy[0] = SIMULATOR_WIDTH - self.radius
            self.vel.xy[0] = -self.vel.xy[0] * self.corestitution

        if self.pos.xy[1] - self.radius < 0:
            self.pos.xy[1] = self.radius
            self.vel.xy[1] = -self.vel.xy[1] * self.corestitution
            self.vel.xy[0] = self.vel.xy[0] - 0.1
        
        if self.pos.xy[1] + self.radius > SCREEN_HEIGHT:
            self.pos.xy[1] = SCREEN_HEIGHT - self.radius
            self.vel.xy[1] = -self.vel.xy[1] * self.corestitution
            

def draw_sidebar(entites):
    pg.draw.rect(screen, (230,230,230), (SIMULATOR_WIDTH, 0, SCREEN_WIDTH - SIMULATOR_WIDTH, SCREEN_HEIGHT))
    pg.draw.line(screen, (0,0,0), (SIMULATOR_WIDTH, 0), (SIMULATOR_WIDTH,SCREEN_HEIGHT), 2)

    yOff = 20

    for entity in entites:
        speed = entity.vel.magnitude()
        conversionFactor = 0.1
        dt = 1/10
        speedMS = speed * conversionFactor / dt
        
        if speedMS < 1:
            speedMS = 0.0
        else:
            speedMS = round(speedMS)
        
        position = [round(float(entity.pos.xy[0])), round(float(entity.pos.xy[1] - entity.radius))]

        info = [
            f"Ball {entity.name} Info:",
            f"Speed: {speedMS} m/s",
            f"position: {position}"
        ]
        for i, line in enumerate(info):
            text = font.render(line, True, (0,0,0))
            screen.blit(text, (SIMULATOR_WIDTH+10, yOff))
            yOff += 25
        yOff +=20
            
#__________________________________
entites = [Entity(Vector2(320, 250), Vector2(200,0), Vector2(0, 0), 0.6, 1),
           Entity(Vector2(250, 320), Vector2(10,0), Vector2(0, 0), 0.6, 2),
           Entity(Vector2(100, 300), Vector2(50,0), Vector2(0, 0), 0.6, 3),
           Entity(Vector2(450, 480), Vector2(400,0), Vector2(0, 0), 0.6, 4)]
#__________________________________

while True:
    screen.fill((255,255,255))

    for entity in entites:
        entity.draw()
        entity.move()

    draw_sidebar(entites)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
    clock.tick(100)
    


