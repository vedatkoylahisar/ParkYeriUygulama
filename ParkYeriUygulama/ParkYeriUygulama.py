import pygame
import random
from collections import deque

# Pygame baþlat
pygame.init()

# Pencere boyutlarý ve hücre boyutu
cell_size = 50  # Hücre boyutunu büyüttük
rows, cols = 10, 10  # Daha büyük bir alan için satýr ve sütun sayýsýný artýrdýk
screen = pygame.display.set_mode((cols * cell_size, rows * cell_size + 50))  # Adým sayýsý için ekstra alan ekledik
pygame.display.set_caption("Park Yeri Bulma")


# Renkler
RED = (255, 0, 0)    # Dolu park yeri
GREEN = (0, 255, 0)  # Boþ park yeri
ORANGE = (255, 165, 0)  # Baþlangýç noktasý (Turuncu)
BLUE = (0, 0, 255)   # En yakýn park yeri
YELLOW = (255, 255, 0)  # Yol
WHITE = (255, 255, 255)  # Arka plan
LIGHT_BLUE = (173, 216, 230)  # Seçenekler için arka plan rengi
DARK_BLUE = (0, 0, 128)  # Buton rengi
HIGHLIGHT_BLUE = (0, 0, 255)  # Buton üzerine gelinceki renk
BLACK = (0, 0, 0)  # Metin rengi

# BFS ile en yakýn park yerini bulma fonksiyonu
def bfs(parking_lot, start_x, start_y, rows, cols):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Yukarý, Aþaðý, Sola, Saða yön tarifi
    queue = deque([(start_x, start_y)])
    visited = [[False] * cols for _ in range(rows)]
    visited[start_x][start_y] = True
    parent = { (start_x, start_y): None }  # Nereden geldiðini takip et

    while queue:
        x, y = queue.popleft()

        # Boþ park yeri bulundu
        if parking_lot[x][y] == 'B':
            # Hedef park yerine ulaþýldýðýnda yolun geri izlenmesi
            path = []
            while (x, y) != (start_x, start_y):
                path.append((x, y))
                x, y = parent[(x, y)]
            path.append((start_x, start_y))
            return path[::-1]  # Yolu ters çevir

        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and not visited[new_x][new_y]:
                visited[new_x][new_y] = True
                parent[(new_x, new_y)] = (x, y)
                queue.append((new_x, new_y))

    return None  # Eðer boþ park yeri bulunmazsa

# Rastgele park yeri matrisi oluþtur
def generate_random_parking_lot_with_empty_spots(rows, cols, num_empty_spots):
    grid = [['D' for _ in range(cols)] for _ in range(rows)]  # Tüm matrisin dolu (D) olduðu baþlangýç
    
    # Baþlangýç noktasýný rastgele yerleþtir
    start_x, start_y = random.randint(0, rows - 1), random.randint(0, cols - 1)
    grid[start_x][start_y] = 'S'
    
    # Verilen sayýda boþ park yeri (B) ekle
    empty_spots = random.sample([(i, j) for i in range(rows) for j in range(cols)], num_empty_spots)
    empty_spots = [spot for spot in empty_spots if spot != (start_x, start_y)]  # Baþlangýç noktasýna park yeri eklenmesin
    for x, y in empty_spots:
        grid[x][y] = 'B'
    
    return grid, (start_x, start_y)

# Park yeri matrisini görselleþtirme fonksiyonu
# Park yeri matrisini görselleþtirme fonksiyonu
def draw_grid(parking_lot, path=None, steps=0):
    screen.fill(WHITE)  # Arka planý temizle
    for i in range(rows):
        for j in range(cols):
            color = WHITE
            if parking_lot[i][j] == 'D':
                color = RED  # Dolu park yeri
            elif parking_lot[i][j] == 'B':
                color = GREEN  # Boþ park yeri
            elif parking_lot[i][j] == 'S':
                color = ORANGE  # Baþlangýç noktasý (Turuncu)

            # Hücreyi çiz
            pygame.draw.rect(screen, color, (j * cell_size, i * cell_size + 50, cell_size, cell_size))
            pygame.draw.rect(screen, BLACK, (j * cell_size, i * cell_size + 50, cell_size, cell_size), 2)  # Hücre kenarlýðý

    # Eðer yol varsa, yol hücrelerini sarýya boyama
    if path:
        for index, (x, y) in enumerate(path):
            # Baþlangýç noktasýný ve en yakýn park yerini ayrý renklerle iþaretle
            if index == 0:  # Baþlangýç noktasý
                pygame.draw.rect(screen, ORANGE, (y * cell_size, x * cell_size + 50, cell_size, cell_size))
            elif index == len(path) - 1:  # En yakýn park yeri
                pygame.draw.rect(screen, BLUE, (y * cell_size, x * cell_size + 50, cell_size, cell_size))
            else:  # Yol adýmlarý
                pygame.draw.rect(screen, YELLOW, (y * cell_size, x * cell_size + 50, cell_size, cell_size))

    # Adým sayýsýný yazdýr
    font = pygame.font.SysFont(None, 40)
    if(steps==0):
        steps_text = font.render(f"Adim Sayisi: BOS YER YOKTUR", True, BLACK)
    else:
      steps_text = font.render(f"Adim Sayisi: {steps - 1}", True, BLACK)
    screen.blit(steps_text, (10, 10))
    
    pygame.display.flip()



# Baþlangýç ekraný fonksiyonu
def start_screen():
    font = pygame.font.SysFont(None, 50)
    screen.fill(LIGHT_BLUE)
    
    # Baþlýk
    title_text = font.render("Park Yeri Bulma Similasyonu", True, BLACK)
    screen.blit(title_text, (cols * cell_size // 2 - title_text.get_width() // 2, 50))
    
    # Buton metinleri
    manual_text = font.render("Manuel Giris", True, WHITE)
    random_text = font.render("Rastgele Secim", True, WHITE)
    
    # Buton konumlarý
    manual_button = pygame.Rect(cols * cell_size // 2 - 150, 150, 300, 50)
    random_button = pygame.Rect(cols * cell_size // 2 - 150, 250, 300, 50)
    
    # Butonlarý çiz
    pygame.draw.rect(screen, DARK_BLUE, manual_button)
    pygame.draw.rect(screen, DARK_BLUE, random_button)
    screen.blit(manual_text, (manual_button.centerx - manual_text.get_width() // 2, manual_button.centery - manual_text.get_height() // 2))
    screen.blit(random_text, (random_button.centerx - random_text.get_width() // 2, random_button.centery - random_text.get_height() // 2))
    
    pygame.display.flip()
    
    # Buton týklama döngüsü
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if manual_button.collidepoint(mouse_pos):
                    return "manual"
                elif random_button.collidepoint(mouse_pos):
                    return "random"

# Manuel boþ alan sayýsý giriþi fonksiyonu
def get_manual_input():
    font = pygame.font.SysFont(None, 50)
    input_box = pygame.Rect(cols * cell_size // 2 - 150, 150, 300, 50)
    user_text = ""
    
    while True:
        screen.fill(LIGHT_BLUE)
        prompt_text = font.render("Bos alan sayisini girin:", True, BLACK)
        screen.blit(prompt_text, (cols * cell_size // 2 - prompt_text.get_width() // 2, 50))
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        
        # Girdi metnini çiz
        input_text = font.render(user_text, True, BLACK)
        screen.blit(input_text, (input_box.x + 10, input_box.y + 10))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter tuþuna basýldýðýnda
                    if user_text.isdigit():
                        return int(user_text)
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

# Ana fonksiyon
def main():
    # Baþlangýç ekranýný göster ve seçim yap
    user_choice = start_screen()
    
    if user_choice == "manual":
        num_empty_spots = get_manual_input()
    else:  # Rastgele seçim
        num_empty_spots = random.randint(1, 20)
    
    print(f"Secilen bos alan sayisi: {num_empty_spots}")
    
    # Rastgele bir park yeri matrisi oluþtur
    parking_lot, (start_x, start_y) = generate_random_parking_lot_with_empty_spots(rows, cols, num_empty_spots)
    
    print(f"Baslangic noktasi: ({start_x}, {start_y})")
    draw_grid(parking_lot)

    # En yakýn boþ park yerini bul ve adýmlarý görselleþtir
    path = bfs(parking_lot, start_x, start_y, rows, cols)
    if path:
        print("En yakin park yerine gitme yolu:")
        steps = 0
        for (x, y) in path:
            steps += 1
            print(f"({x}, {y})")
            draw_grid(parking_lot, path[:steps], steps)  # Her adýmda adým sayýsýný ve yolu güncelle
            pygame.time.delay(1000)  # Her adým arasýnda bekleme süresi
    else:
        print("Bos park yeri bulunamadi.")
    
    # Çýkýþ için bekleme
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
    pygame.quit()

if __name__ == "__main__":
    main()
