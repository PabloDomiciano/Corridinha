import pygame

class RocketEffect:
    def __init__(self, entity):
        """
        Gerencia os efeitos visuais e de colisão do poder foguete com duração limitada.

        Args:
            entity: Referência à entidade que receberá o efeito (deve ter:
                    - image (Surface)
                    - rect (Rect)
                    - [opcional] hitbox (Hitbox))
        """
        self.entity = entity

        # Estados do efeito
        self.is_rocket = False
        self.is_blinking = False
        self.blink_visible = True

        # Configurações de tempo
        self.rocket_duration = 10000  # 10 segundos em ms
        self.blink_start_time = 8000  # Piscar nos últimos 2 segundos
        self.blink_interval = 200     # ms entre piscadas
        self.rocket_start_time = 0
        self.last_blink_time = 0

        # Configurações visuais
        self.rocket_alpha = 128  # Transparência do modo foguete

        # Prepara as variações de imagem
        self._prepare_images()

    def _prepare_images(self):
        """Prepara todas as variações de imagem necessárias."""
        self.normal_image = self.entity.image.copy()
        self.rocket_image = self._create_rocket_image()
        self.blank_image = self._create_blank_image()

    def _create_rocket_image(self):
        """Cria versão foguete semi-transparente."""
        rocket_img = self.normal_image.copy()
        rocket_img.fill((255, 255, 255, self.rocket_alpha),
                        special_flags=pygame.BLEND_RGBA_MULT)
        return rocket_img

    def _create_blank_image(self):
        """Cria imagem totalmente transparente."""
        blank = pygame.Surface((self.entity.rect.width, self.entity.rect.height),
                              pygame.SRCALPHA)
        blank.fill((0, 0, 0, 0))
        return blank

    def activate(self, current_time):
        """
        Ativa o efeito foguete por tempo limitado.
        """
        self.is_rocket = True
        self.is_blinking = False
        self.blink_visible = True
        self.rocket_start_time = current_time
        self.last_blink_time = current_time
        self.entity.image = self.rocket_image

    def update(self, current_time):
        """
        Atualiza os efeitos visuais e controla o tempo do foguete.
        Deve ser chamado a cada frame.
        """
        if self.is_rocket:
            elapsed = current_time - self.rocket_start_time
            if elapsed >= self.rocket_duration:
                self.deactivate()
            elif elapsed >= self.blink_start_time:
                self.is_blinking = True
                self._update_blink(current_time)
            else:
                self.is_blinking = False
                self.entity.image = self.rocket_image

    def _update_blink(self, current_time):
        """Gerencia a lógica do piscar."""
        if current_time - self.last_blink_time > self.blink_interval:
            self.blink_visible = not self.blink_visible
            self.last_blink_time = current_time

            if self.blink_visible:
                self.entity.image = self.rocket_image
            else:
                self.entity.image = self.blank_image

    def deactivate(self):
        """
        Desativa o efeito foguete.
        """
        self.is_rocket = False
        self.is_blinking = False
        self.entity.image = self.normal_image

    def check_collision(self, other):
        """
        Verifica colisão, ignorando se estiver no modo foguete.

        Args:
            other: Outra entidade para verificar colisão

        Returns:
            bool: True se houve colisão e não está no modo foguete
        """
        if self.is_rocket:
            return False

        # Prioriza usar hitbox se disponível
        if hasattr(self.entity, 'hitbox') and hasattr(other, 'rect'):
            return self.entity.hitbox.check_rect_collision(other)

        # Fallback para colisão simples de rect
        return self.entity.rect.colliderect(other.rect)