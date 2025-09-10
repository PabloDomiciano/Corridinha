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

# Adicione estas importações
from utils.score_manager import ScoreManager
from ui.highscore_screen import HighscoreScreen
from ui.leaderboard_screen import LeaderboardScreen


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

        # Sistema de Highscore (ADICIONADO)
        self.score_manager = ScoreManager()
        self.highscore_screen = HighscoreScreen(self.score_manager)
        self.leaderboard_screen = LeaderboardScreen(self.score_manager)
        self.current_state = "start_screen"

        # Carrega os sons
        self._load_sounds()

        self.hud = HUD(
            self.screen.surface,
            self.game_world.car,
            self.img_config,
            lambda: self.score,
        )

        self.game_world.car.ghost_effect = GhostPickupEffect(self.game_world.car)

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

            # Tela inicial
            if self.current_state == "start_screen":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.current_state = "game"
                        self._restart_game()  # Reinicia o jogo ao começar
                    elif event.key == pygame.K_l:
                        self.current_state = "leaderboard"
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

            # Tela de input de highscore
            elif self.current_state == "highscore_input":
                result = self.highscore_screen.handle_event(event)  # continua tratando a digitação
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Finaliza input e volta para o menu inicial
                        self.current_state = "start_screen"
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

            # Tela de leaderboard
            elif self.current_state == "leaderboard":
                result = self.leaderboard_screen.handle_event(event)
                if result == "menu":
                    self.current_state = "start_screen"

            # Tela de game over
            elif self.current_state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self._restart_game()
                    elif event.key == pygame.K_l:
                        self.current_state = "leaderboard"
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                        self.current_state = "start_screen"


    def _update(self, current_time):
        # Atualiza apenas se estiver no estado de jogo
        if self.current_state == "game":
            if not self.game_over:
                # Calcula pontuação baseada em tempo (segundos * 10) ou distância
                elapsed_seconds = (current_time - self.start_ticks) // 1000
                self.score = elapsed_seconds * 10  # 10 pontos por segundo
                
                
                self._check_rocket_explosion()

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

            # Transição para highscore_input ou game_over após 3 segundos
            if self.game_over and current_time - self.game_over_time > 3000:
                # VERIFICA se é uma pontuação alta ANTES de mudar de estado
                if self.score_manager.is_highscore(self.score):
                    self.current_state = "highscore_input"
                    self.highscore_screen.active = True  # Ativa a tela de highscore
                    print(f"Nova pontuação alta! Score: {self.score}")  # DEBUG
                else:
                    self.current_state = "game_over"
                    print(f"Pontuação não é highscore: {self.score}")  # DEBUG

            # CORREÇÃO: Não encerrar o jogo após explosão, apenas mudar de estado
            if (self.showing_explosion and current_time >= self.explosion_end_time
                and self.current_state == "game"):
                self.showing_explosion = False
                # Não encerre o jogo, apenas processe a transição de estado
                if self.game_over:
                    if self.score_manager.is_highscore(self.score):
                        self.current_state = "highscore_input"
                        self.highscore_screen.active = True
                    else:
                        self.current_state = "game_over"

        # ADICIONADO: Atualiza a tela de highscore se necessário
        elif self.current_state == "highscore_input":
            self.highscore_screen.update()

        # ADICIONADO: Para estados de menu, não faz nada especial
        elif self.current_state in ["start_screen", "leaderboard", "game_over"]:
            # Esses estados não precisam de atualizações de jogo
            pass
        

    def _handle_ghost_power(self, current_time):
        self._check_ghost_pickup_collision(current_time)
        self._update_ghost_effect(current_time)

    def _check_ghost_pickup_collision(self, current_time):
        for pickup in self.game_world.ghost_pickups[:]:
            if pickup.check_collision(self.game_world.car):
                self._activate_ghost_power(current_time)
                self.game_world.ghost_pickups.remove(pickup)
                # Toca o som do pickup
                if hasattr(self, "ghost_pickup_sound"):
                    self.ghost_pickup_sound.play()
                break

    def _activate_ghost_power(self, current_time):
        """Ativa o poder fantasma no jogador"""
        print("Ghost power ATIVADO!")  # DEBUG
        self.game_world.car.ghost_power_active = True
        self.game_world.car.ghost_power_end_time = current_time + 8000  # 8 segundos

        if self.game_world.car.ghost_effect:
            self.game_world.car.ghost_effect.set_ghost_mode(True)
        else:
            print("ERRO: ghost_effect não encontrado!")

    def _update_ghost_effect(self, current_time):
        """Atualiza o efeito fantasma"""
        if not self.game_world.car.ghost_power_active:
            return

        remaining_time = self.game_world.car.ghost_power_end_time - current_time

        # Ativa piscar nos últimos 3 segundos
        if remaining_time < self.game_world.car.blink_start_offset:
            if self.game_world.car.ghost_effect:
                self.game_world.car.ghost_effect.is_blinking = True
                self.game_world.car.ghost_effect.update(current_time)
        else:
            if self.game_world.car.ghost_effect:
                self.game_world.car.ghost_effect.is_blinking = False

        # Desativa quando o tempo acabar
        if remaining_time <= 0:
            self._deactivate_ghost_power()

    def _deactivate_ghost_power(self):
        """Desativa o poder fantasma"""
        self.game_world.car.ghost_power_active = False
        if self.game_world.car.ghost_effect:
            self.game_world.car.ghost_effect.set_ghost_mode(False)

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
            # USA O MÉTODO check_collision DO EFEITO FANTASMA
            collision_occurred = False

            # Verifica se o efeito fantasma existe e detecta colisão
            if (
                hasattr(self.game_world.car, "ghost_effect")
                and self.game_world.car.ghost_effect is not None
            ):
                collision_occurred = self.game_world.car.ghost_effect.check_collision(
                    enemy
                )
            else:
                # Fallback: verificação de colisão normal se não houver efeito fantasma
                collision_occurred = self.game_world.car.check_collision(enemy)

            if collision_occurred:
                if ghost_mode_active:
                    print("Colisão ignorada - modo fantasma ativo")  # DEBUG
                    continue  # Ignora colisão se estiver no modo fantasma

                print("COLISÃO DETECTADA - GAME OVER")  # DEBUG

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

                # Toca som de explosão
                if hasattr(self, "explosion_sound"):
                    self.explosion_sound.play()

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

        # Desenha de acordo com o estado atual
        if self.current_state == "start_screen":
            # ADICIONADO: Desenha a tela inicial
            self._draw_start_screen()

        elif self.current_state == "game":
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

        elif self.current_state == "highscore_input":
            # ADICIONADO: Desenha a tela de inserção de nome
            self.highscore_screen.draw(self.screen.surface, self.score)

        elif self.current_state == "leaderboard":
            # ADICIONADO: Desenha a tela de leaderboard
            self.leaderboard_screen.draw(self.screen.surface)

        elif self.current_state == "game_over":
            # ADICIONADO: Tela de game over com opções
            self._draw_game_over_screen()

    def _draw_game_over_screen(self):
        """Desenha a tela de game over com opções"""
        # Fundo escuro semi-transparente
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.surface.blit(overlay, (0, 0))

        # Título
        font_large = pygame.font.Font(None, 64)
        title = font_large.render("FIM DE JOGO", True, (255, 255, 255))
        self.screen.surface.blit(title, (self.width // 2 - title.get_width() // 2, 100))

        # Pontuação
        font_medium = pygame.font.Font(None, 48)
        score_text = font_medium.render(
            f"Pontuação: {self.score}", True, (255, 255, 255)
        )
        self.screen.surface.blit(
            score_text, (self.width // 2 - score_text.get_width() // 2, 180)
        )

        # Opções
        font_small = pygame.font.Font(None, 36)
        options = [
            "Pressione R para reiniciar",
            "Pressione L para ver o ranking",
            "Pressione ESC ou ENTER para voltar ao menu",
        ]

        y_pos = 280
        for option in options:
            text = font_small.render(option, True, (200, 200, 200))
            self.screen.surface.blit(
                text, (self.width // 2 - text.get_width() // 2, y_pos)
            )
            y_pos += 40

    def _restart_game(self):
        """Reinicia o jogo"""
        # Recria todas as instâncias necessárias
        self.game_world = GameWorld(self.width, self.height, self.img_config)
        self.game_world.game_manager = self
        self.game_world.car.game_manager = self
        self.game_world.car.ghost_effect = GhostPickupEffect(self.game_world.car)

        # Reseta variáveis de estado
        self.score = 0
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.game_over_time = None
        self.player_controls_enabled = True
        self.showing_explosion = False
        self.explosion_end_time = 0

        # Reseta a tela de highscore
        self.highscore_screen.input_text = ""
        self.highscore_screen.active = False

        # Volta para o estado de jogo
        self.current_state = "game"

        # Recria o HUD
        self.hud = HUD(
            self.screen.surface,
            self.game_world.car,
            self.img_config,
            lambda: self.score,
        )

        # Recria os GIFs laterais
        self.side_gifs_list = []
        self._init_side_gifs()

    def _draw_start_screen(self):
        """Desenha uma tela inicial simples"""
        self.screen.surface.fill((0, 0, 50))  # Fundo azul escuro

        font_large = pygame.font.Font(None, 64)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)

        # Título
        title = font_large.render("CORRIDINHA", True, (255, 255, 0))
        self.screen.surface.blit(title, (self.width // 2 - title.get_width() // 2, 100))

        # Opções
        options = [
            "Pressione ENTER para começar",
            "Pressione L para ver o ranking",
            "Pressione ESC para sair",
        ]

        y_pos = 250
        for option in options:
            text = font_medium.render(option, True, (255, 255, 255))
            self.screen.surface.blit(
                text, (self.width // 2 - text.get_width() // 2, y_pos)
            )
            y_pos += 50

        # Instruções
        instructions = [
            "Use SETAS para mover",
            "Desvie dos carros inimigos",
            "Pegue os power-ups no caminho!",
        ]

        y_pos = 400
        for instruction in instructions:
            text = font_small.render(instruction, True, (200, 200, 200))
            self.screen.surface.blit(
                text, (self.width // 2 - text.get_width() // 2, y_pos)
            )
            y_pos += 30

    def check_highscore(self):
        """Verifica se a pontuação atual é um highscore"""
        return self.score_manager.is_highscore(self.score)