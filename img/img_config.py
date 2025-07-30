# img/img_config.py
import pygame
import os

class ImgConfig:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.asset_dir = "./assets"
        
        # Dicionário de fallback para imagens
        self.fallback_images = {
            "track": self._create_fallback_surface(width, height, (50, 50, 50)),
            "car": self._create_fallback_surface(50, 90, (255, 0, 0)),
            "fuel": self._create_fallback_surface(50, 50, (255, 255, 0)),
            "enemy": self._create_fallback_surface(70, 110, (0, 0, 255)),
            "ghost": self._create_fallback_surface(50, 50, (150, 0, 150)),
            "explosion": self._create_fallback_surface(60, 60, (255, 100, 0)),
            "rocket": self._create_fallback_surface(50, 50, (255, 200, 0))
        }

        # Carrega as imagens com tratamento de erro
        self.track_img = self._load_image("track/track.png", (width, height), "track")
        self.car_img = self._load_image("cars/car.png", (50, 90), "car", alpha=True)
        self.fuel_img = self._load_image("icons/fuel.png", (50, 50), "fuel", alpha=True)
        self.ambulancia_img = self._load_image("cars/ambulancia.png", (70, 110), "enemy", alpha=True)
        self.onibus_img = self._load_image("cars/onibus.png", (70, 170), "enemy", alpha=True)
        self.car_enemy = self._load_image("cars/car_verde.png", (50, 100), "enemy", alpha=True)
        self.ghost_power_img = self._load_image("icons/fantasma.png", (50, 50), "ghost", alpha=True)
        self.rocket_pickup_img = self._load_image("weapons/rocket.png", (50, 50), "rocket", alpha=True)

        # Explosões
        self.explosion_1 = self._load_image("track/explosion_1.png", (60, 60), "explosion", alpha=True)
        self.explosion_2 = self._load_image("track/explosion_2.png", (90, 90), "explosion", alpha=True)
        self.explosion_3 = self._load_image("track/explosion_3.png", (120, 120), "explosion", alpha=True)

    def _create_fallback_surface(self, width, height, color):
        """Cria uma superfície de fallback com cor específica"""
        surf = pygame.Surface((width, height))
        surf.fill(color)
        pygame.draw.rect(surf, (255, 255, 255), surf.get_rect(), 2)  # Borda branca
        return surf

    def _load_image(self, path, size, fallback_key, alpha=False):
        """Carrega uma imagem com tratamento de erros"""
        try:
            full_path = os.path.join(self.asset_dir, path)
            if alpha:
                image = pygame.image.load(full_path).convert_alpha()
            else:
                image = pygame.image.load(full_path).convert()
            return pygame.transform.scale(image, size)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar {path}: {e}. Usando fallback.")
            return self.fallback_images[fallback_key]