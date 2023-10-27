import pygame as pg

pg.init()

monitor = pg.display.Info()
monitor_res = (monitor.current_w, monitor.current_h)
screen = pg.display.set_mode(monitor_res, pg.FULLSCREEN)

clock = pg.time.Clock()

defender = pg.image.load("images/defender.png")
defender_pos = pg.Vector2(monitor_res[0] // 2, monitor_res[1] // 2)
defender_speed = 5

atacker = pg.image.load("images/atacker.png")
atacker_pos = pg.Vector2(monitor_res[0] // 2, monitor_res[1] // 2)
atacker_speed = 5

moment = 0
count = 0


wood_barriers = []
concrete_barriers = []
metal_barriers = []

class Barrier:
    def __init__(self, x, y):
        self.pos = pg.Vector2(x + 32, y + 32)

class Wood_Barrier(Barrier):

    def __init__(self, x, y):
        Barrier.__init__(self, x, y)
        self.img = pg.image.load("images/wood.png")
        self.hp = 1

    def hit(dmg):
        self.hp -= dmg

'''
class Concrete_Barrier(Barrier):

    def __init__(self, x, y):
        Barrier.__init__(x,y)
        self.img = pg.image.load("images/concrete.png")
        self.hp = 1

    def hit(dmg):
        self.hp -= dmg


class Metal_Barrier(Barrier):

    def __init__(self, x, y):
        Barrier.__init__(x,y)
        self.img = pg.image.load("images/metal.png")
        self.hp = 1

    def hit(dmg):
        self.hp -= dmg
'''

running = True

while running:

    if moment == 0:

        if count >= 3600:
            moment = 1
            
        screen.fill("green")

        screen.blit(defender, defender_pos)
        
        for each in wood_barriers:
            screen.blit(each.img, each.pos)

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            defender_pos.y -= defender_speed
        if keys[pg.K_s]:
            defender_pos.y += defender_speed
        if keys[pg.K_a]:
            defender_pos.x -= defender_speed
        if keys[pg.K_d]:
            defender_pos.x += defender_speed

        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False
                if event.key == pg.K_SPACE:
                    if len(wood_barriers) < 10:
                        wood_barriers += [Wood_Barrier(defender_pos.x - 96, defender_pos.y - 32)]

    if moment == 1:

        screen.fill("green")

        screen.blit(defender, defender_pos)
        screen.blit(atacker, atacker_pos)

        for each in wood_barriers:
            screen.blit(each.img, each.pos)
        

        for event in pg.event.get():

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    running = False

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            defender_pos.y -= defender_speed
        if keys[pg.K_s]:
            defender_pos.y += defender_speed
        if keys[pg.K_a]:
            defender_pos.x -= defender_speed
        if keys[pg.K_d]:
            defender_pos.x += defender_speed
        if keys[pg.K_UP]:
            atacker_pos.y -= atacker_speed
        if keys[pg.K_DOWN]:
            atacker_pos.y += atacker_speed
        if keys[pg.K_LEFT]:
            atacker_pos.x -= atacker_speed
        if keys[pg.K_RIGHT]:
            atacker_pos.x += atacker_speed
    




    pg.display.flip()

    count += 1
    clock.tick(60)

pg.quit()
