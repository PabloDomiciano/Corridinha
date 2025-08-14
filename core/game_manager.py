import pygame
import random
from core.game_world import GameWorld
from entities.pickups.effects.ghost_effect import GhostPickupEffect
from entities.player import Player
from entities.side_gif import SideGif
from img import img_config
from img.img_config import ImgConfig
from ui.hud import HUD
from ui.screen import Screen


class GameManager:
    def __init__(self, width, height, title):
        pygame.init()

        # Inicializa o mixer de áudio
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        self.width = width
        self.height = height
        self.running = True
        self.fps = 60
        self.clock = pygame.time.Clock()

        self.screen = Screen(width, height, title)
        self.img_config = ImgConfig(width, height)
        self.game_world = GameWorld(width, height, self.img_config)
        self.game_world.game_manager = self  # Permite acesso aos sons
        self.game_world.car.game_manager = self  # Para o jogador acessar os sons também

        # Pontuação
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.game_over_time = None

        # Carrega os sons
        self._load_sounds()

        self.hud = HUD(
            self.screen.surface,
            self.game_world.car,
            self.img_config,
            lambda: self.score,
        )

        self.ghost_effect = GhostPickupEffect(self.game_world.car)

        self.player_controls_enabled = True
        self.showing_explosion = False
        self.explosion_end_time = 0

        # GIFs laterais
        self.side_gifs_list = []
        self._init_side_gifs()

    def _init_side_gifs(self):
        """Cria GIFs laterais com tamanho individual"""
        if not self.img_config.side_gifs:
            print("Nenhum GIF encontrado.")
            return

        sizes = {
            "coqueiro": (40, 80),  # tamanho específico para 'coqueiro'
            "default": (40, 40),  # tamanho padrão para outros GIFs
        }

        for folder_name, frames in self.img_config.side_gifs.items():
            if not frames:
                continue
            size = sizes.get(folder_name, sizes["default"])

            # Lado esquerdo
            x_left = 6
            y_left = random.randint(-200, self.height - 50)

            # Lado direito
            x_right = self.width - size[0] - 6
            y_right = random.randint(-200, self.height - 50)
            # evita que fiquem muito próximos verticalmente
            while abs(y_right - y_left) < 80:
                y_right = random.randint(-200, self.height - 50)

            self.side_gifs_list.append(
                SideGif(frames, x_left, y_left, speed=5, frame_duration=300, size=size)
            )
            self.side_gifs_list.append(
                SideGif(
                    frames, x_right, y_right, speed=5, frame_duration=300, size=size
                )
            )

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()
            self._handle_events()
            self._update(current_time)
            self._render()
            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _update(self, current_time):
        # Atualiza a pontuação se o jogo não terminou
        if not self.game_over:
            self.score = (current_time - self.start_ticks) // 100

        # Atualiza o mundo do jogo com as teclas pressionadas
        keys = pygame.key.get_pressed() if self.player_controls_enabled else {}
        self.game_world.update(keys)

        # Atualiza os GIFs laterais
        for gif in self.side_gifs_list:
            gif.update()

        # Gerencia o poder fantasma
        self._handle_ghost_power(current_time)

        # Verifica condições do jogo se não estiver em explosão ou game over
        if not self.showing_explosion and not self.game_over:
            self._check_game_conditions()

        # Encerra o jogo após 3 segundos do game over
        if self.game_over and current_time - self.game_over_time > 3000:
            self.running = False

        # Encerra o jogo quando terminar a explosão
        if self.showing_explosion and current_time >= self.explosion_end_time:
            self.running = False

    def _handle_ghost_power(self, current_time):
        self._check_ghost_pickup_collision(current_time)
        self._update_ghost_effect(current_time)

    def _check_ghost_pickup_collision(self, current_time):
        for pickup in self.game_world.ghost_pickups[:]:
            if pickup.check_collision(self.game_world.car):
                self._activate_ghost_power(current_time)
                self.game_world.ghost_pickups.remove(pickup)
                break

    def _activate_ghost_power(self, current_time):
        """Ativa o poder fantasma no jogador"""
        self.game_world.car.ghost_power_active = True
        self.game_world.car.ghost_power_end_time = current_time + 8000  # 8 segundos
        self.ghost_effect.set_ghost_mode(True)

    def _update_ghost_effect(self, current_time):
        """Atualiza o efeito fantasma"""
        if not self.game_world.car.ghost_power_active:
            return

        remaining_time = self.game_world.car.ghost_power_end_time - current_time

        # Ativa piscar nos últimos 3 segundos
        if remaining_time < self.game_world.car.blink_start_offset:
            self.ghost_effect.is_blinking = True
            self.ghost_effect.update(current_time)
        else:
            self.ghost_effect.is_blinking = False

        # Desativa quando o tempo acabar
        if remaining_time <= 0:
            self._deactivate_ghost_power()

    def _deactivate_ghost_power(self):
        """Desativa o poder fantasma"""
        self.game_world.car.ghost_power_active = False
        self.ghost_effect.set_ghost_mode(False)

    def _check_game_conditions(self):
        self._check_collisions()
        self._check_fuel()

    def _check_collisions(self):
        # Se não há inimigos, não precisa verificar colisões
        if not self.game_world.enemies:
            return

        # Verifica se o efeito fantasma está ativo no jogador
        current_time = pygame.time.get_ticks()
        ghost_mode_active = (
            hasattr(self.game_world.car, "ghost_power_active")
            and self.game_world.car.ghost_power_active
            and current_time < self.game_world.car.ghost_power_end_time
        )

        for enemy in self.game_world.enemies[:]:
            if self.game_world.car.check_collision(enemy):
                if ghost_mode_active:
                    continue

                # Verificação de segurança
                if not hasattr(self.game_world, "frozen"):
                    self.game_world.frozen = False

                # Congela todo o jogo
                self.game_world.freeze_all()
                self.player_controls_enabled = False

                # Ativa explosão
                car_center = self.game_world.car.rect.center
                self.game_world.explosion.trigger(car_center[0], car_center[1], 50)
                self.explosion_end_time = current_time + 2000
                self.showing_explosion = True
                self.game_over = True
                self.game_over_time = current_time
                break  # Sai do loop após a primeira colisão

    def _check_fuel(self):
        if self.game_world.car.fuel <= 0:
            self.game_world.freeze_all()
            self.game_over = True
            self.game_over_time = pygame.time.get_ticks()

    def _load_sounds(self):
        """Carrega todos os sons do jogo"""
        try:
            # Sons do motor
            self.game_world.car.load_sounds(
                "assets/sounds/engine/idle.mp3",  # Som de aceleração
                "assets/sounds/engine/idle.mp3",  # Som de motor parado
            )

            # Efeitos sonoros
            self.explosion_sound = pygame.mixer.Sound(
                "assets/sounds/effects/explosion.mp3"
            )
            self.rocket_sound = pygame.mixer.Sound(
                "assets/sounds/effects/rocket_launch.mp3"
            )

            # Sons específicos para cada pickup
            self.fuel_pickup_sound = pygame.mixer.Sound(
                "assets/sounds/effects/fuel_pickup.wav"
            )
            self.ghost_pickup_sound = pygame.mixer.Sound(
                "assets/sounds/effects/ghost_pickup.mp3"
            )
            self.rocket_pickup_sound = pygame.mixer.Sound(
                "assets/sounds/effects/pickup.wav"
            )

            self.fuel_pickup_sound.set_volume(0.25)  # Baixinho, não é o foco
            self.ghost_pickup_sound.set_volume(0.35)  # Um pouco mais perceptível
            self.rocket_pickup_sound.set_volume(0.6)  # Destaque, mas não exagerado
            self.rocket_sound.set_volume(0.65)  # Barulho do disparo, bem presente
            self.explosion_sound.set_volume(0.85)  # Alto para impacto realista

        except Exception as e:
            print(f"Erro ao carregar sons: {e}")
            # Cria sons dummy para evitar erros
            dummy_sound = pygame.mixer.Sound(buffer=bytearray(100))
            self.explosion_sound = dummy_sound
            self.rocket_sound = dummy_sound
            self.pickup_sound = dummy_sound

    def _render(self):
        # Limpa a tela
        self.screen.surface.fill((0, 0, 0))

        # Desenha o mundo do jogo
        self.game_world.draw(self.screen.surface)

        # Desenha os GIFs laterais
        for gif in self.side_gifs_list:
            gif.draw(self.screen.surface)

        # Atualiza e desenha o HUD
        self.hud.update()
        self.hud.draw()

        # Overlay final (se game over)
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height))
            overlay.set_alpha(180)
            overlay.fill((50, 50, 50))
            self.screen.surface.blit(overlay, (0, 0))

            font = pygame.font.Font(None, 50)
            final_text = font.render(
                f"Pontuação Final: {self.score}", True, (255, 255, 255)
            )
            text_x = self.width // 2 - final_text.get_width() // 2
            text_y = self.height // 2 - final_text.get_height() // 2
            self.screen.surface.blit(final_text, (text_x, text_y))
