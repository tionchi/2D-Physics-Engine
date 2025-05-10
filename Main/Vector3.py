import numpy as np
import pygame as pg
import sys

pg.init()
font = pg.font.SysFont("Helvetica", 20)
screen=pg.display.set_mode((900,480))
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
    def __init__(self, pos, vel, acel, corestitution):
        if acel is None:
            acel = Vector2(0,9.8)
        else:
            acel.xy[1] += 9.8
        
        input_vectors = {
            "pos": pos,
            "vel": vel,
            "acel": acel
        }
        for attr_name, value in input_vectors.items():
            setattr(self, attr_name, value if value is not None else Vector2())
        self.radius = 30
        self.corestitution = corestitution
        self.draw()

    def draw(self):
        pg.draw.circle(screen, (255,0,0), self.pos.int, self.radius, 0)

    def move(self, dt=1/10):
        self.vel.xy += self.acel.xy * dt
        self.pos.xy += self.vel.xy * dt

        if np.abs(self.vel.xy[1]) < 0.1:
            self.vel.xy[1] = 0
        if np.abs(self.vel.xy[0]) < 0.1:
            self.vel.xy[0] = 0
        
        if np.abs(self.vel.xy[0]) < 0.1 and np.abs(self.vel.xy[1]) < 0.1:
            self.vel.xy = np.array([0,0])


        self.checkCollision()

    def checkCollision(self):
        if self.pos.xy[0] - self.radius < 0:
            self.pos.xy[0] = self.radius
            self.vel.xy[0] = -self.vel.xy[0] 

        if self.pos.xy[0] + self.radius > 640:
            self.pos.xy[0] = 640 - self.radius
            self.vel.xy[0] = -self.vel.xy[0] 

        if self.pos.xy[1] - self.radius < 0:
            self.pos.xy[1] = self.radius
            self.vel.xy[1] = -self.vel.xy[1] * self.corestitution
        
        if self.pos.xy[1] + self.radius > 480:
            self.pos.xy[1] = 480 - self.radius
            self.vel.xy[1] = -self.vel.xy[1] * self.corestitution
            self.vel.xy[0] = self.vel.xy[0] * 0.99

def draw_sidebar(entity):
    pg.draw.rect(screen, (230,230,230), (640, 0, 160, 480))
    pg.draw.line(screen, (0,0,0), (640, 0), (640,480), 2)

    speed = round(entity.vel.magnitude())
    position = [round(float(entity.pos.xy[0])), round(float(entity.pos.xy[1]))]

    info = [
        "Entity Info:",
        f"Speed: {speed}",
        f"position: {position}"
    ]
    for i, line in enumerate(info):
        text = font.render(line, True, (0,0,0))
        screen.blit(text, (650, 20 + i * 25))

#__________________________________
circle = Entity(Vector2(320, 240), Vector2(10,-50), Vector2(0, 9.81), 0.9)
#__________________________________

while True:
    screen.fill((255,255,255))
    circle.draw()
    circle.move()
    draw_sidebar(circle)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
    pg.display.update()
    clock.tick(100)
    


