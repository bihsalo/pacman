from os import walk
import pygame

"""Настройка анимаций"""


def import_sprite(path):
    """
    Импортирует все изображения и возвращает список surfaces.

    Аргументы:
        path (str): Путь к папке, содержащей изображения.

    Возвращает:
        list: Список объектов `Surface` для каждого изображения в указанной папке.
    """
    surface_list = []
    for _, __, img_file in walk(path):
        for image in img_file:
            full_path = f"{path}/{image}"
            img_surface = pygame.image.load(full_path).convert_alpha()
            surface_list.append(img_surface)
    return surface_list