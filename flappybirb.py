import pygame, random, time
from pygame.locals import *
from time import sleep

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
GAME_SPEED = 10

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

white = (255, 255, 255)
count = 0

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets/bluebird-upflap.png').convert_alpha(),
                       pygame.image.load('assets/bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('assets/bluebird-downflap.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0

        self.image = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[ self.current_image ]

        self.speed += GRAVITY

        # Update height
        self.rect[1] += self.speed
    
    def bump(self):
        self.speed = -SPEED

class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/pipe-red.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH,PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED

class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
    
    def update(self):
        self.rect[0] -= GAME_SPEED

def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


def placar(count):
    font = pygame.font.SysFont("perpetua", 20)
    text = font.render("Desvios: "+str(count), True, white)
    screen.blit(text, (10, 20))


def log(email, count):
    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        banco_de_dados = open("Pontuações.txt","a")
        banco_de_dados.write("E_mail do jogador: ")
        banco_de_dados.write(email)
        banco_de_dados.write(" |Pontuação: ")
        banco_de_dados.write(str(count))
        banco_de_dados.write("\n")


email = input("E-mail: ")
print("PARA JOGAR BASTA CLICAR EM 'SPACE' ")

print('O JOGO VAI COMEÇAR EM...')
sleep(1)
print('3...')
sleep(1)
print('2...')
sleep(1)
print('1...')
sleep(1)
print('GO !!!')
sleep(0.5)
    

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


BACKGROUND = pygame.image.load('assets/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
base_font = pygame.font.Font(None, 32)


wing_sound = pygame.mixer.Sound('assets/wing.wav')
die_sound = pygame.mixer.Sound('assets/die.wav')
point_sound = pygame.mixer.Sound('assets/point.wav')


bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])


clock = pygame.time.Clock()

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            
        if event.type == KEYDOWN:
            if event.key == K_SPACE:         
                bird.bump()
                wing_sound.play() 

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])

        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        count += 1
        point_sound.play()
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)
    placar(count)

    pygame.display.update()


    if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
        die_sound.play()
        try:
            log(email, count)
        except:
            banco_de_dados = open("Pontuações.txt","x")
            log(email, count)
        # Game over
        sleep(1)
        break