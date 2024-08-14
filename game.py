import pygame
import sys
import random

# Inicializar PyGame
pygame.init()

# Configurar las dimensiones de la ventana
screen_width = 1280  # Ancho de la ventana en píxeles
screen_height = 720  # Altura de la ventana en píxeles
# Crear la ventana con las dimensiones especificadas
screen = pygame.display.set_mode((screen_width, screen_height))
# Establecer el título de la ventana
pygame.display.set_caption("Nave Esquiva")

# Cargar las imágenes para el fondo, jugador y enemigo
background_image = pygame.image.load(
    "assets/background.jpg")  # Cargar la imagen de fondo
# Cargar la imagen del jugador (nave espacial)
player_image = pygame.image.load("assets/nave-espacial.png")
# Cargar la imagen del enemigo (asteroide)
enemy_image = pygame.image.load("assets/asteroide.png")

# Escalar las imágenes al tamaño adecuado
# Escalar la imagen de fondo para que cubra toda la ventana
background_image = pygame.transform.scale(
    background_image, (screen_width, screen_height))
# Escalar la imagen del jugador a un tamaño de 50x50 píxeles
player_image = pygame.transform.scale(player_image, (50, 50))
# Escalar la imagen del enemigo a un tamaño de 50x50 píxeles
enemy_image = pygame.transform.scale(enemy_image, (50, 50))

# Configuración inicial del jugador
player_x = 50  # Posición inicial en el eje X del jugador
# Posición inicial en el eje Y del jugador, centrada verticalmente
player_y = screen_height // 2 - player_image.get_height() // 2
player_speed = 5  # Velocidad de movimiento del jugador

# Configuración inicial de los enemigos
enemy_speed = 2  # Velocidad inicial de los enemigos
# Tiempo en milisegundos tras el cual se incrementará la velocidad de los enemigos
enemy_spawn_time = 10 * 1000
# Marca el tiempo de la última vez que se incrementó la velocidad de los enemigos
last_enemy_speed_increase = pygame.time.get_ticks()
enemies = []  # Lista que almacenará a todos los enemigos que aparecen en pantalla
# Probabilidad inicial de que un enemigo aparezca en cada frame
enemy_spawn_chance = 100

# Configuración del marcador de puntaje
score = 0  # Puntaje inicial del jugador
# Fuente utilizada para mostrar el puntaje en pantalla
font = pygame.font.Font(None, 36)
# Fuente utilizada para mostrar el mensaje de "Game Over"
game_over_font = pygame.font.Font(None, 74)


def spawn_enemy():
    """Función para crear y añadir un nuevo enemigo a la lista de enemigos."""
    # Se elige una posición aleatoria en el eje Y para el enemigo dentro de los límites de la pantalla
    enemy_y = random.randint(0, screen_height - enemy_image.get_height())
    # Se crea un diccionario que contiene la posición X, Y y la velocidad del enemigo
    enemy = {'x': screen_width, 'y': enemy_y, 'speed': enemy_speed}
    enemies.append(enemy)  # Añadir el enemigo creado a la lista de enemigos


def move_enemies():
    """Función para mover los enemigos de derecha a izquierda y aumentar el puntaje si salen de la pantalla."""
    global score
    # Se recorren todos los enemigos de la lista
    for enemy in enemies:
        # Se mueve el enemigo hacia la izquierda restando su velocidad a su posición X
        enemy['x'] -= enemy['speed']
        # Si el enemigo sale de la pantalla (es decir, su X es menor que el ancho de la imagen)
        if enemy['x'] < -enemy_image.get_width():
            enemies.remove(enemy)  # Se elimina el enemigo de la lista
            score += 1  # Se incrementa el puntaje del jugador


def check_collision(player_x, player_y, player_image, enemies):
    """Función para verificar si el jugador colisiona con algún enemigo."""
    # Se crea un rectángulo que representa la posición y tamaño del jugador
    player_rect = player_image.get_rect(topleft=(player_x, player_y))
    # Se recorren todos los enemigos para verificar si alguno colisiona con el jugador
    for enemy in enemies:
        # Se crea un rectángulo que representa la posición y tamaño del enemigo
        enemy_rect = enemy_image.get_rect(topleft=(enemy['x'], enemy['y']))
        # Se verifica si el rectángulo del jugador colisiona con el rectángulo de algún enemigo
        if player_rect.colliderect(enemy_rect):
            return True  # Si hay colisión, se retorna True
    return False  # Si no hay colisión, se retorna False


def main_menu():
    """Función que muestra el menú principal antes de iniciar el juego."""
    menu_running = True  # Bandera para controlar el bucle del menú
    while menu_running:
        screen.fill((0, 0, 0))  # Se llena la pantalla con color negro
        # Se define la fuente a utilizar para los textos del menú
        font = pygame.font.Font(None, 74)
        # Se renderiza el texto del título del juego
        title_text = font.render("Nave esquiva", True, (85, 107, 47))
        # Se coloca el texto en el centro horizontal y 1/3 de la altura de la pantalla
        screen.blit(title_text, (screen_width // 2 -
                    title_text.get_width() // 2, screen_height // 3))
        # Se renderiza el texto de inicio
        start_text = font.render(
            "Presiona ESPACIO para comenzar", True, (85, 107, 47))
        screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2,
                    screen_height // 2))  # Se coloca el texto en el centro de la pantalla

        for event in pygame.event.get():  # Se procesan todos los eventos
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()  # Se cierra PyGame
                sys.exit()  # Se cierra el programa
            if event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_SPACE:  # Si la tecla presionada es la barra espaciadora
                    menu_running = False  # Se sale del menú, lo que comienza el juego

        pygame.display.flip()  # Se actualiza la pantalla


def game_over():
    """Función que muestra la pantalla de game over cuando el jugador pierde."""
    global score
    game_over_running = True  # Bandera para controlar el bucle de la pantalla de game over
    while game_over_running:
        screen.fill((0, 0, 0))  # Se llena la pantalla con color negro
        # Se renderiza el texto de "Game Over"
        game_over_text = game_over_font.render(
            "Game Over", True, (85, 107, 47))
        # Se coloca el texto en el centro horizontal y 1/3 de la altura de la pantalla
        screen.blit(game_over_text, (screen_width // 2 -
                    game_over_text.get_width() // 2, screen_height // 3))
        # Se renderiza el puntaje del jugador
        score_text = font.render(
            f"Tu puntaje es: {score}", True, (85, 107, 47))
        # Se coloca el puntaje en el centro de la pantalla
        screen.blit(score_text, (screen_width // 2 -
                    score_text.get_width() // 2, screen_height // 2))
        # Se renderiza el texto de reinicio
        restart_text = font.render(
            "Presiona ESPACIO para jugar de nuevo", True, (85, 107, 47))
        # Se coloca el texto de reinicio en el centro horizontal y 2/3 de la altura de la pantalla
        screen.blit(restart_text, (screen_width // 2 -
                    restart_text.get_width() // 2, screen_height // 1.5))

        for event in pygame.event.get():  # Se procesan todos los eventos
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()  # Se cierra PyGame
                sys.exit()  # Se cierra el programa
            if event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_SPACE:  # Si la tecla presionada es la barra espaciadora
                    game_over_running = False  # Se sale de la pantalla de game over
                    reset_game()  # Se reinicia el juego

        pygame.display.flip()  # Se actualiza la pantalla


def reset_game():
    """Función que reinicia el juego a su estado inicial."""
    global player_x, player_y, enemy_speed, last_enemy_speed_increase, score, enemies, enemy_spawn_chance
    # Se restablecen todas las variables del juego a sus valores iniciales
    player_x = 50
    player_y = screen_height // 2 - player_image.get_height() // 2
    enemy_speed = 2
    last_enemy_speed_increase = pygame.time.get_ticks()
    enemies = []
    score = 0
    enemy_spawn_chance = 100
    game_loop()  # Se inicia el bucle principal del juego


def pause_menu():
    """Función que muestra el menú de pausa."""
    paused = True  # Bandera para controlar el bucle del menú de pausa
    # Se crea una superficie que almacena la pantalla actual
    blur_surface = pygame.Surface((screen_width, screen_height))
    blur_surface.blit(screen, (0, 0))
    # Se escala la superficie para crear un efecto de desenfoque
    blur_surface = pygame.transform.smoothscale(
        blur_surface, (screen_width // 10, screen_height // 10))
    blur_surface = pygame.transform.smoothscale(
        blur_surface, (screen_width, screen_height))

    while paused:
        # Se dibuja la superficie desenfocada en la pantalla
        screen.blit(blur_surface, (0, 0))
        # Se renderiza el texto de "PAUSA"
        pause_text = game_over_font.render("PAUSA", True, (85, 107, 47))
        screen.blit(pause_text, (screen_width // 2 - pause_text.get_width() // 2, screen_height //
                    2 - pause_text.get_height() // 2))  # Se coloca el texto en el centro de la pantalla

        for event in pygame.event.get():  # Se procesan todos los eventos
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()  # Se cierra PyGame
                sys.exit()  # Se cierra el programa
            if event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_ESCAPE:  # Si la tecla presionada es ESCAPE
                    paused = False  # Se sale del menú de pausa

        pygame.display.flip()  # Se actualiza la pantalla


def game_loop():
    """Función principal que maneja el bucle de juego."""
    global player_x, player_y, enemy_speed, last_enemy_speed_increase, enemy_spawn_chance
    running = True  # Bandera para controlar el bucle principal del juego
    # Reloj para controlar la tasa de fotogramas por segundo (FPS)
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():  # Se procesan todos los eventos
            if event.type == pygame.QUIT:  # Si se cierra la ventana
                pygame.quit()  # Se cierra PyGame
                sys.exit()  # Se cierra el programa
            if event.type == pygame.KEYDOWN:  # Si se presiona una tecla
                if event.key == pygame.K_ESCAPE:  # Si la tecla presionada es ESCAPE
                    pause_menu()  # Se muestra el menú de pausa

        # Manejo de la entrada del jugador
        keys = pygame.key.get_pressed()  # Se obtiene el estado de todas las teclas
        if keys[pygame.K_UP]:  # Si se mantiene presionada la tecla ARRIBA
            player_y -= player_speed  # Se mueve el jugador hacia arriba
        if keys[pygame.K_DOWN]:  # Si se mantiene presionada la tecla ABAJO
            player_y += player_speed  # Se mueve el jugador hacia abajo
        if keys[pygame.K_LEFT]:  # Si se mantiene presionada la tecla IZQUIERDA
            player_x -= player_speed  # Se mueve el jugador hacia la izquierda
        if keys[pygame.K_RIGHT]:  # Si se mantiene presionada la tecla DERECHA
            player_x += player_speed  # Se mueve el jugador hacia la derecha

        # Evitar que el jugador salga de los límites de la pantalla
        if player_x < 0:
            player_x = 0
        elif player_x > screen_width - player_image.get_width():
            player_x = screen_width - player_image.get_width()

        if player_y < 0:
            player_y = 0
        elif player_y > screen_height - player_image.get_height():
            player_y = screen_height - player_image.get_height()

        # Dibujar el fondo
        screen.blit(background_image, (0, 0))

        # Incrementar la velocidad de los enemigos a intervalos regulares
        if pygame.time.get_ticks() - last_enemy_speed_increase > enemy_spawn_time:
            enemy_speed += 1  # Incrementa la velocidad de los enemigos
            # Aumenta la probabilidad de aparición de enemigos
            enemy_spawn_chance = max(10, enemy_spawn_chance - 10)
            # Actualiza el tiempo del último incremento de velocidad
            last_enemy_speed_increase = pygame.time.get_ticks()

        # Generar nuevos enemigos con una cierta probabilidad
        if random.randint(0, enemy_spawn_chance) == 0:
            spawn_enemy()  # Llama a la función para crear un nuevo enemigo

        move_enemies()  # Llama a la función para mover todos los enemigos en pantalla

        # Dibujar al jugador
        screen.blit(player_image, (player_x, player_y))

        # Dibujar a los enemigos
        for enemy in enemies:
            screen.blit(enemy_image, (enemy['x'], enemy['y']))

        # Verificar colisiones entre el jugador y los enemigos
        if check_collision(player_x, player_y, player_image, enemies):
            running = False  # Termina el bucle de juego si hay una colisión
            game_over()  # Muestra la pantalla de game over

        # Dibujar el puntaje en pantalla
        score_text = font.render(f"Puntaje: {score}", True, (255, 255, 255))
        screen.blit(score_text, (screen_width -
                    score_text.get_width() - 10, 10))

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)  # Mantener una tasa de 60 FPS


# Iniciar el juego mostrando el menú principal
main_menu()
# Iniciar el bucle principal del juego
game_loop()
