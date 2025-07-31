import pygame
from entities.carro import Carro


class Player(Carro):
    def __init__(self, image, screen_width, screen_height, x_pos, y_pos):
        super().__init__(image, x_pos, y_pos)
        self.screen_width = screen_width
        self.screen_height = screen_height
<<<<<<< Updated upstream
        self.speed = 3
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_consumption_rate = 0.05
        self.left_limit = 100
        self.right_limit = self.screen_width - 100 - self.rect.width

        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def update(self, keys):
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
        else:
            
            pass

    def draw(self, screen):
        # Desenha o carro
        super().draw(screen)  # Chama o método draw da classe Carro para desenhar a imagem

        # Opcional: Desenha o combustível (Exemplo simples)
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, self.fuel, 20))

=======

        # Propriedades do jogador
        self.speed = 200  # pixels por segundo
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_consumption_rate = 5  # combustível por segundo

        # Limites da pista
        self.left_limit = 100
        self.right_limit = self.screen_width - 100 - self.rect.width

        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y
        )

    def update(self, keys, delta_time):
        if self.fuel <= 0:
            return

        # Cálculo de deslocamento
        displacement = self.speed * delta_time

        if keys[pygame.K_LEFT] and self.rect.x > self.left_limit:
            self.rect.x -= displacement
        if keys[pygame.K_RIGHT] and self.rect.x < self.right_limit:
            self.rect.x += displacement
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= displacement
        if keys[pygame.K_DOWN] and self.rect.y < self.screen_height - self.rect.height:
            self.rect.y += displacement

        # Atualiza hitbox
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y
        )

        # Consome combustível proporcional ao tempo
        self.fuel -= self.fuel_consumption_rate * delta_time
        if self.fuel < 0:
            self.fuel = 0

    def draw(self, screen):
        super().draw(screen)  # Desenha o carro
        # Combustível opcional no HUD (removível)
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, self.fuel, 20))
>>>>>>> Stashed changes
