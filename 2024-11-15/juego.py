import cv2
import mediapipe as mp
import pygame
import sys
import random
import time
import os

# Inicializar Pygame
pygame.init()
screen_width, screen_height = 1200, 800  # Tamaño de la ventana más grande
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Control de Bola con Gestos")

# Configuración de la bola
ball_color = (255, 0, 0)
ball_radius = 20
ball_start_x, ball_start_y = screen_width // 2, 50
ball_x, ball_y = ball_start_x, ball_start_y

# Configuración de las líneas
line_color = (0, 0, 0)
line_thickness = 15
num_lines = 5
top_offset = 150
line_spacing = (screen_height - top_offset) // (num_lines + 1)
line_gap_width = 120

# Generar las posiciones iniciales de los huecos en cada línea
lines = []
for i in range(num_lines):
    gap_position = random.randint(50, screen_width - line_gap_width - 50)
    lines.append((top_offset + line_spacing * (i + 1), gap_position))

# Configurar mediapipe para detección de manos
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Variables para suavizar el movimiento
smoothing_factor = 0.2

# Estados del juego
state = "start"
start_time = None
final_time = 0

# Almacena el nombre del jugador y su foto
player_name = ""
captured_photo = None

# Archivos para el ranking y la carpeta para fotos
ranking_file = "ranking.txt"
photo_directory = "photos"

if not os.path.exists(photo_directory):
    os.makedirs(photo_directory)

# Función para mostrar texto en la pantalla, centrado
def display_text(text, size, color, y_offset=0):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 + y_offset))
    screen.blit(text_surface, text_rect)

# Función para capturar foto con cuenta regresiva
def capture_photo_with_countdown():
    global captured_photo
    countdown = 3  # Segundos de cuenta regresiva

    while countdown > 0:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_rgb)
        frame_surface = pygame.transform.rotate(pygame.transform.scale(frame_surface, (screen_width, screen_height)), 270)
        
        screen.blit(frame_surface, (0, 0))
        display_text(f"{countdown}", 120, (255, 0, 0), -200)  # Muestra el número de la cuenta regresiva
        pygame.display.flip()

        time.sleep(1)
        countdown -= 1

    # Capturar foto final
    ret, frame = cap.read()
    if ret:
        captured_photo = cv2.flip(frame, 1)  # Guardar la imagen como espejo

# Función para guardar el puntaje en el archivo de ranking
def save_score(name, time_score, photo_filename):
    try:
        with open(ranking_file, "a") as file:
            file.write(f"{name},{time_score:.2f},{photo_filename}\n")
    except Exception as e:
        print(f"Error al guardar el puntaje: {e}")

# Función para mostrar el ranking con fotos, centrado
def display_ranking():
    screen.fill((255, 255, 255))
    display_text("Ranking", 48, (0, 0, 0), -250)

    try:
        with open(ranking_file, "r") as file:
            lines = file.readlines()
            scores = []
            for line in lines:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) == 3:
                        name, score, photo_filename = parts
                        scores.append((name, float(score), photo_filename))
            scores = sorted(scores, key=lambda x: x[1])[:5]
    except Exception as e:
        print(f"Error al leer el archivo de ranking: {e}")
        scores = []

    y_offset = -150
    for i, (name, score, photo_filename) in enumerate(scores):
        text = f"{i + 1}. {name} - {score:.2f} segundos"
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(midleft=(100, screen_height // 2 + y_offset))
        screen.blit(text_surface, text_rect)

        try:
            photo_path = os.path.join(photo_directory, photo_filename)
            photo = pygame.image.load(photo_path)
            photo = pygame.transform.scale(photo, (80, 80))
            photo_rect = photo.get_rect(midright=(screen_width - 100, screen_height // 2 + y_offset))
            screen.blit(photo, photo_rect)
        except Exception as e:
            print(f"Error cargando la foto: {e}")

        y_offset += 120

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release()
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if state == "start":
                capture_photo_with_countdown()  # Captura la foto antes de iniciar el juego
                state = "playing"
                ball_x, ball_y = ball_start_x, ball_start_y
                start_time = time.time()
            elif state == "ranking" and event.key == pygame.K_RETURN:
                state = "start"

    if state == "start":
        screen.fill((255, 255, 255))
        display_text("Presiona cualquier tecla para comenzar", 48, (0, 0, 0))
        pygame.display.flip()
        continue
    elif state == "win":
        screen.fill((255, 255, 255))
        display_text("¡Ganaste!", 64, (0, 255, 0), -50)
        display_text(f"Tiempo: {final_time:.2f} segundos", 48, (0, 0, 0), 10)
        if captured_photo is not None:
            photo_surface = pygame.surfarray.make_surface(cv2.cvtColor(captured_photo, cv2.COLOR_BGR2RGB))
            photo_surface = pygame.transform.scale(photo_surface, (200, 200))
            screen.blit(photo_surface, (screen_width // 2 - 100, screen_height // 2 + 100))
        display_text("Presiona cualquier tecla para reiniciar", 48, (0, 0, 0), 200)
        pygame.display.flip()
        state = "ranking"
        continue
    elif state == "ranking":
        display_ranking()
        display_text("Presiona ENTER para volver al inicio", 36, (0, 0, 0), 200)
        pygame.display.flip()
        continue

    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
            wrist_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y
            target_x = int(wrist_x * screen_width)
            target_y = int(wrist_y * screen_height)
            ball_x += (target_x - ball_x) * smoothing_factor
            ball_y += (target_y - ball_y) * smoothing_factor

    screen.fill((255, 255, 255))
    for y, gap_x in lines:
        pygame.draw.line(screen, line_color, (0, y), (gap_x, y), line_thickness)
        pygame.draw.line(screen, line_color, (gap_x + line_gap_width, y), (screen_width, y), line_thickness)
        if (ball_y - ball_radius <= y <= ball_y + ball_radius) and not (gap_x <= ball_x <= gap_x + line_gap_width):
            state = "lose"

    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)
    if ball_y >= screen_height:
        final_time = time.time() - start_time
        state = "win"

    pygame.display.flip()

cap.release()
hands.close()
pygame.quit()
