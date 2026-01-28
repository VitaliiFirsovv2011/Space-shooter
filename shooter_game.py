from pygame import *
from random import *
from time import time as timer

class GameSprite(sprite.Sprite):
    def __init__(self, image_file, x, y, speed, size_x, size_y):
        super().__init__()  
        self.image = transform.scale(
            image.load(image_file), (size_x, size_y)
        )  
        self.speed = speed  
        self.rect = (
            self.image.get_rect()
        )  
        self.rect.x = x
        self.rect.y = y

    def reset(self):

        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update1(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys[K_RIGHT] and self.rect.x < width -70:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(image_bullet, self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = -50
            lost += 1

class Asteroids(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= height:
            self.rect.x = randint(80, width - 80)
            self.rect.y = 0


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

width = 700
height = 500

image_back = 'galaxy.jpg'
image_hero = 'rocket.png'
image_enemy  = 'ufo.png'
image_bullet = "bullet.png"
image_asteroid = "asteroid.png"
image_heart = 'heart.png'

window = display.set_mode((width, height))
display.set_caption('Космический шутер')

background = transform.scale(image.load(image_back), (width, height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
fire_sound = mixer.Sound("fire.ogg")

clock = time.Clock()
FPS = 60

ship = Player(image_hero, 5, 400, 10, 80, 100)

monsters = sprite.Group()
bullets = sprite.Group()
asteroids1 = sprite.Group()

for i in range(5):
    monster = Enemy(image_enemy, randint(0, width- 80), -40, randint(1,4),80, 50)
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroids(image_asteroid, randint(0, width - 50), -40, randint(1, 4), 50, 50)
    asteroids1.add(asteroid)


lost = 0
score = 0
max_score = 10
max_lost = 3
max_bullets = 10 
num_bullet = 0 
num_fire = 0 

font.init()
font1 = font.SysFont('Arial', 36)
font2  = font.SysFont('Arial', 80)
lose = font2.render('YOU LOSE!', True, (255, 0 ,0 ))
win = font2.render("YOU WIN!", True, (0, 255, 0))

game = True
reload_bullets = False
finish = False

lives = 5
heart = transform.scale(image.load(image_heart), (40, 40))
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_bullet < max_bullets and reload_bullets == False:
                    fire_sound.play() 
                    ship.fire()
                    num_bullet += 1  # увеличиваем количество пуль
                if num_bullet >= max_bullets and reload_bullets == False:
                    last_time = timer()
                    reload_bullets = True
  
    if finish != True:
    
        window.blit(background, (0, 0))

        ship.reset()
        ship.update1()
        
        text = font1.render('Счёт:' + str(score), True,(255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font1.render('Пропущено:' + str(lost), True, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        monsters.draw(window)
        monsters.update()

        asteroids1.draw(window)
        asteroids1.update()

        bullets.draw(window)
        bullets.update()

        if reload_bullets:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font2.render("Wait, reload...", True, (150, 0, 0))
                window.blit(reload_text, (200, 400))
            else:
                num_bullet = 0
                reload_bullets = False

        if sprite.spritecollide(ship, monsters, True):
            lives -= 1
            monster = Enemy(image_enemy , randint(0, width- 80), -40, randint(1,4),80, 50)
            monsters.add(monster)
        
        if sprite.spritecollide(ship, asteroids1, True):
            lives -= 1
            asteroid = Enemy(image_asteroid , randint(0, width- 80), -40, randint(1,4),80, 50)
            asteroids1.add(asteroid)

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1 
            monster = Enemy(
                image_enemy, randint(0, width - 80), -40, randint(1, 4), 80, 50
            )
            monsters.add(monster) 

        if lives == 0 or lost >= max_lost:
            finish = True  
            window.blit(lose, (200, 200))  
        
        if score >= max_score:
            finish = True
            window.blit(win, (200, 200))

        x = 650
        for i in range(lives):
            window.blit(heart, (x, 10))
            x -= 45

    display.update()
    clock.tick(FPS)

