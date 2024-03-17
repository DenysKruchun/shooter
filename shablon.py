from pygame import*
run = True
WIDTH, HEIGHT = 700,500
FPS = 60
window = display.set_mode((WIDTH,HEIGHT))
display.set_caption("shooter")
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    
    display.update()
    clock.tick(FPS)
