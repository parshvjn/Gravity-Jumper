import pygame, sys
from consts import *
from scripts.tilemap import Tilemap
from scripts.utils import *
from scripts.entities import Player

class Game:
    def __init__(self):
        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.tilemap = Tilemap(self)
        self.display = pygame.Surface((320, 240))
        self.assets = {
            'grass': load_images('tiles/grass'),
            'stone': load_images('tiles/stone'),
            'player/idle': Animation(load_images('entities/player/test/idle'), img_dur = 6),
            'player/attack': Animation(load_images('entities/player/attack', scaleFactor=0.5), img_dur = 3),
            'player/death1': Animation(load_images('entities/player/death1', scaleFactor=0.5), img_dur = 3),
            'player/death2': Animation(load_images('entities/player/death2', scaleFactor=0.5), img_dur = 3),
            'player/death3': Animation(load_images('entities/player/death3', scaleFactor=0.5), img_dur = 3),
            'player/jump': Animation(load_images('entities/player/test/jump')),
            'player/land': Animation(load_images('entities/player/land', scaleFactor=0.5), img_dur = 3, loop = False),
            'player/run': Animation(load_images('entities/player/test/run'), img_dur = 4)
        }

        self.movement = [False, False]
        self.playerTestImg = pygame.image.load("data/images/entities/player/idle/0.png")

        self.player = Player(self, (100, 100), (8,15))

        self.scroll = [0,0]
    
    def main(self):
        self.running = True
        while self.running:
            self.display.fill((14, 219, 248))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0])/30
            self.scroll[1] += (self.player.rect().centery - self.display.get_width() / 2 - self.scroll[1])/30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.tilemap.render(self.display, offset=render_scroll)
            self.player.update(self.tilemap,(self.movement[1]-self.movement[0],0))
            self.player.render(self.display, offset= render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
        
            self.window.blit(pygame.transform.scale(self.display, self.window.get_size()), (0,0))

            pygame.display.update()
            self.clock.tick(60)


if __name__ == '__main__':
    Game().main()
