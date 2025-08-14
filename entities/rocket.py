import pygame
import random
from entities.base import BaseEntity
import math


class Rocket(BaseEntity):
    def __init__(self, x, y, speed=10):
        # Carrega a imagem do foguete do img_config
        image = pygame.Surface((20, 40), pygame.SRCALPHA)  # Fallback temporário

        super().__init__(image, x, y)
        self.speed = speed
        self.damage = 1
        self.trail_particles = []  # Partículas para o efeito de rastro
        self.last_trail_time = 0
        self.trail_interval = 30  # ms entre partículas do rastro

        # Configurações do rastro melhoradas
        self.base_trail_color = (255, 100, 0)  # Laranja mais forte no início
        self.trail_length = 15  # Mais partículas para um rastro mais longo
        self.max_trail_size = 8  # Tamanho máximo inicial das partículas
        self.min_trail_size = 1  # Tamanho mínimo no final
        self.particle_lifetime = 25  # Duração em frames

    def update(self):
        if not self.frozen:
            self.rect.y -= self.speed
            current_time = pygame.time.get_ticks()

            # Adiciona nova partícula ao rastro periodicamente
            if current_time - self.last_trail_time > self.trail_interval:
                self._add_trail_particle()
                self.last_trail_time = current_time

            # Atualiza partículas existentes
            for particle in self.trail_particles[:]:
                particle["lifetime"] -= 1

                if particle["lifetime"] <= 0:
                    self.trail_particles.remove(particle)
                else:
                    # Progressão da vida (0 a 1)
                    life_progress = 1 - (particle["lifetime"] / self.particle_lifetime)

                    # Movimento para baixo com desaceleração
                    particle["y"] += 1 + (2 * life_progress)

                    # Movimento horizontal aleatório suave
                    particle["x"] += particle["drift"] * (0.5 + life_progress)

                    # Diminuição do tamanho
                    particle["size"] = self.max_trail_size - (
                        life_progress * (self.max_trail_size - self.min_trail_size)
                    )

                    # Mudança de cor (de laranja para amarelo)
                    fade_progress = life_progress**0.5  # Suaviza a transição
                    particle["color"] = (
                        int(self.base_trail_color[0] * (1 - fade_progress * 0.7)),
                        int(self.base_trail_color[1] * (0.8 + fade_progress * 0.5)),
                        int(self.base_trail_color[2] * (0.3 + fade_progress * 0.7)),
                    )

    def _add_trail_particle(self):
        """Adiciona uma nova partícula ao rastro com propriedades dinâmicas"""
        if len(self.trail_particles) >= self.trail_length:
            self.trail_particles.pop(0)  # Remove a partícula mais antiga

        # Posição com pequena variação aleatória
        pos_variation = 3  # Quanto maior, mais espalhado
        x_pos = self.rect.centerx + random.uniform(-pos_variation, pos_variation)

        self.trail_particles.append(
            {
                "x": x_pos,
                "y": self.rect.bottom,
                "size": self.max_trail_size,
                "color": self.base_trail_color,
                "lifetime": self.particle_lifetime,
                "drift": random.uniform(-0.5, 0.5),  # Movimento horizontal aleatório
                "initial_size": self.max_trail_size,
            }
        )

    def draw(self, surface):
        # Desenha o rastro primeiro (para ficar atrás do foguete)
        for particle in self.trail_particles:
            # Calcula alpha baseado no tempo de vida restante
            alpha = int(255 * (particle["lifetime"] / self.particle_lifetime) ** 0.7)
            color = particle["color"]

            # Cria superfície para a partícula
            size = max(1, int(particle["size"]))
            particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

            # Desenha círculo com suavidade (usando apenas pygame.draw)
            pygame.draw.circle(
                particle_surf, (*color, alpha), (size, size), size  # Cor com alpha
            )

            # Desenha na tela principal
            surface.blit(
                particle_surf, (int(particle["x"] - size), int(particle["y"] - size))
            )

        # Desenha o foguete por cima do rastro
        super().draw(surface)
