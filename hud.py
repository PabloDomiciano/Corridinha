import pygame

class HUD:
    def __init__(self, screen, car):
        self.screen = screen
        self.car = car
        self.font = pygame.font.SysFont("Arial", 20)
        self.max_fuel = 100
        self.fuel = self.max_fuel

    def update(self):
        # Simula consumo de combustível
        if self.fuel > 0:
            self.fuel -= 0.05

    def draw(self):
        # Velocidade
        speed_text = self.font.render(f"Velocidade: {self.car.speed} km/h", True, (255, 255, 255))
        self.screen.blit(speed_text, (10, 10))

        # Combustível
        fuel_bar_width = 200
        fuel_bar_height = 20
        fuel_percentage = self.fuel / self.max_fuel
        fuel_color = (0, 200, 0) if fuel_percentage > 0.3 else (255, 100, 0)

        pygame.draw.rect(self.screen, (100, 100, 100), (10, 40, fuel_bar_width, fuel_bar_height))  # fundo
        pygame.draw.rect(self.screen, fuel_color, (10, 40, fuel_bar_width * fuel_percentage, fuel_bar_height))  # preenchimento
        fuel_text = self.font.render("Combustível", True, (255, 255, 255))
        self.screen.blit(fuel_text, (10, 65))
