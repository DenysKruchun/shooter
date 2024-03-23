from pygame import*
from random import randint

init()
font.init()
run = True
WIDTH, HEIGHT = 900,700
FPS = 60
window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("shooter")
clock = time.Clock()

background = image.load("infinite_starts.jpg")
background = transform.scale(background,(WIDTH ,HEIGHT  ))
player_image =image.load("spaceship.png")
alien_image = image.load("alien.png")
fire_image = image.load("fire.png")

class Sprite(sprite.Sprite):
    def __init__(self, sprite_image,x,y,sprite_width,sprite_height,sprite_speed) -> None:
        super().__init__()
        self.image = transform.scale(sprite_image, (sprite_width,sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = sprite_speed

    def draw(self,window):
        window.blit(self.image,self.rect)

class Player(Sprite):
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed):
        super().__init__(sprite_image, x, y, sprite_width, sprite_height, sprite_speed)
        self.hp = 100
        self.points = 0
        self.lost = 0
    
    def update(self):
        keyes = key.get_pressed()
        if keyes[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keyes[K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keyes[K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
        if keyes[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

class Enemy(Sprite):
    def __init__(self, sprite_image, sprite_width, sprite_height, sprite_speed):
        rand_x = randint(0,WIDTH-70)
        super().__init__(sprite_image, rand_x, -100, sprite_width, sprite_height, sprite_speed)
        
        monsters.add(self)
    
    def update(self):
        global label
        self.rect.y += self.speed
    
        if self.rect.y > HEIGHT:
            player.lost += 1
            label = font1.render("Lost: "+ str(player.lost),1,(255,255,255))

            self.kill()                                                                       

player = Player(player_image,400,500,100,70,5)
monsters = sprite.Group()
Enemy(alien_image,70,70,7)
spawn_time = time.get_ticks()

interval_spawn = randint(1000,5000)
font1 = font.SysFont("Arial",35)
font2 = font.SysFont("Arial",100)
label = font1.render("Lost: "+ str(player.lost),1,(255,255,255))
hp_label =  font1.render("Hp: "+ str(player.hp),1,(255,255,255))
lose_game = font2.render("Game over!",1,(255,255,255))

finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:

        now = time.get_ticks()
        if now - spawn_time > interval_spawn:
            Enemy(alien_image,70,70,7)
            spawn_time = time.get_ticks()
            interval_spawn = randint(1000,5000)

        colides_hits  = sprite.spritecollide(player,monsters,True)     
        if colides_hits:
            player.hp -= 30
            hp_label =  font1.render("Hp: "+ str(player.hp),1,(255,255,255))
            if player.hp <= 0:
                finish = True
        player.update()
        monsters.update()


    window.blit(background,(0,0))
    player.draw(window)
   
    monsters.draw(window)
    window.blit(label,(20,20))
    window.blit(hp_label,(20,60))
    if finish == True:
        window.blit(lose_game,(220,300))
    display.update()
    clock.tick(FPS)