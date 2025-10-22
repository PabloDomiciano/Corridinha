import pygame
from entities.carro import Carro
from entities.rocket import Rocket


class Player(Carro):
    """
    Representa o carro do jogador com todos os sistemas de controle.
    
    Responsabilidades:
    - Controlar movimento do jogador (teclas direcionais)
    - Gerenciar combustível (consumo e reabastecimento)
    - Controlar sistema de armas (foguetes)
    - Gerenciar power-ups (fantasma, etc)
    - Tocar sons de motor
    """
    
    def __init__(self, image, screen_width, screen_height, x_pos, y_pos, rocket_icon=None):
        # Inicializa a classe pai (Carro)
        super().__init__(image, x_pos, y_pos)
        
        # === CONFIGURAÇÕES DE TELA ===
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # === CONFIGURAÇÕES DE MOVIMENTO ===
        self.speed = 3  # Velocidade de movimento (pixels por frame)
        self.left_limit = 100  # Limite esquerdo da área jogável
        self.right_limit = screen_width - 100 - self.rect.width  # Limite direito
        
        # === SISTEMA DE COMBUSTÍVEL ===
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_consumption_rate = 0.04  # Quanto de combustível gasta por segundo
        
        # === SISTEMA DE FOGUETES ===
        self.rockets = []  # Lista de foguetes ativos na tela
        self.rocket_cooldown = 0  # Tempo até poder disparar novamente
        self.has_rocket = False  # Se tem power-up de foguete ativo
        self.rocket_end_time = 0  # Quando o power-up de foguete acaba
        
        # Configurações de interface do foguete
        self.rocket_icon = self._validate_rocket_icon(rocket_icon)
        self.rocket_icon_pos = (10, 50)
        self.rocket_blink_start_offset = 3000  # Quando começar a piscar (3s antes de acabar)
        self.rocket_blink_interval = 200  # Intervalo entre piscadas (ms)
        self.last_rocket_blink_time = 0
        self.rocket_blink_visible = True
        
        # Configurações visuais da bazuca no carro
        self.rocket_on_car_img = None
        self.rocket_on_car_offset = (0, 0)
        self.rocket_scale_factor = 1.0
        
        # === SISTEMA DE POWER-UP FANTASMA ===
        self.ghost_power_active = False  # Se está com poder fantasma ativo
        self.ghost_power_end_time = 0  # Quando o poder acaba
        self.ghost_effect = None  # Referência ao efeito visual
        self.blink_start_offset = 3000  # Quando começar a piscar antes de acabar
        
        # === ESTADO DO JOGO ===
        self.frozen = False  # Se o jogo está pausado/congelado
        self.original_image = image.copy()  # Backup da imagem original (para efeitos)
        
        # === SISTEMA DE SOM ===
        self.car_acceleration_sound = None  # Som de aceleração
        self.car_idle_sound = None  # Som de motor parado
        self.is_accelerating = False  # Se está acelerando agora
        self.sound_playing = False  # Se algum som está tocando
        
        # Atualiza a hitbox inicial
        self.hitbox.set_rect(self.rect.width, self.rect.height, self.rect.x, self.rect.y)
    
    # === MÉTODOS DE INICIALIZAÇÃO ===
    
    def _validate_rocket_icon(self, icon):
        """Cria um ícone padrão caso nenhum seja fornecido"""
        if icon is None:
            # Cria um ícone simples de foguete
            icon = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.polygon(icon, (255, 200, 0), [(15, 0), (30, 30), (0, 30)])
            pygame.draw.rect(icon, (200, 200, 200), (12, 20, 6, 8))
        return icon

    
    # === MÉTODO PRINCIPAL DE ATUALIZAÇÃO ===
    
    def update(self, keys, dt):
        """
        Atualiza todos os sistemas do jogador a cada frame.
        
        Args:
            keys: Dicionário com estado das teclas pressionadas
            dt: Delta time (tempo desde o último frame em segundos)
        """
        # Se o jogo está congelado, para todos os sons e não atualiza
        if self.frozen:
            self.stop_sounds()
            return
        
        current_time = pygame.time.get_ticks()
        
        # Atualiza cada sistema do jogador
        self._handle_movement(keys, dt)  # Movimento com teclas
        self._handle_rockets(keys, dt)  # Disparo de foguetes
        self._update_fuel(dt)  # Consumo de combustível
        self.update_rocket_power(current_time)  # Power-up de foguete
        self.update_ghost_power(current_time)  # Power-up fantasma
        self._update_sound(keys)  # Sons do motor
    
    # === SISTEMA DE SOM ===
    
    def _update_sound(self, keys):
        """Gerencia os sons do motor baseado no movimento do jogador"""
        # Se não tem combustível, para todos os sons
        if self.fuel <= 0:
            self.stop_sounds()
            return
        
        # Verifica se alguma tecla de movimento está pressionada
        moving = any([
            keys[pygame.K_LEFT],
            keys[pygame.K_RIGHT],
            keys[pygame.K_UP],
            keys[pygame.K_DOWN],
        ])
        
        # Muda entre som de aceleração e idle
        if moving and not self.is_accelerating:
            self.is_accelerating = True
            self.play_acceleration_sound()
        elif not moving and self.is_accelerating:
            self.is_accelerating = False
            self.play_idle_sound()
    
    def play_acceleration_sound(self):
        """Toca o som de motor acelerando em loop"""
        if self.car_acceleration_sound and not self.sound_playing:
            self.car_idle_sound.stop()
            self.car_acceleration_sound.play(-1)  # Loop infinito
            self.sound_playing = True
    
    def play_idle_sound(self):
        """Toca o som de motor em idle (parado) em loop"""
        if self.car_idle_sound and not self.sound_playing:
            self.car_acceleration_sound.stop()
            self.car_idle_sound.play(-1)  # Loop infinito
            self.sound_playing = True
    
    def stop_sounds(self):
        """Para todos os sons do motor"""
        if self.car_acceleration_sound:
            self.car_acceleration_sound.stop()
        if self.car_idle_sound:
            self.car_idle_sound.stop()
        self.sound_playing = False
    
    # === SISTEMA DE POWER-UP: FOGUETE ===
    
    def activate_rocket_power(self, current_time):
        """Ativa o power-up de foguete por 10 segundos"""
        self.has_rocket = True
        self.rocket_end_time = current_time + 10000  # 10 segundos
        self.rocket_blink_visible = True

        if hasattr(self, "game_manager") and hasattr(self.game_manager, "img_config"):
            original_img = self.game_manager.img_config.rocket_pickup_img

            # Aumenta o fator de escala (de 0.7 para 0.9 por exemplo)
            self.rocket_scale_factor = 1.5  # Ajuste este valor conforme necessário

            # Calcula o tamanho proporcional ao carro
            rocket_width = int(self.rect.width * self.rocket_scale_factor)
            rocket_height = int(
                rocket_width * original_img.get_height() / original_img.get_width()
            )

            # Redimensiona a imagem
            scaled_img = pygame.transform.scale(
                original_img, (rocket_width, rocket_height)
            )

            # Remove a rotação ou ajusta para 0 graus para ficar vertical
            self.rocket_on_car_img = scaled_img  # Sem rotação
            # Ou se precisar de pequeno ajuste:
            # self.rocket_on_car_img = pygame.transform.rotate(scaled_img, 0)

            # Ajusta o offset para posicionar verticalmente no carro
            self.rocket_on_car_offset = (
                (self.rect.width - rocket_width) // 2,  # Centralizado horizontalmente
                -rocket_height + 75,  # 75 pixels acima do topo do carro
            )

    def update_rocket_power(self, current_time):
        """Atualiza o estado do poder do foguete"""
        if not self.has_rocket:
            return

        remaining_time = self.rocket_end_time - current_time

        # Desativa quando o tempo acabar
        if remaining_time <= 0:
            self.has_rocket = False
            return

        # Piscar nos últimos 3 segundos
        if remaining_time < self.rocket_blink_start_offset:
            if current_time - self.last_rocket_blink_time > self.rocket_blink_interval:
                self.rocket_blink_visible = not self.rocket_blink_visible
                self.last_rocket_blink_time = current_time

            # Aqui você pode adicionar efeitos visuais (como mudar a cor do ícone)
            if self.rocket_blink_visible:
                # Ícone normal
                pass
            else:
                # Ícone piscando (pode ser uma versão mais clara ou transparente)
                pass

    def _handle_movement(self, keys, dt):
        """Controla o movimento do carro"""
        if self.fuel <= 0:
            return

        # Velocidade base multiplicada por 60 para manter a mesma velocidade em 60 FPS
        speed_dt = self.speed * 60 * dt
        
        if keys[pygame.K_LEFT] and self.rect.x > self.left_limit:
            self.rect.x -= speed_dt
        if keys[pygame.K_RIGHT] and self.rect.x < self.right_limit:
            self.rect.x += speed_dt
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= speed_dt
        if keys[pygame.K_DOWN] and self.rect.y < self.screen_height - self.rect.height:
            self.rect.y += speed_dt

        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y
        )

    def _handle_rockets(self, keys, dt):
        """Controla o disparo de foguetes"""
        current_time = pygame.time.get_ticks()
        if (
            self.has_rocket
            and keys[pygame.K_SPACE]
            and current_time > self.rocket_cooldown
        ):

            self.fire_rocket()
            self.rocket_cooldown = current_time + 500  # 0.5s de cooldown

        # Atualiza foguetes existentes
        for rocket in self.rockets[:]:
            rocket.update(dt)
            if rocket.rect.bottom < 0:  # Remove se sair da tela
                self.rockets.remove(rocket)

    def _update_fuel(self, dt):
        """Atualiza o sistema de combustível"""
        if any([pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
            # Consumo multiplicado por 60 para manter a mesma taxa em 60 FPS
            self.fuel -= self.fuel_consumption_rate * 60 * dt
            self.fuel = max(0, self.fuel)  # Garante não ficar negativo

    def fire_rocket(self):
        """Dispara um novo foguete com sprite personalizada"""
        if hasattr(self, "game_manager") and hasattr(self.game_manager, "img_config"):
            # Usa a imagem do foguete do img_config
            original_img = self.game_manager.img_config.rocket_pickup_img
            # Redimensiona para o tamanho desejado
            rocket_img = pygame.transform.scale(original_img, (30, 60))
            # Rotaciona se necessário (90 graus para ficar vertical)
            rocket_img = pygame.transform.rotate(rocket_img, 0)
        else:
            # Fallback caso não tenha acesso ao game_manager
            rocket_img = None

        new_rocket = Rocket(self.rect.centerx, self.rect.top)

        # Atribui a imagem personalizada se disponível
        if rocket_img:
            new_rocket.image = rocket_img
            new_rocket.rect = new_rocket.image.get_rect(center=new_rocket.rect.center)

        self.rockets.append(new_rocket)

        # Toca o som do foguete
        if hasattr(self, "game_manager") and hasattr(self.game_manager, "rocket_sound"):
            self.game_manager.rocket_sound.play()

    def draw(self, screen):
        """
        Desenha o jogador e seus componentes na tela com a bazuca equipada
        """
        # 1. Desenha o carro base
        super().draw(screen)

        # 2. Desenha foguetes ativos
        for rocket in self.rockets[:]:  # Usando slice para segurança
            rocket.draw(screen)

        # 3. Desenha a bazuca no telhado (se equipada)
        self._draw_rocket_on_car(screen)

        # 4. Desenha o HUD (ícone + combustível)
        self._draw_hud_elements(screen)

    def _draw_rocket_on_car(self, screen):
        """Desenha a bazuca equipada no telhado do carro"""
        if not (self.has_rocket and self.rocket_on_car_img):
            return

        # Verifica visibilidade (para efeito de piscar)
        visible = not hasattr(self, "rocket_blink_visible") or self.rocket_blink_visible
        if not visible:
            return

        # Calcula a posição para colocar no telhado do carro
        rocket_x = self.rect.x + self.rocket_on_car_offset[0]
        rocket_y = self.rect.y + self.rocket_on_car_offset[1]

        # Aplica efeito visual se estiver perto de acabar
        if (
            hasattr(self, "last_rocket_blink_time")
            and pygame.time.get_ticks() - self.last_rocket_blink_time < 100
        ):
            # Cria uma cópia da imagem para aplicar transparência
            temp_img = self.rocket_on_car_img.copy()
            temp_img.set_alpha(180)  # Efeito de piscar
            screen.blit(temp_img, (rocket_x, rocket_y))
        else:
            screen.blit(self.rocket_on_car_img, (rocket_x, rocket_y))

    def _draw_hud_elements(self, screen):
        """Desenha todos os elementos do HUD"""
        # Ícone da bazuca
        if self.has_rocket and (
            not hasattr(self, "rocket_blink_visible") or self.rocket_blink_visible
        ):
            alpha = (
                128
                if hasattr(self, "rocket_blink_visible")
                and not self.rocket_blink_visible
                else 255
            )
            self.rocket_icon.set_alpha(alpha)
            screen.blit(self.rocket_icon, self.rocket_icon_pos)

        # Barra de combustível
        self._draw_fuel_bar(screen)

    def _draw_fuel_bar(self, screen):
        """Desenha a barra de combustível na HUD"""
        # Fundo da barra
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, self.max_fuel, 20))

        # Barra de preenchimento (muda de cor conforme o nível)
        fuel_width = max(0, self.fuel)  # Garante não ser negativo
        if self.fuel > 60:
            color = (0, 255, 0)  # Verde
        elif self.fuel > 30:
            color = (255, 255, 0)  # Amarelo
        else:
            color = (255, 0, 0)  # Vermelho

        pygame.draw.rect(screen, color, (10, 10, fuel_width, 20))

        # Borda
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, self.max_fuel, 20), 2)

    def add_fuel(self, amount):
        """Recarrega combustível"""
        self.fuel = min(self.max_fuel, self.fuel + amount)

    def reset_position(self):
        """Reseta a posição do jogador"""
        self.rect.x = self.screen_width // 2 - self.rect.width // 2
        self.rect.y = self.screen_height - self.rect.height - 20
        self.hitbox.set_rect(
            self.rect.width, self.rect.height, self.rect.x, self.rect.y
        )

    def load_sounds(self, acceleration_sound_path, idle_sound_path):
        """Carrega os sons do carro"""
        try:
            self.car_acceleration_sound = pygame.mixer.Sound(acceleration_sound_path)
            self.car_idle_sound = pygame.mixer.Sound(idle_sound_path)
            # Configura volume
            self.car_acceleration_sound.set_volume(0.6)
            self.car_idle_sound.set_volume(0.4)
        except Exception as e:
            print(f"Erro ao carregar sons do carro: {e}")
            # Cria sons dummy para evitar erros
            dummy_sound = pygame.mixer.Sound(buffer=bytearray(100))
            self.car_acceleration_sound = dummy_sound
            self.car_idle_sound = dummy_sound

    def activate_ghost_power(self, current_time, duration=8000):
        """Ativa o poder fantasma por um tempo determinado"""
        self.ghost_power_active = True
        self.ghost_power_end_time = current_time + duration

        # Aplica o efeito visual imediatamente
        if self.ghost_effect:
            self.ghost_effect.set_ghost_mode(True)

        # Toca o som do pickup
        if hasattr(self, "game_manager") and hasattr(
            self.game_manager, "ghost_pickup_sound"
        ):
            self.game_manager.ghost_pickup_sound.play()

    def update_ghost_power(self, current_time):
        """Atualiza o estado do poder fantasma"""
        if not self.ghost_power_active:
            return

        remaining_time = self.ghost_power_end_time - current_time

        if remaining_time <= 0:
            self.ghost_power_active = False
            if self.ghost_effect:
                self.ghost_effect.set_ghost_mode(False)
            return

        # Nos últimos 3 segundos, ativa piscar
        if self.ghost_effect:
            self.ghost_effect.is_blinking = remaining_time < self.blink_start_offset
            self.ghost_effect.update(current_time)