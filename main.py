import pygame
import os
import random
import sys
from levels_data import levels, Level

pygame.init()
WIDTH, HEIGHT = 480, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tile Match Trivia Game")
clock = pygame.time.Clock()

BG_FOLDER = "assets/backgrounds"
FOODS_FOLDER = "assets/foods"
SOUNDS_FOLDER = "assets/sounds"

WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
SKY_BLUE = (131, 200, 230)

font = pygame.font.SysFont("arial", 24)
large_font = pygame.font.SysFont("arial", 48)

pygame.mixer.music.load(os.path.join(SOUNDS_FOLDER, "background_music.mp3"))
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

tile_size = 70
cols, rows = 6, 3
y_start = 150
padding = 10
time_limit = 20

tile_images = {}
tiles = []
selected_tiles = []
matched_count = 0
start_ticks = 0
quiz_started = False
quiz_result = ""
game_over = False
final_scene = False
buttons = []
current_level_index = 0
background = None


class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-100, -10)
        self.size = random.randint(5, 10)
        self.color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)])
        self.speed = random.uniform(1, 3)

    def fall(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, WIDTH)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))


def load_tile_images():
    global tile_images
    files = os.listdir(FOODS_FOLDER)
    for file in files:
        if file.endswith(".png"):
            name = file[:-4]
            tile_images[name] = pygame.image.load(os.path.join(FOODS_FOLDER, file)).convert_alpha()


def create_tiles_for_level(tile_names):
    max_tiles = cols * rows
    max_types = max_tiles // 3
    if len(tile_names) > max_types:
        selected_tile_names = random.sample(tile_names, max_types)
    else:
        selected_tile_names = tile_names

    all_tiles = selected_tile_names * 3
    all_tiles = all_tiles[:max_tiles]
    random.shuffle(all_tiles)

    tiles_local = []
    positions = []
    total_width = cols * tile_size + (cols - 1) * padding
    x_margin_centered = (WIDTH - total_width) // 2

    for row in range(rows):
        for col in range(cols):
            x = x_margin_centered + col * (tile_size + padding)
            y = y_start + row * (tile_size + padding)
            positions.append((x, y))

    all_tiles = all_tiles[:len(positions)]
    for i, name in enumerate(all_tiles):
        rect = pygame.Rect(positions[i][0], positions[i][1], tile_size, tile_size)
        tiles_local.append({"name": name, "rect": rect, "selected": False, "matched": False})

    return tiles_local


def load_level(level: Level):
    global background, tiles, selected_tiles, matched_count, start_ticks
    global quiz_started, quiz_result, game_over, buttons, final_scene

    background = pygame.image.load(os.path.join(BG_FOLDER, level.bg_file))
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    tiles[:] = create_tiles_for_level(level.tile_names)
    selected_tiles.clear()
    matched_count = 0
    start_ticks = pygame.time.get_ticks()
    quiz_started = False
    quiz_result = ""
    game_over = False
    final_scene = False

    buttons = []
    btn_width, btn_height = 150, 50
    margin_x = 50
    margin_y = 600
    gap = 40
    for i, option in enumerate(level.options):
        x = margin_x + (i % 2) * (btn_width + gap)
        y = margin_y + (i // 2) * (btn_height + 20)
        buttons.append({"label": option, "rect": pygame.Rect(x, y, btn_width, btn_height)})


def draw_tile(tile, is_hovered=False):
    if tile["matched"]:
        return
    if tile["selected"]:
        color = (255, 255, 150)
    elif is_hovered:
        color = (200, 200, 255)
    else:
        color = WHITE

    pygame.draw.rect(screen, color, tile["rect"], border_radius=8)
    img = pygame.transform.scale(tile_images[tile["name"]], (tile_size - 10, tile_size - 10))
    screen.blit(img, (tile["rect"].x + 5, tile["rect"].y + 5))


def draw_selected_top():
    pygame.draw.rect(screen, SKY_BLUE, (20, 20, WIDTH - 40, 80), border_radius=10)

    for i, tile in enumerate(selected_tiles):
        img = pygame.transform.scale(tile_images[tile["name"]], (tile_size, tile_size))
        screen.blit(img, (30 + i * (tile_size + 10), 30))


def draw_game():
    screen.blit(background, (0, 0))

    for tile in tiles:
        if not tile["matched"]:
            draw_tile(tile)

    draw_selected_top()


    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(time_limit - seconds_passed))
    timer_text = font.render(f"Time left: {time_left}s", True, BLACK)
    screen.blit(timer_text, (30, 110))

    level_label = f"Level {current_level_index + 1}"
    level_text = pygame.font.SysFont("arial", 36, bold=True).render(level_label, True, BLACK)
    text_x = WIDTH - level_text.get_width() - 30
    screen.blit(level_text, (text_x, 25))

    mouse_pos = pygame.mouse.get_pos()

    for tile in tiles:
        if tile["matched"]:
            continue
        is_hovered = tile["rect"].collidepoint(mouse_pos)
        draw_tile(tile, is_hovered)

    if quiz_started:
        draw_quiz()

    if game_over and not quiz_started:
        screen.fill(BLACK)
        text = large_font.render("Game Over!", True, RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 100))

        again_rect = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2, 180, 50)
        pygame.draw.rect(screen, BLUE, again_rect, border_radius=10)
        label = font.render("Start Again", True, WHITE)
        screen.blit(label, (again_rect.x + 25, again_rect.y + 10))

        pygame.display.update()
        return again_rect

    pygame.display.update()
    return None


def draw_quiz():
    current_level = levels[current_level_index]
    question = font.render(current_level.question, True, WHITE)
    screen.blit(question, (50, 530))
    for btn in buttons:
        pygame.draw.rect(screen, GRAY, btn["rect"], border_radius=10)
        label = font.render(btn["label"], True, BLACK)
        screen.blit(label, (btn["rect"].x + 10, btn["rect"].y + 10))
    if quiz_result:
        result_color = GREEN if "Correct" in quiz_result else RED
        result_text = font.render(quiz_result, True, result_color)
        screen.blit(result_text, (50, 740))


def draw_restart_button():
    restart_rect = pygame.Rect(WIDTH - 100, HEIGHT - 50, 80, 35)
    pygame.draw.rect(screen, BLUE, restart_rect, border_radius=8)
    label = font.render("Restart", True, WHITE)
    screen.blit(label, (restart_rect.x + 5, restart_rect.y + 5))
    return restart_rect


def check_match():
    global matched_count
    if len(selected_tiles) < 3:
        return
    counts = {}
    for tile in selected_tiles:
        name = tile["name"]
        counts[name] = counts.get(name, 0) + 1
    for name, count in counts.items():
        if count == 3:
            match_group = [tile for tile in selected_tiles if tile["name"] == name][:3]
            for tile in match_group:
                tile["matched"] = True
                selected_tiles.remove(tile)
            matched_count += 3


def can_select(tile):
    for other in tiles:
        if other == tile or other["matched"]:
            continue
        if other["rect"].colliderect(tile["rect"]) and other["rect"].y < tile["rect"].y:
            return False
    return True


def reset_game():
    global current_level_index, final_scene
    current_level_index = 0
    final_scene = False
    load_level(levels[current_level_index])


load_tile_images()
load_level(levels[current_level_index])
confettis = [Confetti() for _ in range(100)]
running = True

while running:
    clock.tick(30)
    screen.fill(BLACK)

    seconds_passed = (pygame.time.get_ticks() - start_ticks) / 1000
    time_left = max(0, int(time_limit - seconds_passed))
    if time_left <= 0 and not quiz_started and not game_over:
        game_over = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if game_over and not quiz_started:
                again_rect = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2, 180, 50)
                if again_rect.collidepoint(pos):
                    reset_game()
                    continue
            if not quiz_started:
                for tile in tiles:
                    if tile["rect"].collidepoint(pos) and not tile["matched"]:
                        if tile["selected"]:
                            tile["selected"] = False
                            if tile in selected_tiles:
                                selected_tiles.remove(tile)
                        else:
                            if len(selected_tiles) < 3 and can_select(tile):
                                tile["selected"] = True
                                selected_tiles.append(tile)
                        check_match()
                        if matched_count == len(tiles):
                            quiz_started = True
                        break
            else:
                for btn in buttons:
                    if btn["rect"].collidepoint(pos):
                        current_level = levels[current_level_index]
                        if btn["label"] == current_level.correct_answer:
                            quiz_result = "Correct! 🎉"
                            pygame.display.update()
                            pygame.time.wait(1500)
                            current_level_index += 1
                            if current_level_index < len(levels):
                                load_level(levels[current_level_index])
                            else:
                                final_scene = True
                            quiz_started = False
                            selected_tiles.clear()
                            matched_count = 0
                        else:
                            quiz_result = "Wrong answer. Try again."

            if draw_restart_button().collidepoint(pos):
                reset_game()

    if final_scene:
        screen.fill(BLACK)
        for c in confettis:
            c.fall()
            c.draw(screen)
        text = large_font.render("Congratulations!", True, GOLD)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 200))
        subtext = font.render("You've completed all levels!", True, WHITE)
        screen.blit(subtext, (WIDTH // 2 - subtext.get_width() // 2, 280))
        pygame.display.update()
    else:
        draw_game()

pygame.quit()
sys.exit()
