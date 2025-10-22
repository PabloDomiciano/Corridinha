import pygame
import random
import math
from entities.carro import Carro
from entities.hitbox import Hitbox


class EnemyCar(Carro):
    """
    Representa um carro inimigo com movimentos realistas.
    
    Responsabilidades:
    - Mover-se verticalmente para baixo (scrolling)
    - Oscilar lateralmente (movimento realista)
    - Trocar de faixa ocasionalmente
    - Evitar colisões com outros carros inimigos
    - Manter distância segura do jogador
    """
    
    def __init__(self, image, x_pos, screen_height, speed=3):
        # Adiciona variação de velocidade (70% a 130% da velocidade base)
        # Isso faz cada carro ter velocidade única, criando tráfego realista
        speed_variation = random.uniform(0.7, 1.3)
        varied_speed = speed * speed_variation
        
        # Inicializa carro acima da tela (y negativo)
        super().__init__(image, x_pos, y_pos=-image.get_height(), speed=varied_speed)
        
        self.screen_height = screen_height
        self.frozen = False  # Estado de congelamento (game over)
        
        # === MOVIMENTO LATERAL (OSCILAÇÃO) ===
        self.base_x = x_pos  # Posição central da faixa
        self.lateral_offset = 0  # Quanto deslocou para os lados
        self.max_lateral_movement = 25  # Limite máximo de desvio lateral
        
        # Parâmetros de oscilação (únicos para cada carro)
        self.oscillation_speed = random.uniform(0.015, 0.05)  # Velocidade da oscilação
        self.oscillation_amplitude = random.uniform(10, 30)  # Amplitude da oscilação
        self.time_offset = random.uniform(0, math.pi * 2)  # Fase inicial (para variar)
        self.time = 0  # Contador interno de tempo
        
        # Padrão de movimento (cada carro tem um estilo diferente)
        self.movement_pattern = random.choice([
            'sine',        # Movimento senoidal suave
            'slow_drift',  # Deriva lenta
            'subtle',      # Movimento quase imperceptível
            'aggressive',  # Zig-zag rápido
            'calm'         # Muito suave e previsível
        ])
        
        # Ajusta parâmetros baseado no padrão
        if self.movement_pattern == 'aggressive':
            self.oscillation_speed *= 1.5  # Mais rápido
            self.oscillation_amplitude *= 1.2  # Mais amplitude
        elif self.movement_pattern == 'calm':
            self.oscillation_speed *= 0.6  # Mais lento
            self.oscillation_amplitude *= 0.7  # Menos amplitude
        
        # === SISTEMA DE TROCA DE FAIXA ===
        self.available_lanes = [100, 220]  # Posições X das faixas
        self.is_changing_lane = False  # Se está trocando agora
        self.target_lane = None  # Faixa de destino (None = não está trocando)
        self.lane_change_speed = varied_speed * 0.8  # Velocidade da troca
        self.safe_distance_from_player = 150  # Distância mínima do jogador
        self.min_y_for_lane_change = 100  # Precisa estar abaixo dessa posição
        
        # Apenas 20% dos carros podem trocar de faixa
        self.can_change_lane = random.random() < 0.2
        if self.can_change_lane:
            # Define quando tentará trocar (aleatório entre 150-350 pixels)
            self.lane_change_trigger_y = random.randint(150, 350)
        
        # Inicializa hitbox para detecção de colisão
        self.hitbox = Hitbox()
        self.hitbox.set_rect(self.rect.width, self.rect.height, self.rect.x, self.rect.y)
    
    # === MÉTODO PRINCIPAL DE ATUALIZAÇÃO ===
    
    def update(self, player_rect=None, other_enemies=None, dt=1/60):
        """
        Atualiza o estado do carro inimigo.
        
        Args:
            player_rect: Rect do jogador (para evitar colisões)
            other_enemies: Lista de outros carros inimigos (para evitar colisões)
            dt: Delta time (tempo desde o último frame)
        """
        if not self.frozen:
            # Converte velocidade para delta time (mantém 60 FPS como base)
            speed_dt = self.speed * 60 * dt
            
            # Calcula nova posição vertical
            new_y = self.rect.y + speed_dt
            
            # Verifica colisão com outros carros antes de mover
            can_move = True
            if other_enemies:
                can_move = self._check_collision_with_enemies(new_y, other_enemies)
            
            # Só move se não houver colisão
            if can_move:
                self.rect.y = new_y
            else:
                # Se há colisão, reduz a velocidade para acompanhar o carro da frente
                # Ajusta para ficar a uma distância segura
                pass  # Mantém a posição atual (não avança)
            
            # Verifica se deve iniciar troca de faixa (passando a posição do player)
            self._check_lane_change(player_rect)
            
            # Se está trocando de faixa, executa a troca
            if self.is_changing_lane:
                self._perform_lane_change(dt)
            else:
                # Atualiza o movimento lateral baseado no padrão escolhido
                self._update_lateral_movement(dt)
            
            # Atualiza a posição x com o offset lateral
            self.rect.x = self.base_x + self.lateral_offset
            
            # Atualiza a hitbox
            self.hitbox.set_rect(
                self.rect.width, self.rect.height, self.rect.x, self.rect.y)
    
    def _check_collision_with_enemies(self, new_y, other_enemies):
        """Verifica se há colisão com outros carros inimigos na nova posição"""
        # Cria um rect temporário na nova posição para testar
        temp_rect = self.rect.copy()
        temp_rect.y = new_y
        
        # Distância mínima segura entre carros (em pixels)
        safe_distance = 20
        
        for enemy in other_enemies:
            # Não verifica colisão consigo mesmo
            if enemy is self:
                continue
            
            # Verifica se estão na mesma faixa (ou próximos horizontalmente)
            horizontal_overlap = abs(self.rect.centerx - enemy.rect.centerx) < 60
            
            if horizontal_overlap:
                # Calcula a distância vertical
                distance = enemy.rect.y - temp_rect.y
                
                # Se está muito perto de um carro à frente, não pode mover
                if 0 < distance < (self.rect.height + safe_distance):
                    return False  # Não pode mover
        
        return True  # Pode mover
    
    def _update_lateral_movement(self, dt):
        """Atualiza o movimento lateral do carro baseado no padrão escolhido"""
        # Multiplicamos a velocidade de oscilação por 60 para manter a mesma taxa em 60 FPS
        self.time += self.oscillation_speed * 60 * dt
        
        if self.movement_pattern == 'sine':
            # Movimento senoidal suave e constante
            self.lateral_offset = math.sin(self.time + self.time_offset) * self.oscillation_amplitude
            
        elif self.movement_pattern == 'slow_drift':
            # Movimento de deriva lenta (vai para um lado e volta devagar)
            self.lateral_offset = math.sin(self.time * 0.5 + self.time_offset) * self.oscillation_amplitude
            
        elif self.movement_pattern == 'subtle':
            # Movimento bem sutil (quase imperceptível)
            self.lateral_offset = math.sin(self.time + self.time_offset) * (self.oscillation_amplitude * 0.6)
        
        elif self.movement_pattern == 'aggressive':
            # Movimento agressivo e errático (zig-zag rápido)
            # Combina duas ondas senoidais de frequências diferentes
            wave1 = math.sin(self.time + self.time_offset) * self.oscillation_amplitude
            wave2 = math.sin(self.time * 2 + self.time_offset) * (self.oscillation_amplitude * 0.5)
            self.lateral_offset = wave1 + wave2
            
        elif self.movement_pattern == 'calm':
            # Movimento muito suave e previsível
            self.lateral_offset = math.sin(self.time * 0.3 + self.time_offset) * (self.oscillation_amplitude * 0.5)
        
        # Garante que não ultrapassa os limites
        self.lateral_offset = max(-self.max_lateral_movement, 
                                   min(self.max_lateral_movement, self.lateral_offset))
    
    def _check_lane_change(self, player_rect=None):
        """Verifica se deve iniciar uma troca de faixa"""
        # Só tenta trocar de faixa se:
        # 1. O carro tem permissão para trocar de faixa
        # 2. Não está atualmente trocando de faixa
        # 3. Passou da posição Y de trigger
        # 4. Está abaixo do mínimo Y necessário
        if (self.can_change_lane and 
            not self.is_changing_lane and 
            self.rect.y >= self.lane_change_trigger_y and
            self.rect.y >= self.min_y_for_lane_change):
            
            # NOVA VERIFICAÇÃO: Verifica distância segura do player
            if player_rect is not None:
                # Calcula distância vertical do player
                distance_from_player = abs(self.rect.y - player_rect.y)
                
                # Se estiver muito perto do player (menos de 150px), não troca de faixa
                if distance_from_player < self.safe_distance_from_player:
                    return  # Não troca de faixa se estiver muito perto
            
            # Escolhe uma faixa diferente da atual
            other_lanes = [lane for lane in self.available_lanes if lane != self.base_x]
            if other_lanes:
                self.target_lane = random.choice(other_lanes)
                self.is_changing_lane = True
                # Desabilita para não trocar novamente
                self.can_change_lane = False
    
    def _perform_lane_change(self, dt):
        """Executa a troca de faixa de forma suave"""
        if self.target_lane is None:
            self.is_changing_lane = False
            return
        
        # Calcula a diferença entre a posição atual e o alvo
        diff = self.target_lane - self.base_x
        
        # Velocidade de troca de faixa multiplicada por 60 para manter a mesma velocidade em 60 FPS
        speed_dt = self.lane_change_speed * 60 * dt
        
        # Move gradualmente em direção à faixa alvo
        if abs(diff) > speed_dt:
            # Ainda não chegou, continua movendo
            direction = 1 if diff > 0 else -1
            self.base_x += direction * speed_dt
        else:
            # Chegou na faixa alvo
            self.base_x = self.target_lane
            self.is_changing_lane = False
            self.target_lane = None
            # Reseta o offset lateral para a nova faixa
            self.lateral_offset = 0
            self.time = 0

    def off_screen(self, height):
        return self.rect.y > height

    def draw(self, surface):
        # Desenha o carro inimigo e sua hitbox
        surface.blit(self.image, self.rect)
        self.hitbox.draw_hitbox(surface)  # Desenha a hitbox do carro inimigo
