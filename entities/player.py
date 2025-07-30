import pygame
from entities.carro import Carro
from entities.rocket import Rocket


class Player(Carro):
    def __init__(self, image, screen_width, screen_height, x_pos, y_pos):
        super().__init__(image, x_pos, y_pos)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed = 3
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_consumption_rate = 0.05
        self.left_limit = 100
        self.right_limit = self.screen_width - 100 - self.rect.width
        
        # Rocket attributes
        self.has_rocket = False
        self.rockets = []
        self.rocket_cooldown = 0
        self.rocket_icon_pos = (10, 50)  # Posição do ícone na HUD


        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def update(self, keys):
        # Verificação de estado frozen
        if not hasattr(self, 'frozen'):
            self.frozen = False
        if self.frozen:
            return
        
        # Controle de movimento (mantido igual)
        if self.fuel > 0:
            if keys[pygame.K_LEFT] and self.rect.x > self.left_limit:
                self.rect.x -= self.speed
            if keys[pygame.K_RIGHT] and self.rect.x < self.right_limit:
                self.rect.x += self.speed
            if keys[pygame.K_UP] and self.rect.y > 0:
                self.rect.y -= self.speed
            if keys[pygame.K_DOWN] and self.rect.y < self.screen_height - self.rect.height:
                self.rect.y += self.speed

            self.hitbox.set_rect(
                self.rect.width, self.rect.height, self.rect.x, self.rect.y)

            self.fuel -= self.fuel_consumption_rate
            if self.fuel < 0:
                self.fuel = 0
        
        # Sistema de disparo da bazuca (novo)
        current_time = pygame.time.get_ticks()
        if (self.has_rocket and 
            keys[pygame.K_SPACE] and 
            current_time > self.rocket_cooldown):
            
            self.fire_rocket()
            self.rocket_cooldown = current_time + 500  # 0.5 segundos de cooldown
        
        # Atualização dos projéteis (novo)
        for rocket in self.rockets[:]:
            rocket.update()
            if rocket.rect.bottom < 0:  # Remove se sair da tela
                self.rockets.remove(rocket)
        
        
    def fire_rocket(self):
        self.rockets.append(Rocket(self.rect.centerx, self.rect.top))
        
        
    def draw(self, screen):
        super().draw(screen) 
        # Desenha os foguetes
        for rocket in self.rockets:
            rocket.draw(screen)
        
        # Desenha ícone da bazuca
        if self.has_rocket:
            screen.blit(self.rocket_icon, self.rocket_icon_pos)
            
        # Opcional: Desenha o combustível (Exemplo simples)
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, self.fuel, 20))

