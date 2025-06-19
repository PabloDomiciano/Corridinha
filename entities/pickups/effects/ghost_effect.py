import pygame

class GhostPickupEffect:
    def __init__(self, entity):
        """
        Gerencia apenas os efeitos visuais e de colisão do poder fantasma.
        
        Args:
            entity: Referência à entidade que receberá o efeito (deve ter:
                    - image (Surface)
                    - rect (Rect)
                    - [opcional] hitbox (Hitbox))
        """
        self.entity = entity

        # Estados do efeito
        self.is_ghost = False
        self.is_blinking = False
        self.blink_visible = True

        # Configurações de tempo
        self.blink_interval = 200  # ms entre piscadas
        self.last_blink_time = 0

        # Configurações visuais
        self.ghost_alpha = 128  # Transparência do modo fantasma

        # Prepara as variações de imagem
        self._prepare_images()

    def _prepare_images(self):
        """Prepara todas as variações de imagem necessárias."""
        self.normal_image = self.entity.image.copy()
        self.ghost_image = self._create_ghost_image()
        self.blank_image = self._create_blank_image()

    def _create_ghost_image(self):
        """Cria versão fantasma semi-transparente."""
        ghost_img = self.normal_image.copy()
        ghost_img.fill((255, 255, 255, self.ghost_alpha), 
                      special_flags=pygame.BLEND_RGBA_MULT)
        return ghost_img

    def _create_blank_image(self):
        """Cria imagem totalmente transparente."""
        blank = pygame.Surface((self.entity.rect.width, self.entity.rect.height), 
                             pygame.SRCALPHA)
        blank.fill((0, 0, 0, 0))
        return blank

    def set_ghost_mode(self, active, blinking=False):
        """
        Ativa/desativa o modo fantasma.
        
        Args:
            active: True para ativar o efeito fantasma
            blinking: True para ativar o efeito de piscar
        """
        self.is_ghost = active
        self.is_blinking = blinking
        self.blink_visible = True  # Reseta o estado

        # Aplica a imagem imediatamente
        if active:
            self.entity.image = self.ghost_image
        else:
            self.entity.image = self.normal_image

    def update(self, current_time):
        """
        Atualiza os efeitos visuais.
        Deve ser chamado a cada frame.
        """
        if self.is_blinking:
            self._update_blink(current_time)

    def _update_blink(self, current_time):
        """Gerencia a lógica do piscar."""
        if current_time - self.last_blink_time > self.blink_interval:
            self.blink_visible = not self.blink_visible
            self.last_blink_time = current_time

            # Alterna entre imagem fantasma/normal e transparente
            if self.blink_visible:
                self.entity.image = self.ghost_image if self.is_ghost else self.normal_image
            else:
                self.entity.image = self.blank_image

    def check_collision(self, other):
        """
        Verifica colisão, ignorando se estiver no modo fantasma.
        
        Args:
            other: Outra entidade para verificar colisão
            
        Returns:
            bool: True se houve colisão e não está no modo fantasma
        """
        if self.is_ghost:
            return False
            
        # Prioriza usar hitbox se disponível
        if hasattr(self.entity, 'hitbox') and hasattr(other, 'rect'):
            return self.entity.hitbox.check_rect_collision(other)
            
        # Fallback para colisão simples de rect
        return self.entity.rect.colliderect(other.rect)