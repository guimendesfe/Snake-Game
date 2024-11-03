
import pygame
import random

# Configurações iniciais do jogo
pygame.init()
pygame.display.set_caption("Snake Game")
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
square_size = 20
game_speed = 15
obstacles = []


# Função para gerar comida em uma posição aleatória que não colida com obstáculos
def generate_food():
    while True:
        food_x = round(random.randrange(0, width - square_size) / float(square_size)) * float(square_size)
        food_y = round(random.randrange(0, height - square_size) / float(square_size)) * float(square_size)
        if (food_x, food_y) not in obstacles:
            return food_x, food_y


# Função para desenhar a comida
def draw_food(size, food_x, food_y):
    pygame.draw.ellipse(screen, (255, 0, 0), [food_x, food_y, size, size])
    stem_width = size // 4
    stem_height = size // 3
    stem_x = food_x + size // 2 - stem_width // 2
    stem_y = food_y - stem_height
    pygame.draw.rect(screen, (139, 69, 19), [stem_x, stem_y, stem_width, stem_height])
    leaf_width = size // 3
    leaf_height = size // 4
    leaf_x = stem_x - stem_width
    leaf_y = stem_y + stem_height // 2 - leaf_height // 2
    pygame.draw.rect(screen, (0, 255, 0), [leaf_x, leaf_y, leaf_width, leaf_height])

# Função para desenhar a cobra
def draw_snake(size, pixels):
    for pixel in pixels:
        pygame.draw.rect(screen, (0, 255, 0), [pixel[0], pixel[1], size, size])
        dot_size = size // 4
        dot_x = pixel[0] + (size - dot_size) // 2
        dot_y = pixel[1] + (size - dot_size) // 2
        pygame.draw.rect(screen, (255, 255, 0), [dot_x, dot_y, dot_size, dot_size])

# Função para desenhar obstáculos
def draw_obstacles():
    for obs in obstacles:
        pygame.draw.rect(screen, (255, 0, 255), [obs[0], obs[1], square_size, square_size])

# Função para desenhar obstáculos
def draw_points(points):
    font = pygame.font.SysFont("Arial", 35)
    text = font.render(f"Points: {points}", True, (255, 255, 255))
    screen.blit(text, [1, 1])

# FFunção para selecionar a direção da cobra com as teclas de seta
def select_speed(key):
    if key == pygame.K_DOWN:
        return 0, square_size
    elif key == pygame.K_UP:
        return 0, -square_size
    elif key == pygame.K_RIGHT:
        return square_size, 0
    elif key == pygame.K_LEFT:
        return -square_size, 0
    else:
        return None, None

# Função para exibir o menu inicial
def show_menu():
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 50)
        title_text = font.render("Snake Game", True, (255, 255, 255))
        instruction_text = font.render("Press SPACE to Start", True, (255, 255, 255))
        exit_text = font.render("Press ESC to Exit", True, (255, 255, 255))

        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 50))
        screen.blit(instruction_text, (width // 2 - instruction_text.get_width() // 2, height // 2))
        screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 50))

        pygame.display.update()

        # Verifica os eventos para iniciar ou sair do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Função para exibir a tela de "Game Over"
def show_game_over(points):
    while True:
        screen.fill((0, 0, 0))
        font = pygame.font.SysFont("Arial", 50)
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        points_text = font.render(f"Your Score: {points}", True, (255, 255, 255))
        restart_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
        exit_text = font.render("Press ESC to Exit", True, (255, 255, 255))

        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 2 - 50))
        screen.blit(points_text, (width // 2 - points_text.get_width() // 2, height // 2))
        screen.blit(restart_text, (width // 2 - restart_text.get_width() // 2, height // 2 + 50))
        screen.blit(exit_text, (width // 2 - exit_text.get_width() // 2, height // 2 + 100))

        pygame.display.update()

        # Verifica se o jogador quer reiniciar ou sair do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# Função para mostrar uma mensagem de erro ao pressionar uma tecla inválida
def show_invalid_key_message():
    font = pygame.font.SysFont("Arial", 35)
    message = font.render("Invalid Key! Use Arrow Keys.", True, (255, 255, 0))
    screen.blit(message, (width // 2 - message.get_width() // 2, height // 2 + 150))
    pygame.display.update()
    pygame.time.delay(2000)

# Função para gerar um obstáculo a cada comida consumida
def generate_obstacles(num_obstacles):
    for _ in range(num_obstacles):
        obs_x = round(random.randrange(0, width - square_size) / float(square_size)) * float(square_size)
        obs_y = round(random.randrange(0, height - square_size) / float(square_size)) * float(square_size)
        obstacles.append((obs_x, obs_y))

# Função principal para iniciar e executar o jogo
def run_game():
    global game_speed, obstacles
    game_over = False
    game_speed = 15
    obstacles = []
    generate_obstacles(5)
    x = width / 2
    y = height / 2
    speed_x = 0
    speed_y = 0
    snake_size = 1
    pixels = []
    food_x, food_y = generate_food()

    # Looping principal do jogo.
    while not game_over:
        screen.fill((0, 0, 0))

        # Verifica as teclas pressionadas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                new_speed_x, new_speed_y = select_speed(event.key)
                if new_speed_x is None and new_speed_y is None:
                    show_invalid_key_message()
                else:
                    speed_x, speed_y = new_speed_x, new_speed_y


        draw_food(square_size, food_x, food_y) # Desenha a comida
        draw_obstacles() # Desenha os obstáculos

        # Detecta se a cobra saiu da tela
        if x < 0 or x >= width or y < 0 or y >= height:
            game_over = True

        # Atualiza a posição da cobra
        x += speed_x
        y += speed_y


        pixels.append([x, y]) # Adiciona o novo segmento da cobra
        if len(pixels) > snake_size: # Remove o último segmento se o tamanho da cobra for excedido
            del pixels[0]

        # Detecta se a cobra colidiu consigo mesma
        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                game_over = True

        # Detecta colisão com os obstáculos
        for obs in obstacles:
            if obs[0] == x and obs[1] == y:
                game_over = True


        draw_snake(square_size, pixels) # Desenha a cobra
        draw_points(snake_size - 1)  # Atualiza e exibe a pontuação

        pygame.display.update()

        # Verifica se a cobra comeu a comida
        if x == food_x and y == food_y:
            snake_size += 1 # Aumenta o tamanho da cobra
            food_x, food_y = generate_food() # Gera uma nova posição para a comida
            game_speed += 1 # Aumenta a velocidade do jogo
            generate_obstacles(1) # Gera um novo obstáculo

        clock.tick(game_speed)  # Define a velocidade do jogo

    show_game_over(snake_size - 1)  # Exibe a tela de "Game Over" com a pontuação final

# Exibe o menu inicial
show_menu()

# Loop principal para reiniciar o jogo após "Game Over"
while True:
    run_game()
    show_menu()
