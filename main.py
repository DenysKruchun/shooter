from pygame import*
from random import randint

init()
font.init()
mixer.init()
mixer.music.load('musictheme.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
fire_sound = mixer.Sound("laser.wav")
fire_sound.set_volume(0.3)
run = True
WIDTH, HEIGHT = 900,700
FPS = 60

record = 0
with open("record.txt", "r") as file:
    record = int(file.read())
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
        self.mask = mask.from_surface(self.image)

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
        
    def fire(self):
        new_fire = Bullet(fire_image, self.rect.centerx, self.rect.top, 20,60,5)
        fire_sound.play()



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

class Bullet(Sprite):
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed) -> None:
        super().__init__(sprite_image, x, y, sprite_width, sprite_height, sprite_speed)
        self.rect.centerx = x
        self.rect.bottom = y
        bullets.add(self)
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
                
def start_game():
    global monsters,player,bullets,label,hp_label,points_label,finish
    player = Player(player_image,400,500,100,70,5)
    monsters = sprite.Group()
    bullets = sprite.Group()
    label = font1.render("Lost: "+ str(player.lost),1,(255,255,255))
    hp_label =  font1.render("Hp: "+ str(player.hp),1,(255,255,255))
    points_label =  font1.render("Points: "+ str(player.points),1,(255,255,255))
    finish = False

def save_record():
    with open("record.txt", "w") as file:
        file.write(str(record))

spawn_time = time.get_ticks()
interval_spawn = randint(1000,5000)
font1 = font.SysFont("Arial",35)
font2 = font.SysFont("Arial",100)

start_game()
hint_text = font1.render("Press any button to start ",1,(255,255,255))
finish_text = font1.render("Press 'R' button to start ",1,(255,255,255))

lose_game = font2.render("Game over!",1,(255,255,255))
start = False
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type  == KEYDOWN:
            start = True
            if e.key == K_SPACE:
                player.fire()
            if e.key == K_r and finish == True:
                start_game()

    if not finish and start:

        now = time.get_ticks()
        if now - spawn_time > interval_spawn:
            Enemy(alien_image,70,70,7)
            spawn_time = time.get_ticks()
            interval_spawn = randint(1000,5000)

        colides_hits  = sprite.spritecollide(player,monsters,True,sprite.collide_mask)     
        if colides_hits:
            player.hp -= 30
            if player.hp <= 0:
                player.hp = 0
                finish = True
                if player.points > record:
                    record = player.points
                    save_record()
            hp_label =  font1.render("Hp: "+ str(player.hp),1,(255,255,255))

        if player.lost > 5:
            finish = True


        sprites_list = sprite.groupcollide(monsters,bullets,True,True, sprite.collide_mask)
        for hit in sprites_list:
            player.points += 10
            points_label =  font1.render("Points: "+ str(player.points),1,(255,255,255))

        player.update()
        monsters.update()
        bullets.update()


    window.blit(background,(0,0))
    player.draw(window)
   
    monsters.draw(window)
    bullets.draw(window)
    window.blit(label,(20,20))
    window.blit(hp_label,(20,60))
    window.blit(points_label,(WIDTH - 150,20))
    if finish == True:
        window.blit(lose_game,(220,300))
        window.blit(finish_text,(300,450))

    if start == False:
        window.blit(hint_text,(300,300))
    display.update()
    clock.tick(FPS)