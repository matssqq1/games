import pygame
import sys
from PIL import Image

# Функция для загрузки кадров GIF
def load_gif(filename):
    image = Image.open(filename)
    frames = []
    try:
        while True:
            frame = pygame.image.frombytes(image.tobytes(), image.size, image.mode)
            frames.append(frame)
            image.seek(len(frames))  # Перейти к следующему кадру
    except EOFError:
        pass  # Достигнут конец файла
    return frames

# Инициализация Pygame
pygame.init()

# Конфигурация экрана
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Отображение анимированного GIF в Pygame')

# Загрузка анимированного GIF
gif_frames = load_gif('tanks.gif')
frame_count = len(gif_frames)

# Основной цикл

clock = pygame.time.Clock()
current_frame = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Отображение текущего кадра
    screen.fill((255, 255, 255))  # Заполнение фона белым цветом
    screen.blit(gif_frames, current_frame, (0, 0))  # Вывод текущего кадра
    pygame.display.flip()  # Обновление экрана

    # Переход к следующему кадру
    current_frame = (current_frame + 1) % frame_count
    # clock.tick(10)  # Ограничение до 1 кадров в секунду

# Завершение Pygame
pygame.quit()
sys.exit()
