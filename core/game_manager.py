import pygame
import random
import math
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
from ui.credits_screen import CreditsScreen


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
        self.bonus_score = 0  # Pontos de bônus (explosões, etc)
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.game_over_time = None

        # Sistema de Highscore (ADICIONADO)
        self.score_manager = ScoreManager()
        self.highscore_screen = HighscoreScreen(self.score_manager)
        self.leaderboard_screen = LeaderboardScreen(self.score_manager)
        self.credits_screen = CreditsScreen()
        self.current_state = "start_screen"

        # Menu inicial: opções e seleção (navegável por setas)
        self.menu_options = ["Iniciar Jogo", "Ranking", "Créditos", "Sair"]
        self.menu_selection = 0
        self.menu_rects = []  # Para armazenar as áreas clicáveis das opções


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
        """Cria GIFs laterais com spawn controlado por probabilidade"""
        if not self.img_config.side_gifs:
            return

        sizes = {
            "coqueiro": (40, 80),
            "casa": (120, 120),
            "pedra": (30, 30),
            "default": (40, 40),
        }

        base_offsets = {
            "default": 6,
        }

        spawn_chances = {
            "coqueiro": 0.9,
            "pedra": 0.4,
            "casa": 0.3,
        }

        for folder_name, frames in self.img_config.side_gifs.items():
            if not frames:
                continue

            chance = spawn_chances.get(folder_name, 1.0)
            if random.random() > chance:
                continue

            size = sizes.get(folder_name, sizes["default"])

            # Posição Y aleatória
            y = random.randint(-200, self.height - 50)

            if folder_name == "casa":
                # CASA apenas no lado direito
                x_right = self.width - size[0]  # colada na direita
                self.side_gifs_list.append(
                    SideGif(frames, x_right, y, speed=5, frame_duration=300, size=size)
                )
            else:
                # Outros objetos podem spawnar dos dois lados
                offset = base_offsets.get(folder_name, base_offsets["default"])

                x_left = offset
                x_right = self.width - size[0] - offset

                y_left = y
                y_right = random.randint(-200, self.height - 50)

                # Evita spawn no mesmo Y dos dois lados
                while abs(y_right - y_left) < 80:
                    y_right = random.randint(-200, self.height - 50)

                self.side_gifs_list.append(
                    SideGif(frames, x_left, y_left, speed=5, frame_duration=300, size=size)
                )
                self.side_gifs_list.append(
                    SideGif(frames, x_right, y_right, speed=5, frame_duration=300, size=size)
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
                    # Navegação do menu por setas
                    if event.key == pygame.K_UP:
                        self.menu_selection = (self.menu_selection - 1) % len(self.menu_options)
                    elif event.key == pygame.K_DOWN:
                        self.menu_selection = (self.menu_selection + 1) % len(self.menu_options)
                    elif event.key == pygame.K_RETURN:
                        # Executa a opção selecionada
                        choice = self.menu_options[self.menu_selection]
                        if choice == "Iniciar Jogo":
                            self.current_state = "game"
                            self._restart_game()
                        elif choice == "Ranking":
                            self.current_state = "leaderboard"
                            # Reset leaderboard animation
                            self.leaderboard_screen.alpha = 0
                            self.leaderboard_screen.last_time = pygame.time.get_ticks()
                            self.leaderboard_screen.start_time = pygame.time.get_ticks()
                        elif choice == "Créditos":
                            self.current_state = "credits"
                            # Reset credits animation
                            self.credits_screen.alpha = 0
                            self.credits_screen.last_time = pygame.time.get_ticks()
                            self.credits_screen.start_time = pygame.time.get_ticks()
                        elif choice == "Sair":
                            self.running = False
                    elif event.key == pygame.K_l:
                        self.current_state = "leaderboard"
                        self.leaderboard_screen.alpha = 0
                        self.leaderboard_screen.last_time = pygame.time.get_ticks()
                        self.leaderboard_screen.start_time = pygame.time.get_ticks()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                # Suporte a mouse: hover e clique
                elif event.type == pygame.MOUSEMOTION:
                    mx, my = event.pos
                    # Verifica hover sobre as opções do menu
                    for idx, rect in enumerate(self.menu_rects):
                        if rect.collidepoint(mx, my):
                            self.menu_selection = idx
                            break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # clique esquerdo
                        mx, my = event.pos
                        # Verifica clique nas opções do menu
                        for idx, rect in enumerate(self.menu_rects):
                            if rect.collidepoint(mx, my):
                                choice = self.menu_options[idx]
                                if choice == "Iniciar Jogo":
                                    self.current_state = "game"
                                    self._restart_game()
                                elif choice == "Ranking":
                                    self.current_state = "leaderboard"
                                    self.leaderboard_screen.alpha = 0
                                    self.leaderboard_screen.last_time = pygame.time.get_ticks()
                                    self.leaderboard_screen.start_time = pygame.time.get_ticks()
                                elif choice == "Créditos":
                                    self.current_state = "credits"
                                    self.credits_screen.alpha = 0
                                    self.credits_screen.last_time = pygame.time.get_ticks()
                                    self.credits_screen.start_time = pygame.time.get_ticks()
                                elif choice == "Sair":
                                    self.running = False
                                break

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

            # Tela de créditos
            elif self.current_state == "credits":
                result = self.credits_screen.handle_event(event)
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
                # Calcula pontuação baseada na distância percorrida + bônus
                # Distância é medida em pixels, convertemos para metros (dividindo por 100)
                # E multiplicamos por 1 para cada metro = 1 ponto
                distance_in_meters = int(self.game_world.distance_traveled / 100)
                self.score = distance_in_meters + self.bonus_score

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

        # ADICIONADO: Atualiza a tela de leaderboard (fade-in)
        elif self.current_state == "leaderboard":
            self.leaderboard_screen.update()

        # ADICIONADO: Atualiza a tela de créditos (fade-in)
        elif self.current_state == "credits":
            self.credits_screen.update()

        # ADICIONADO: Para estados de menu, não faz nada especial
        elif self.current_state in ["start_screen", "leaderboard", "game_over"]:
            # Esses estados não precisam de atualizações de jogo
            pass


    def _check_rocket_explosion(self):
        """Verifica se a rocket explodiu inimigos e adiciona pontos"""
        # NOTA: A adição de pontos agora é feita diretamente no game_world
        # quando o foguete colide com o inimigo (linha ~85 de game_world.py)
        if hasattr(self.game_world, "rocket_explosion_active") and self.game_world.rocket_explosion_active:
            for enemy in self.game_world.enemies[:]:
                if self.game_world.rocket_explosion_rect.colliderect(enemy.rect):
                    # Pontos já são adicionados no game_world.update()
                    self.game_world.enemies.remove(enemy)
                    # Pode tocar som de inimigo explodindo, se quiser
                    if hasattr(self, "explosion_sound"):
                        self.explosion_sound.play()

    def _handle_ghost_power(self, current_time):
        self._check_ghost_pickup_collision(current_time)

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
        self.game_world.car.activate_ghost_power(current_time, duration=8000)

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
                
                # Congela os sidegifs
                for gif in self.side_gifs_list:
                    gif.frozen = True

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
        """Verifica se o combustível acabou"""
        if self.game_world.car.fuel <= 0:
            self.game_world.freeze_all()
            
            # Congela os sidegifs
            for gif in self.side_gifs_list:
                gif.frozen = True
                
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

            self.fuel_pickup_sound = pygame.mixer.Sound(
                "assets/sounds/effects/fuel_pickup.wav"
            )
            self.ghost_pickup_sound = pygame.mixer.Sound(
                "assets/sounds/effects/ghost_pickup.mp3"
            )
            self.rocket_pickup_sound = pygame.mixer.Sound(
                "assets/sounds/effects/pickup.wav"
            )

            self.fuel_pickup_sound.set_volume(0.25)
            self.ghost_pickup_sound.set_volume(0.35)
            self.rocket_pickup_sound.set_volume(0.6)
            self.rocket_sound.set_volume(0.65)
            self.explosion_sound.set_volume(0.85)

            # 🎵 Música de fundo
            pygame.mixer.music.load("assets/sounds/music.mp3")
            pygame.mixer.music.set_volume(0.5)  # volume da música (0.0 até 1.0)
            pygame.mixer.music.play(-1)  # -1 = loop infinito

        except Exception as e:
            print(f"Erro ao carregar sons: {e}")
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

        elif self.current_state == "highscore_input":
            # ADICIONADO: Desenha a tela de inserção de nome
            self.highscore_screen.draw(self.screen.surface, self.score)

        elif self.current_state == "leaderboard":
            # ADICIONADO: Desenha a tela de leaderboard
            self.leaderboard_screen.draw(self.screen.surface)

        elif self.current_state == "credits":
            # ADICIONADO: Desenha a tela de créditos
            self.credits_screen.draw(self.screen.surface)

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
        self.bonus_score = 0  # Reseta os pontos de bônus
        self.start_ticks = pygame.time.get_ticks()
        self.game_over = False
        self.game_over_time = None
        self.player_controls_enabled = True
        self.showing_explosion = False
        self.explosion_end_time = 0
        
        # Reseta a distância percorrida
        self.game_world.distance_traveled = 0

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
        # Fundo com gradiente vertical (doescuro para mais claro)
        top_color = pygame.Color(6, 16, 42)
        bottom_color = pygame.Color(10, 60, 120)
        for i in range(self.height):
            ratio = i / self.height
            r = int(top_color.r * (1 - ratio) + bottom_color.r * ratio)
            g = int(top_color.g * (1 - ratio) + bottom_color.g * ratio)
            b = int(top_color.b * (1 - ratio) + bottom_color.b * ratio)
            pygame.draw.line(self.screen.surface, (r, g, b), (0, i), (self.width, i))

        # Fontes
        font_large = pygame.font.Font(None, 72)
        font_medium = pygame.font.Font(None, 40)
        font_small = pygame.font.Font(None, 22)

        # Título com sombra
        title = font_large.render("CORRIDINHA", True, (255, 230, 120))
        title_shadow = font_large.render("CORRIDINHA", True, (20, 20, 40))
        tx = self.width // 2 - title.get_width() // 2
        self.screen.surface.blit(title_shadow, (tx + 4, 104))
        self.screen.surface.blit(title, (tx, 100))

        # Pequena descrição abaixo
        subtitle = font_small.render("Desvie, colete power-ups e sobreviva o maior tempo!", True, (220, 220, 220))
        self.screen.surface.blit(subtitle, (self.width // 2 - subtitle.get_width() // 2, 170))

        # Animação de pulso para item selecionado
        t = pygame.time.get_ticks() / 1000.0
        pulse = 1.0 + 0.05 * (1 + math.sin(t * 3))

        # Desenha um sprite de carro (pixel art se disponível) com um leve bob
        try:
            car_sprite = self.img_config.car_img
        except Exception:
            car_sprite = None

        if car_sprite:
            # Escala para uma dimensão agradável no menu
            car_w = 120
            car_h = int(car_sprite.get_height() * (car_w / car_sprite.get_width()))
            car_img_scaled = pygame.transform.scale(car_sprite, (car_w, car_h))

            # Bob (subida/descida) para animação
            bob = int(8 * math.sin(t * 2.0))

            car_x = self.width // 2 - car_w // 2
            car_y = 200 + bob

            # Sombra simples
            shadow = pygame.Surface((car_w, 8), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow, (0, 0, 0, 100), shadow.get_rect())
            self.screen.surface.blit(shadow, (car_x, car_y + car_h - 6))

            # Desenha o carro
            self.screen.surface.blit(car_img_scaled, (car_x, car_y))

        # Opções navegáveis com destaque
        y_pos = 250
        self.menu_rects = []  # Limpa e recria as áreas clicáveis
        for idx, option in enumerate(self.menu_options):
            is_selected = idx == self.menu_selection
            color = (255, 240, 140) if is_selected else (240, 240, 240)
            text = font_medium.render(option, True, color)

            # Calcula posição, aplica transformação se selecionado
            x = self.width // 2 - text.get_width() // 2
            y = y_pos
            
            # Armazena a área clicável (com padding)
            rect = pygame.Rect(x - 15, y - 7, text.get_width() + 30, text.get_height() + 14)
            self.menu_rects.append(rect)
            
            if is_selected:
                # Pula levemente e aumenta
                scaled = int(text.get_height() * pulse)
                # Centro preservado: desenha um highlight
                highlight = pygame.Surface((text.get_width() + 30, text.get_height() + 14), pygame.SRCALPHA)
                highlight.fill((30, 30, 60, 120))
                self.screen.surface.blit(highlight, (x - 15, y - 7))

            self.screen.surface.blit(text, (x, y))
            y_pos += 60

        # Instruções
        instructions = [
            "Use SETAS ou o MOUSE para navegar",
            "ENTER ou clique para confirmar",
            "Boa sorte!",
        ]

        y_pos = self.height - 90
        for instruction in instructions:
            text = font_small.render(instruction, True, (200, 200, 200))
            self.screen.surface.blit(text, (self.width // 2 - text.get_width() // 2, y_pos))
            y_pos += 22

    def check_highscore(self):
        """Verifica se a pontuação atual é um highscore"""
        return self.score_manager.is_highscore(self.score)