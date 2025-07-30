import pygame
from entities.carro import Carro
from entities.rocket import Rocket

class Player(Carro):
    def __init__(self, image, screen_width, screen_height, x_pos, y_pos, rocket_icon=None):
        """
        Classe do jogador com sistema de movimento, combustível e armas
        
        Args:
            image: Surface do pygame com a imagem do carro
            screen_width: Largura da tela
            screen_height: Altura da tela
            x_pos: Posição X inicial
            y_pos: Posição Y inicial
            rocket_icon: Ícone para exibir quando tiver bazuca (opcional)
        """
        super().__init__(image, x_pos, y_pos)
        
        # Configurações da tela
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Configurações de movimento
        self.speed = 3
        self.left_limit = 100
        self.right_limit = self.screen_width - 100 - self.rect.width
        
        # Sistema de combustível
        self.max_fuel = 100
        self.fuel = self.max_fuel
        self.fuel_consumption_rate = 0.05
        

        # Sistema de foguetes/bazuca
        self.rockets = []
        self.rocket_cooldown = 0
        self.rocket_icon = self._validate_rocket_icon(rocket_icon)
        self.rocket_icon_pos = (10, 50)
        
        # Sistema de foguetes temporizado
        self.rocket_end_time = 0
        self.rocket_blink_start_offset = 3000  # Começa a piscar 3 segundos antes de acabar
        self.rocket_blink_interval = 200  # ms entre piscadas
        self.last_rocket_blink_time = 0
        self.rocket_blink_visible = True
        
        # Estado do jogo
        self.frozen = False
        self.hitbox.set_rect(self.rect.width, self.rect.height, self.rect.x, self.rect.y)

        
        # Estados de power-up
        self.has_rocket = False
        self.ghost_power_active = False
        self.ghost_power_end_time = 0
        self.blink_start_offset = 3000  # 3 segundos antes de começar a piscar
        
        # No método que coleta o pickup:
        self.has_rocket = True  # Para foguete

    def _validate_rocket_icon(self, icon):
        """Cria um ícone padrão se nenhum for fornecido"""
        if icon is None:
            # Cria um ícone de foguete simples
            icon = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.polygon(icon, (255, 200, 0), [(15, 0), (30, 30), (0, 30)])
            pygame.draw.rect(icon, (200, 200, 200), (12, 20, 6, 8))
        return icon

    def update(self, keys):
        """
        Atualiza o estado do jogador a cada frame
        
        Args:
            keys: Estado das teclas pressionadas
        """
        if self.frozen:
            return
        
        current_time = pygame.time.get_ticks()
        self._handle_movement(keys)
        self._handle_rockets(keys)
        self._update_fuel()
        self.update_rocket_power(current_time)  # Adicione esta linha

    def activate_rocket_power(self, current_time):
        """Ativa o poder do foguete por 10 segundos"""
        self.has_rocket = True  # Corrigi o typo aqui (era has_rocket)
        self.rocket_end_time = current_time + 10000  # 10 segundos
        self.rocket_blink_visible = True
        
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

    def _handle_movement(self, keys):
        """Controla o movimento do carro"""
        if self.fuel <= 0:
            return
            
        if keys[pygame.K_LEFT] and self.rect.x > self.left_limit:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < self.right_limit:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < self.screen_height - self.rect.height:
            self.rect.y += self.speed

        self.hitbox.set_rect(self.rect.width, self.rect.height, self.rect.x, self.rect.y)

    def _handle_rockets(self, keys):
        """Controla o disparo de foguetes"""
        current_time = pygame.time.get_ticks()
        if (self.has_rocket and 
            keys[pygame.K_SPACE] and 
            current_time > self.rocket_cooldown):
            
            self.fire_rocket()
            self.rocket_cooldown = current_time + 500  # 0.5s de cooldown
        
        # Atualiza foguetes existentes
        for rocket in self.rockets[:]:
            rocket.update()
            if rocket.rect.bottom < 0:  # Remove se sair da tela
                self.rockets.remove(rocket)

    def _update_fuel(self):
        """Atualiza o sistema de combustível"""
        if any([pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]):
            self.fuel -= self.fuel_consumption_rate
            self.fuel = max(0, self.fuel)  # Garante não ficar negativo

    def fire_rocket(self):
        """Dispara um novo foguete da posição atual do carro"""
        new_rocket = Rocket(self.rect.centerx, self.rect.top)
        self.rockets.append(new_rocket)

    def draw(self, screen):
        """
        Desenha o jogador e seus componentes na tela
        """
        super().draw(screen)
        
        # Desenha foguetes primeiro (para ficarem atrás do carro)
        for rocket in self.rockets:
            rocket.draw(screen)
        
        # Desenha ícone da bazuca apenas uma vez
        if self.has_rocket and (not hasattr(self, 'rocket_blink_visible') or self.rocket_blink_visible):
            screen.blit(self.rocket_icon, self.rocket_icon_pos)
            
        # Desenha barra de combustível
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
        self.hitbox.set_rect(self.rect.width, self.rect.height, self.rect.x, self.rect.y)