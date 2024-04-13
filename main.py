from pygame import *
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
WIDTH, HEIGHT = 900, 700
FPS = 60

try:
    with open("record.txt", "r") as file:
        record = int(file.read())
except:
    record = 0

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("shooter")
clock = time.Clock()

background = image.load("infinite_starts.jpg")
background = transform.scale(background, (WIDTH, HEIGHT))
bg_y = 0
player_image = image.load("spaceship.png")
alien_image = image.load("alien.png")
fire_image = image.load("fire.png")
asteroid_image = image.load("asteroid.png")


class Sprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed) -> None:
        super().__init__()
        self.image = transform.scale(
            sprite_image, (sprite_width, sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = sprite_speed
        self.mask = mask.from_surface(self.image)

    def draw(self, window):
        window.blit(self.image, self.rect)


class Player(Sprite):
    def __init__(self, sprite_image, x, y, sprite_width, sprite_height, sprite_speed):
        super().__init__(sprite_image, x, y, sprite_width, sprite_height, sprite_speed)
        self.hp = 100
        self.points = 0
        self.lost = 0
        self.bullets = 5
        self.bullets_timer = None

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
        if self.bullets > 0:
            new_fire = Bullet(fire_image, self.rect.centerx,
                              self.rect.top, 20, 60, 5)
            fire_sound.play()
            self.bullets -= 1
            if self.bullets <= 0:
                self.bullets_timer = time.get_ticks()


class Enemy(Sprite):
    def __init__(self, sprite_image, sprite_width, sprite_height, sprite_speed):
        rand_x = randint(0, WIDTH-70)
        super().__init__(sprite_image, rand_x, -100,
                         sprite_width, sprite_height, sprite_speed)

        monsters.add(self)

    def update(self):
        global label
        self.rect.y += self.speed

        if self.rect.y > HEIGHT:
            player.lost += 1
            label = font1.render(
                "Lost: " + str(player.lost), 1, (255, 255, 255))

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


class Asteroid(Sprite):
    def __init__(self, sprite_image, sprite_width, sprite_height, sprite_speed) -> None:
        rand_x = randint(0, WIDTH - 70)
        super().__init__(sprite_image, rand_x, -100,
                         sprite_width, sprite_height, sprite_speed)

        asteroids.add(self)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT:
            self.kill()


def start_game():
    global monsters, player, bullets, asteroids, label, hp_label, points_label, finish, bullets_label
    player = Player(player_image, 400, 500, 100, 70, 5)
    monsters = sprite.Group()
    bullets = sprite.Group()
    asteroids = sprite.Group()
    label = font1.render("Lost: " + str(player.lost), 1, (255, 255, 255))
    hp_label = font1.render("Hp: " + str(player.hp), 1, (255, 255, 255))
    points_label = font1.render(
        "Points: " + str(player.points), 1, (255, 255, 255))
    bullets_label = font1.render(
        "Bullets:" + str(player.bullets), 1, (255, 255, 255))
    finish = False


def save_record():
    with open("record.txt", "w") as file:
        file.write(str(record))


spawn_time = time.get_ticks()
interval_spawn = randint(1000, 5000)
asteroid_spawn_time = time.get_ticks()
asteroid_spawn_interval = randint(3000, 7000)
font1 = font.Font("SpaceMono-Regular.ttf", 25)
font2 = font.Font("SpaceMono-Regular.ttf", 80)

start_game()
hint_text = font1.render("Press any button to start ", 1, (255, 255, 255))
finish_text = font1.render("Press 'R' button to start ", 1, (255, 255, 255))
reload_text = font1.render("Reloading", 1, (255, 247, 128))
record_text = font1.render("Record: " + str(record), 1, (255, 247, 128))
lose_game = font2.render("Game over!", 1, (255, 255, 255))
start = False
finish = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            start = True
            if e.key == K_SPACE and not finish:
                player.fire()
                bullets_label = font1.render(
                    "Bullets:" + str(player.bullets), 1, (255, 255, 255))
            if e.key == K_r and finish == True:
                start_game()

    if not finish and start:
        bg_y += 1
        if bg_y > HEIGHT:
            bg_y = 0

        now = time.get_ticks()
        if now - spawn_time > interval_spawn:
            Enemy(alien_image, 70, 70, 7)
            spawn_time = time.get_ticks()
            interval_spawn = randint(1000, 5000)

        if now - asteroid_spawn_time > asteroid_spawn_interval:
            Asteroid(asteroid_image, 100, 100, 6)
            asteroid_spawn_time = time.get_ticks()
            asteroid_spawn_interval = randint(3000, 7000)

        colides_hits = sprite.spritecollide(
            player, monsters, True, sprite.collide_mask)
        if colides_hits:
            player.hp -= 30
            hp_label = font1.render(
                "Hp: " + str(player.hp), 1, (255, 255, 255))

        if player.lost > 5:
            finish = True

        colides_hits_2 = sprite.spritecollide(
            player, asteroids, True, sprite.collide_mask)
        if colides_hits_2:
            player.hp -= 50
            hp_label = font1.render(
                "Hp: " + str(player.hp), 1, (255, 255, 255))

        sprites_list_2 = sprite.groupcollide(
            asteroids, bullets, False, True, sprite.collide_mask)

        sprites_list = sprite.groupcollide(
            monsters, bullets, True, True, sprite.collide_mask)
        for hit in sprites_list:
            player.points += 10
            points_label = font1.render(
                "Points: " + str(player.points), 1, (255, 255, 255))

        sprites_list_2 = sprite.groupcollide(
            asteroids, monsters, False, True, sprite.collide_mask)

        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        if player.hp <= 0 and not finish:
            player.hp = 0
            hp_label = font1.render(
                "Hp: " + str(player.hp), 1, (255, 255, 255))
            finish = True
            if player.points > record:
                record = player.points
                record_text = font1.render(
                    "Record: " + str(record), 1, (255, 247, 128))
                save_record()

    window.blit(background, (0, bg_y))
    window.blit(background, (0, bg_y - HEIGHT))
    
    player.draw(window)

    monsters.draw(window)
    bullets.draw(window)
    asteroids.draw(window)

    window.blit(label, (20, 20))
    window.blit(hp_label, (20, 60))
    window.blit(points_label, (WIDTH - 150, 20))
    window.blit(bullets_label, (WIDTH - 150, 60))

    if player.bullets <= 0 and not finish:
        window.blit(reload_text, (WIDTH/2 - 50, 20))
        if now - player.bullets_timer >= 5000:
            player.bullets = 5
            bullets_label = font1.render(
                "Bullets:" + str(player.bullets), 1, (255, 255, 255))

    if finish == True:
        window.blit(lose_game, (220, 300))
        window.blit(finish_text, (300, 450))
        window.blit(record_text, (WIDTH/2 - 50, 20))

    if start == False:
        window.blit(hint_text, (300, 300))
        window.blit(record_text, (WIDTH/2 - 50, 20))
    display.update()
    clock.tick(FPS)
