import os
import pygame

def load_explosion_images(folder_path):
    images = []
    for i in range(len(os.listdir(folder_path))):
        path = os.path.join(folder_path, f"explosion_{i}.png")
        image = pygame.image.load(path).convert_alpha()
        images.append(pygame.transform.scale(image, (64, 64)))  # ajuste o tamanho
    return images
