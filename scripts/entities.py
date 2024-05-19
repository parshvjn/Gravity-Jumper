import pygame
class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0,0]
        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False}

        #animation
        self.action = ''
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')

        self.last_movement = [0,0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action: 
            self.action = action
            self.animation = self.game.assets[self.type + '/' + self.action].copy()


    def update(self, tilemap,movement =(0, 0)):

        self.collisions = {'up': False, 'down': False, 'left': False, 'right': False} 

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1]) 

        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0: #if moving right
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x 

        self.pos[1] += frame_movement[1] 
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y
        
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(5, self.velocity[1]+0.1)


        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset =(0,0)):
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), (self.pos[0] - offset[0] + self.anim_offset[0], self.pos[1] - offset[1] + self.anim_offset[1]))


class Player(PhysicsEntity): #inheriting from PhysicsEntity
    def __init__(self, game, pos, size): # we are seperating this part from the above class and putting in another because the animation logic is diff from other entities
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 3
        self.jumpNum = self.jumps
    
    def update(self, tilemap, movement = (0,0)):
        super().update(tilemap, movement = movement)

        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0: 
            self.set_action('run')
        else:
            self.set_action('idle')

        if self.collisions['down']: # if on ground
            self.air_time = 0
            self.jumps = self.jumpNum
        print(self.air_time)
    def render(self, surf, offset =(0,0)):
        super().render(surf, offset = offset)

    def jump(self):
        if self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
    