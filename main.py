from pygame import*

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

player = Player(player_image,400,500,100,70,5)




while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    window.blit(background,(0,0))
    player.draw(window)
    player.update()
    display.update()
    clock.tick(FPS)
