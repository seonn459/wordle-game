import pygame
import sys
import random

# Pygame'i başlatma
pygame.init()

# Ekran
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle")

# Font
font = pygame.font.SysFont("Arial", 36)

# Skor
score = 100

# Oyun sonucunun kontrolü
game_over = False
game_won = False

# İpucu değişkeni ve görseli
used_hints = []
hint_icon = pygame.image.load("hint.png")
hint_icon = pygame.transform.scale(hint_icon, (70, 70))

# Arka plan
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Renkler
white = (255, 255, 255)
black = (0, 0, 0)
gray = (200, 200, 200)
green = (83, 141, 78)
yellow = (181, 159, 59)
dark_gray = (120, 124, 126)
wrong_gray = (100, 100, 100)

# klavye arayüzü
key_colors = {}
öncelik = {
    wrong_gray: 0,
    dark_gray: 1,
    yellow: 2,
    green: 3
}
keyboard_rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]
key_size = 40
key_gap = 5
keyboard = []

# Türkçe karakter sözlüğü
turkce_karakterler = {
    "Ç": "C", "Ş": "S", "Ğ": "G",
    "Ü": "U", "İ": "I", "Ö": "O",
    "ç": "C", "ş": "S", "ğ": "G",
    "ü": "U", "ı": "I", "ö": "O"
}

# Arayüz ayarları
rows = 6
cols = 5
tile_size = 60
tile_gap = 10
üst_boşluk = 40
sol_boşluk = (WIDTH - (cols * tile_size + (cols - 1) * tile_gap)) // 2

# oyun durumu
kelime_listesi = ["YUNUS", "MESSI", "BALIK", "LAMBA", "AMPUL", "KABUK", "YOLCU", "YAZAR", "HATAY", "VALIZ",
                  "DOLAP", "BEYIN", "YEMEK", "BIÇAK", "KITAP", "ARMUT", "PERDE", "ONSOZ", "FIRIN", "BURUN"
                  ]
target_word = random.choice(kelime_listesi)
current_row = 0
current_guess = ""
guesses = []
colors = []

# FPS
clock = pygame.time.Clock()


# Tahmini değerlendiren fonksiyon
def evaluate_guess(guess, target):
    result = [wrong_gray] * cols
    target_temp = list(target)

    # 1. doğru yer ve harf
    for i in range(cols):
        if guess[i] == target[i]:
            result[i] = green
            target_temp[i] = None

    for i in range(cols):
        if result[i] == wrong_gray and guess[i] in target_temp:
            result[i] = yellow
            target_temp[target_temp.index(guess[i])] = None

    for i in range(cols):
        letter = guess[i]
        new_color = result[i]
        old_color = key_colors.get(letter, gray)
        if öncelik[new_color] > öncelik.get(old_color, -1):
            key_colors[letter] = new_color

    return result


# Arka planı çizen fonskiyon
def background_draw():
    screen.blit(background, (0, 0))


# Klavyeyi oluşturan fonksiyon
def create_keyboard():
    keyboard.clear()
    for row_idx, row in enumerate(keyboard_rows):
        y = 500 + row_idx * (key_size + key_gap)
        row_width = len(row) * (key_size + key_gap) - key_gap
        x_start = (WIDTH - row_width) // 2
        for col_idx, letter in enumerate(row):
            x = x_start + col_idx * (key_size + key_gap)
            rect = pygame.Rect(x, y, key_size, key_size)
            keyboard.append((letter, rect))


# Klavyeyi çizen fonskiyon
def draw_keyboard():
    for letter, rect in keyboard:
        bg = key_colors.get(letter, gray)
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, black, rect, 2)

        text = font.render(letter, True, black)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


# Satırları ve sütunları çizen ve harfleri gösteren fonksiyon
def draw_grid():
    for row in range(rows):
        for col in range(cols):
            x = sol_boşluk + col * (tile_size + tile_gap)
            y = üst_boşluk + row * (tile_size + tile_gap)
            pygame.draw.rect(screen, gray, (x, y, tile_size, tile_size), 2)

            # Arkaplan rengi
            if row < len(colors):
                bg_color = colors[row][col]
            else:
                bg_color = white

            pygame.draw.rect(screen, bg_color, (x, y, tile_size, tile_size))
            pygame.draw.rect(screen, gray, (x, y, tile_size, tile_size), 2)

            if row < len(guesses):
                letter = guesses[row][col]
            elif row == current_row and col < len(current_guess):
                letter = current_guess[col]
            elif row == current_row and any(i == col for i, _ in used_hints):
                letter = next(harf for i, harf in used_hints if i == col)
            else:
                letter = ""

            # İpucu olarak verilen harfin yeri
            if (col, target_word[col]) in used_hints and row == current_row:
                letter = target_word[col]

            if letter:
                text = font.render(letter.upper(), True, black)
                text_rect = text.get_rect(center=(x + tile_size // 2, y + tile_size // 2))
                screen.blit(text, text_rect)


# İpucu butonu
def draw_hint_button():
    hint_btn_rect = pygame.Rect(WIDTH - 60, 5, 50, 50)

    screen.blit(hint_icon, hint_btn_rect.topleft)


# Oyun döngüsü
run = True
create_keyboard()
while run:
    background_draw()
    # İpucu verilen harfleri tahmine yerleştirir
    for i, harf in used_hints:
        if len(current_guess) <= i:
            current_guess += " " * (i - len(current_guess))
            current_guess += harf
        else:
            current_guess = current_guess[:i] + harf + current_guess[i + 1:]

    for event in pygame.event.get():
        # Oyundan çıkış kontrolü
        if event.type == pygame.QUIT:
            run = False

        # Oyundaki klavye girdilerini kontrol eden kısım
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(current_guess) == cols and not game_over:
                    guesses.append(current_guess)
                    row_colors = evaluate_guess(current_guess, target_word)
                    colors.append(row_colors)

                    if current_guess == target_word:
                        game_over = True
                        game_won = True
                    elif current_row == rows - 1:
                        game_over = True

                    # Skoru güncelleyen satırlar
                    if not game_won:
                        if current_row >= 0:
                            score -= 10
                            score = max(score, 0)

                    current_guess = ""
                    current_row += 1
            elif event.key == pygame.K_BACKSPACE:
                if current_guess:
                    for i in reversed(range(len(current_guess))):
                        if all(hint_i != i for hint_i, _ in used_hints):
                            current_guess = current_guess[:i] + current_guess[i + 1:]
                            break
            elif event.unicode.isalpha():
                harf = turkce_karakterler.get(event.unicode, event.unicode).upper()

                for i in range(cols):
                    if any(hint_i == i for hint_i, _ in used_hints):
                        continue
                    if i >= len(current_guess):
                        current_guess += " " * (i - len(current_guess)) + harf
                        break
                    elif current_guess[i] == " ":
                        current_guess = current_guess[:i] + harf + current_guess[i + 1:]
                        break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            hint_btn_rect = pygame.Rect(WIDTH - 50, 5, 50, 50)
            if hint_btn_rect.collidepoint(mouse_pos) and not game_over:
                available_indices = [i for i, harf in enumerate(target_word) if (i, harf) not in used_hints]
                if available_indices and score >= 20:
                    index = random.choice(available_indices)
                    hint_letter = target_word[index]
                    used_hints.append((index, hint_letter))
                    score -= 20

            #Oyun sonu her şeyi sıfırlayan kısım
            if game_over:
                btn_rect = pygame.Rect(WIDTH // 2 - 100, 170, 200, 50)
                # Oyunu sıfırla
                if btn_rect.collidepoint(mouse_pos):
                    guesses.clear()
                    colors.clear()
                    key_colors.clear()
                    current_guess = ""
                    current_row = 0
                    game_over = False
                    game_won = False
                    score = 100
                    target_word = random.choice(kelime_listesi)
                    used_hints.clear()
            else:
                for letter, rect in keyboard:
                    if rect.collidepoint(mouse_pos):
                        if len(current_guess) < cols:
                            harf = turkce_karakterler.get(letter, letter)
                            current_guess += harf.upper()

    draw_grid()
    draw_keyboard()
    draw_hint_button()

    # Oyun sonucu ekrana yazan koşul
    if game_over:
        # Arka plan
        panel_width = 500
        panel_height = 260
        panel_x = (WIDTH - panel_width) // 2
        panel_y = 60

        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (230, 230, 230), panel_rect)
        pygame.draw.rect(screen, black, panel_rect, 3)
        if game_won:
            message = "Tebrikler! Cevap: {}".format(target_word)
        else:
            message = "Hakkınız Kalmadı!", "Cevap: {}".format(target_word)
        text = font.render(message, True, black)
        text_rect = text.get_rect(center=(WIDTH // 2, panel_y + 50))
        screen.blit(text, text_rect)

        # Skoru ekrana yazan satırlar
        # score_text = font.render("Puanınız: {}".format(score), True, black)
        # score_text_rect = score_text.get_rect(center=(WIDTH // 2, panel_y + 90))
        # screen.blit(score_text, score_text_rect)

        # Buton kısmı
        btn_width = 280
        btn_height = 70
        btn_x = (WIDTH - btn_width) // 2
        btn_y = panel_y + 130
        btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
        pygame.draw.rect(screen, gray, btn_rect)
        pygame.draw.rect(screen, black, btn_rect, 3)

        btn_text = font.render("Yeniden Başla", True, black)
        btn_text_rect = btn_text.get_rect(center=(btn_rect.center))
        screen.blit(btn_text, btn_text_rect)

    # Skoru güncel olarak gösteren satırlar
    score_display = font.render("Puanınız: {}".format(score), True, black)
    screen.blit(score_display, (5, 5))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
