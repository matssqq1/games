import pygame
import sys
import math
import random
import imageio


# Инициализация Pygame
pygame.init()

# Настройка окна
width, height = 1500, 900
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('game payton')

# Цвета
BLACK = (0, 0, 0)

# # Загрузка изображения игрока
# player_image = pygame.image.load('Pikachu Pixel Art.jpg')  # Замените на путь к вашему изображению
# player_image = pygame.transform.scale(player_image, (30, 30))  # Изменение размера изображения игрока

# гифт
gif = imageio.get_reader("tanks.gif")  # Замените на путь к вашему GIF
frames = [frame for frame in gif]  # Получаем все кадры GIF
frame_count = len(frames)  # Общее количество кадров
current_frame_index = 0  # Индекс текущего кадра

# Загрузка изображения пули
bullet_image = pygame.image.load('Pikachu Pixel Art.jpg')  # Замените на путь к вашему изображению пули
bullet_image = pygame.transform.scale(bullet_image, (10, 10))  # Изменение размера изображения пули

# Загрузка изображения врага
enemy_image = pygame.image.load('enemy.png')  # Замените на путь к изображению врага
enemy_image = pygame.transform.scale(enemy_image, (30, 30))  # Изменение размера изображения врага

# Позиция игрока
player_pos = [750, 450]
player_health = 100  # Здоровье игрока
   

# Пули
bullets = []
bullet_speed = 10

# Враги
enemies = []
enemy_speed = 0.5
enemy_spawn_timer = 0
enemy_hp = 3  # Здоровье врагов
enemy_damage = 10    # Урон, который наносит враг

player_x = player_pos[0]
player_y = player_pos[1]

def check_collisions(player_x, player_y, enemies): 
    global player_health  # Обратите внимание, что мы можем изменять глобальную переменную 
    for enemy in enemies: 
        enemy_x = enemy[0] # Координаты врага 
        enemy_y = enemy[1]   
        if player_x < enemy_x + 30 and player_x + 30 > enemy_x and player_y < enemy_y + 30 and player_y + 30 > enemy_y: 
            player_health -= enemy_damage  # Уменьшаем здоровье игрока при столкновении 
            print(f"Урон от врага! Текущее здоровье: {player_health}")
             
running = True 
score = 0 
kills = 0  # Счетчик убийств 
level = 1  # Текущий уровень 
kills_to_next_level = 10  # Количество убийств для повышения уровня 
enemy_hp_base = 3  # Базовое здоровье врагов 
enemy_damage_base = 10  # Базовый урон врагов 
 
def spawn_enemy(level): 
    edge = random.choice(['top', 'bottom', 'left', 'right'])  # Выбор стороны экрана для спауна 
    if edge == 'top': 
        enemy_x = random.randint(0, width - 30) 
        enemy_y = 0  # Враг появляется сверху 
    elif edge == 'bottom': 
        enemy_x = random.randint(0, width - 30) 
        enemy_y = height - 30  # Враг появляется снизу 
    elif edge == 'left': 
        enemy_x = 0  # Враг появляется слева 
        enemy_y = random.randint(0, height - 30) 
    else:  # edge == 'right' 
        enemy_x = width - 30  # Враг появляется справа 
        enemy_y = random.randint(0, height - 30) 
 
    enemy_hp = enemy_hp_base + (level - 1)  # Увеличение здоровья врагов с каждым уровнем 
    return [enemy_x, enemy_y, enemy_hp] 

while running:
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
        player_pos[0] -= 1
    if keys[pygame.K_d]:
        player_pos[0] += 1
    if keys[pygame.K_w]:
        player_pos[1] -= 1
    if keys[pygame.K_s]:
        player_pos[1] += 1

    # Ограничения игрока в пределах экрана
    player_pos[0] = max(0, min(player_pos[0], width - 30))
    player_pos[1] = max(0, min(player_pos[1], height - 30))

    # Обновление позиции пуль
    for bullet in bullets:
        bullet[0] += bullet[2] * bullet_speed
        bullet[1] += bullet[3] * bullet_speed

    bullets = [bullet for bullet in bullets if bullet[1] > 0 and bullet[0] > 0 and bullet[0] < width]

    # Создание врагов
    enemy_spawn_timer += 1
    if enemy_spawn_timer > 400:  # Интервал спавна врагов
        enemy_spawn_timer = 0
        enemies.append(spawn_enemy(level))  # Теперь не передаем координаты игрока

    # Обновление позиции врагов
    for enemy in enemies:
    # Вычисляем направление к игроку
        direction_x = player_pos[0] - enemy[0]
        direction_y = player_pos[1] - enemy[1]

        length = math.sqrt(direction_x ** 2 + direction_y ** 2)

        if length > 0:
            # Нормализуем направление
            direction_x /= length
            direction_y /= length

            # Передвигаем врага в сторону игрока
            enemy[0] += direction_x * enemy_speed
            enemy[1] += direction_y * enemy_speed

        # Ограничиваем передвижение врага в пределах экрана
        enemy[0] = max(0, min(enemy[0], width - 30))
        enemy[1] = max(0, min(enemy[1], height - 30))


    # Обработка столкновений и логика врагов
    for bullet in bullets:
        for enemy in enemies:
            if enemy[0] < bullet[0] < enemy[0] + 30 and enemy[1] < bullet[1] < enemy[1] + 30:
                enemy[2] -= 3  # Уменьшаем здоровье врага
                bullets.remove(bullet)
                if enemy[2] <= 0:
                    enemies.remove(enemy)
                    kills += 1
                    # Проверка на повышение уровня
                    if kills >= kills_to_next_level:
                        level += 1
                        kills = 0  # Сбрасываем счетчик убийств
    
    # Проверка на столкновения пуль и врагов
    for bullet in bullets:
        for enemy in enemies:
            if enemy[0] < bullet[0] < enemy[0] + 30 and enemy[1] < bullet[1] < enemy[1] + 30:  # Проверка на пересечение
                enemy[2] -= 3  # Уменьшаем HP врага
                bullets.remove(bullet)  # Удаляем пулю
                if enemy[2] <= 0:  # Если HP врага ниже или равно 0
                    enemies.remove(enemy)  # Удаляем врага

    if kills >= kills_to_next_level:
       level += 1  # Увеличиваем уровень
       kills_to_next_level += 10  # Увеличиваем количество убийств для следующего уровня
       print(f"Поздравляем! Вы достигли уровня {level}!")
   
    # Заливка фона цветомы
    screen.fill(BLACK)

    # Отображение пуль
    for bullet in bullets:
        screen.blit(bullet_image, (bullet[0], bullet[1]))

    # Отображение врагов
    for enemy in enemies:
        screen.blit(enemy_image, (enemy[0], enemy[1]))

    font = pygame.font.Font(None, 36)
    kills_text = font.render(f"Убийства: {kills}", True, (255, 255, 255))
    screen.blit(kills_text, (10, 10))

    level_text = font.render(f"Уровень: {level}", True, (255, 255, 255))  # Создание текста с текущим уровнем
    screen.blit(level_text, (10, 50))  # Отображение текста ниже счетчика убийств

    check_collisions(player_pos[0], player_pos[1], enemies)

    if player_health <= 0:
       print("Игра окончена!")
       running = False
       score = kills
    # Отображаем текущий кадр
    current_frame = frames[current_frame_index]
    current_frame = pygame.image.frombuffer(current_frame.tobytes(), current_frame.shape[1::-1], "RGBA")
    screen.blit(current_frame, (player_pos))  # Отображаем кадр по координатам (100, 100)
    
    # Обновляем индекс текущего кадра
    current_frame_index = (current_frame_index + 1) % frame_count
    
    # Обновление экранаwww
    pygame.display.flip()