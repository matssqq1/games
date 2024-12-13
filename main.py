import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Настройка окна
width, height = 1500, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('game payton')

# Цвета
BLACK = (0, 0, 0)

# Загрузка изображения игрока
player_image = pygame.image.load('Pikachu Pixel Art.jpg')  # Замените на путь к вашему изображению
player_image = pygame.transform.scale(player_image, (30, 30))  # Изменение размера изображения игрока

# Загрузка изображения пули
bullet_image = pygame.image.load('Pikachu Pixel Art.jpg')  # Замените на путь к вашему изображению пули
bullet_image = pygame.transform.scale(bullet_image, (10, 10))  # Изменение размера изображения пули

# Позиция игрока
player_pos = [750, 450]

# Пули
bullets = []
bullet_speed = 10

# Основной игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Проверка нажатия кнопки мыши
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                # Определяем направление выстрела
                mouse_x, mouse_y = pygame.mouse.get_pos()
                direction_x = mouse_x - (player_pos[0] + 15)  # Центр изображения
                direction_y = mouse_y - (player_pos[1] + 15)  # Центр изображения
                length = math.sqrt(direction_x ** 2 + direction_y ** 2)

                # Нормализация направления
                if length > 0:
                    direction_x /= length
                    direction_y /= length

                # Добавляем пулю
                bullets.append([player_pos[0] + 15, player_pos[1] + 15, direction_x, direction_y])  # Центрируем пулю

    keys = pygame.key.get_pressed()

    # Движения игрока (WASD управление)
    if keys[pygame.K_a]:
        player_pos[0] -= 5
    if keys[pygame.K_d]:
        player_pos[0] += 5
    if keys[pygame.K_w]:
        player_pos[1] -= 5
    if keys[pygame.K_s]:
        player_pos[1] += 5

    # Ограничения игрока в пределах экрана
    player_pos[0] = max(0, min(player_pos[0], width - 30))
    player_pos[1] = max(0, min(player_pos[1], height - 30))

    # Обновление позиции пуль
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed

    bullets = [bullet for bullet in bullets if bullet[1] > 0 and bullet[0] > 0 and bullet[0] < width]

    # Заливка фона цветом
    screen.fill(BLACK)

    # Отображение изображения игрока
    screen.blit(player_image, player_pos)

    # Отображение пуль
    for bullet in bullets:
        # Отображаем изображение пули
        screen.blit(bullet_image, (bullet[0], bullet[1]))

    # Обновление экрана
    pygame.display.flip()
