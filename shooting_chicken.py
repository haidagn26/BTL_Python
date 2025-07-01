import math
import sqlite3

import pygame, sys, random
from pygame.locals import *

# Kích thước cửa sổ trò chơi
WINDOWWIDTH = 1500
WINDOWHEIGHT = 800

# Tốc độ trò chơi
SHIP_SPEED = 5
BULLET_SPEED = 7
CHICKEN_SPEED = 2
EGG_SPEED = 2

pygame.init()

# Cài đặt cửa sổ
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Bắn Gà')

# Load hình ảnh
SHIP_IMG = pygame.image.load('image\\phithuyen.png')
SHIP_IMG = pygame.transform.scale(SHIP_IMG, (100, 100))

CHICKEN_IMG = pygame.image.load('image\\chicken.png')
CHICKEN_IMG = pygame.transform.scale(CHICKEN_IMG, (50, 50))

# Load hình ảnh cho các quái mới (giả sử bạn có các file hình ảnh tương ứng)
MONSTER1_IMG = pygame.image.load('image\\sau.png')
MONSTER1_IMG = pygame.transform.scale(MONSTER1_IMG, (60, 60))

MONSTER2_IMG = pygame.image.load('image\\meo.png')
MONSTER2_IMG = pygame.transform.scale(MONSTER2_IMG, (80, 80))

MONSTER3_IMG = pygame.image.load('image\\cho.png')
MONSTER3_IMG = pygame.transform.scale(MONSTER3_IMG, (50, 50))

MONSTER4_IMG = pygame.image.load('image\\rong.png')
MONSTER4_IMG = pygame.transform.scale(MONSTER4_IMG, (100, 100))


# Điều chỉnh kích thước
BULLET_IMG = pygame.image.load('image\\laser.png')
EGG_IMG = pygame.image.load('image\\egg.png')
EGG_IMG = pygame.transform.scale(EGG_IMG, (10, 10))

BULLET1_IMG = pygame.image.load('image\\ss.png')  # Đạn cho Monster1
BULLET1_IMG = pygame.transform.scale(BULLET1_IMG, (12, 12))

BULLET2_IMG = pygame.image.load('image\\goi.png')  # Đạn cho Monster2
BULLET2_IMG = pygame.transform.scale(BULLET2_IMG, (15, 15))

BULLET3_IMG = pygame.image.load('image\\phancho.png')  # Đạn cho Monster3
BULLET3_IMG = pygame.transform.scale(BULLET3_IMG, (20, 20))

BULLET4_IMG = pygame.image.load('image\\lua.png')  # Đạn cho Monster4
BULLET4_IMG = pygame.transform.scale(BULLET4_IMG, (20, 20))

# Tải ảnh nền và chỉnh kích thước
BG_IMG = pygame.image.load("image\\bg2.jpg")  # Tải ảnh nền
BG_IMG = pygame.transform.scale(BG_IMG, (WINDOWWIDTH, WINDOWHEIGHT))  # Chỉnh kích thước thành 1500x800
BG_HEIGHT = BG_IMG.get_height()  # Lấy chiều cao mới (800)

BG_SCROLL_SPEED = 1  # Tốc độ cuộn


bg_y1 = 0
bg_y2 = -BG_HEIGHT  # Vị trí hình nền thứ hai ngay trên hình nền đầu tiên

def scroll_background():
    global bg_y1, bg_y2
    bg_y1 += BG_SCROLL_SPEED
    bg_y2 += BG_SCROLL_SPEED

    # Khi một nền di chuyển ra khỏi màn hình, đặt lại vị trí của nó
    if bg_y1 >= BG_HEIGHT:
        bg_y1 = bg_y2 - BG_HEIGHT
    if bg_y2 >= BG_HEIGHT :
        bg_y2 = bg_y1 - BG_HEIGHT

    # Vẽ nền lên màn hình
    DISPLAYSURF.blit(BG_IMG, (0, bg_y1))
    DISPLAYSURF.blit(BG_IMG, (0, bg_y2))


# Lớp phi thuyền
class Ship():
    def __init__(self):
        self.x = WINDOWWIDTH // 2
        self.y = WINDOWHEIGHT - 80
        self.width = SHIP_IMG.get_width()
        self.height = SHIP_IMG.get_height()
        self.bullets = []

    def draw(self):
        DISPLAYSURF.blit(SHIP_IMG, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw()

    def update(self):
        """Cập nhật vị trí phi thuyền theo chuột"""
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.x = mouse_x - self.width // 2
        self.y = mouse_y - self.height // 2

        # Giữ phi thuyền trong màn hình
        self.x = max(0, min(self.x, WINDOWWIDTH - self.width))
        self.y = max(0, min(self.y, WINDOWHEIGHT - self.height))

    def shoot(self):
        """Bắn đạn khi nhấn chuột"""
        bullet = Bullet(self.x + self.width // 2, self.y)  # Đạn xuất phát từ giữa phi thuyền
        self.bullets.append(bullet)


class Bullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET_IMG.get_width()
        self.height = BULLET_IMG.get_height()
        self.speed = BULLET_SPEED

    def draw(self):
        DISPLAYSURF.blit(BULLET_IMG, (self.x, self.y))

    def update(self):
        self.y -= self.speed

class Chicken:
    def __init__(self):
        self.x = random.randint(0, WINDOWWIDTH - CHICKEN_IMG.get_width())
        self.y = random.randint(50, 200)
        self.width = CHICKEN_IMG.get_width()
        self.height = CHICKEN_IMG.get_height()
        self.eggs = []
        self.speed = CHICKEN_SPEED
        self.direction = 1

    def draw(self):
        DISPLAYSURF.blit(CHICKEN_IMG, (self.x, self.y))
        for egg in self.eggs:
            egg.draw()

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WINDOWWIDTH - self.width:
            self.direction *= -1
        if random.randint(1, 1000) > 995:
            self.eggs.append(Egg(self.x + self.width // 2, self.y + self.height))  # Dùng Egg
        for egg in self.eggs:
            egg.update()

# Lớp Monster1
class Monster1:
    def __init__(self):
        self.x = random.randint(0, WINDOWWIDTH - MONSTER1_IMG.get_width())
        self.y = random.randint(50, 200)
        self.width = MONSTER1_IMG.get_width()
        self.height = MONSTER1_IMG.get_height()
        self.eggs = []
        self.speed = CHICKEN_SPEED + 2
        self.health = 2
        self.direction = 1

    def draw(self):
        DISPLAYSURF.blit(MONSTER1_IMG, (self.x, self.y))
        for egg in self.eggs:
            egg.draw()

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WINDOWWIDTH - self.width:
            self.direction *= -1
        if random.randint(1, 1000) > 990:
            self.eggs.append(Bullet1(self.x + self.width // 2, self.y + self.height))  # Dùng Bullet1
        for egg in self.eggs:
            egg.update()

# Lớp Monster2
class Monster2:
    def __init__(self):
        self.x = random.randint(0, WINDOWWIDTH - MONSTER2_IMG.get_width())
        self.y = random.randint(50, 200)
        self.width = MONSTER2_IMG.get_width()
        self.height = MONSTER2_IMG.get_height()
        self.eggs = []
        self.speed = CHICKEN_SPEED
        self.direction = 1
        self.health = 3

    def draw(self):
        DISPLAYSURF.blit(MONSTER2_IMG, (self.x, self.y))
        for egg in self.eggs:
            egg.draw()

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WINDOWWIDTH - self.width:
            self.direction *= -1
        if random.randint(1, 1000) > 995:
            self.eggs.append(Bullet2(self.x + self.width // 2, self.y + self.height))  # Dùng Bullet2
        for egg in self.eggs:
            egg.update()

# Lớp Monster3
class Monster3:
    def __init__(self):
        self.x = random.randint(0, WINDOWWIDTH - MONSTER3_IMG.get_width())
        self.y = random.randint(50, 200)
        self.width = MONSTER3_IMG.get_width()
        self.height = MONSTER3_IMG.get_height()
        self.eggs = []
        self.speed_x = CHICKEN_SPEED + 3
        self.speed_y = 1
        self.health = 4
        self.direction = 1

    def draw(self):
        DISPLAYSURF.blit(MONSTER3_IMG, (self.x, self.y))
        for egg in self.eggs:
            egg.draw()

    def update(self):
        self.x += self.speed_x * self.direction
        self.y += self.speed_y * math.sin(self.x / 50)
        if self.x <= 0 or self.x >= WINDOWWIDTH - self.width:
            self.direction *= -1
        if random.randint(1, 1000) > 995:
            self.eggs.append(Bullet3(self.x + self.width // 2, self.y + self.height))  # Dùng Bullet3
        for egg in self.eggs:
            egg.update()

# Lớp Monster4
class Monster4:
    def __init__(self):
        self.x = random.randint(0, WINDOWWIDTH - MONSTER4_IMG.get_width())
        self.y = random.randint(50, 200)
        self.width = MONSTER4_IMG.get_width()
        self.height = MONSTER4_IMG.get_height()
        self.eggs = []
        self.speed = CHICKEN_SPEED - 1
        self.direction = 1
        self.health = 10

    def draw(self):
        DISPLAYSURF.blit(MONSTER4_IMG, (self.x, self.y))
        for egg in self.eggs:
            egg.draw()

    def update(self):
        self.x += self.speed * self.direction
        if self.x <= 0 or self.x >= WINDOWWIDTH - self.width:
            self.direction *= -1
        if random.randint(1, 1000) > 985:
            self.eggs.append(Bullet4(self.x + self.width // 2, self.y + self.height))  # Dùng Bullet4
        for egg in self.eggs:
            egg.update()

# Lớp trứng
class Egg():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = EGG_IMG.get_width()
        self.height = EGG_IMG.get_height()

    def draw(self):
        DISPLAYSURF.blit(EGG_IMG, (self.x, self.y))

    def update(self):
        self.y += EGG_SPEED


# Lớp đạn cho Monster1 (nhanh hơn)
class Bullet1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET1_IMG.get_width()
        self.height = BULLET1_IMG.get_height()
        self.speed = EGG_SPEED + 2  # Nhanh hơn Egg

    def draw(self):
        DISPLAYSURF.blit(BULLET1_IMG, (self.x, self.y))

    def update(self):
        self.y += self.speed

# Lớp đạn cho Monster2 (to hơn)
class Bullet2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET2_IMG.get_width()
        self.height = BULLET2_IMG.get_height()
        self.speed = EGG_SPEED

    def draw(self):
        DISPLAYSURF.blit(BULLET2_IMG, (self.x, self.y))

    def update(self):
        self.y += self.speed

# Lớp đạn cho Monster3 (di chuyển zigzag)
class Bullet3:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET3_IMG.get_width()
        self.height = BULLET3_IMG.get_height()
        self.speed = EGG_SPEED + 1
        self.angle = 0  # Góc để di chuyển zigzag

    def draw(self):
        DISPLAYSURF.blit(BULLET3_IMG, (self.x, self.y))

    def update(self):
        self.y += self.speed
        self.x += math.sin(self.angle) * 2  # Di chuyển zigzag
        self.angle += 0.1

# Lớp đạn cho Monster4 (rơi chậm nhưng to)
class Bullet4:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = BULLET4_IMG.get_width()
        self.height = BULLET4_IMG.get_height()
        self.speed = EGG_SPEED - 1  # Chậm hơn Egg

    def draw(self):
        DISPLAYSURF.blit(BULLET4_IMG, (self.x, self.y))

    def update(self):
        self.y += self.speed

# Kiểm tra va chạm
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


def game_over(name, score):
    save_score(name, score)  # Lưu điểm vào database
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, (255, 0, 0))
    DISPLAYSURF.blit(text, (WINDOWWIDTH // 2 - 150, WINDOWHEIGHT // 2 - 50))
    pygame.display.update()

    pygame.time.delay(2000)
    main()  # Quay lại menu chính


def show_menu():
    font = pygame.font.Font(None, 50)
    menu_options = ["Play now", "View achievements", "Quit"]
    selected_option = 0  # Vị trí tùy chọn đang chọn

    while True:
        DISPLAYSURF.fill((0, 0, 0))  # Xóa màn hình
        title_text = font.render("SHOOTING CHICKEN", True, (255, 255, 0))
        DISPLAYSURF.blit(title_text, (WINDOWWIDTH // 2 - 100, 100))

        for i, option in enumerate(menu_options):
            color = (255, 255, 255) if i == selected_option else (150, 150, 150)
            text = font.render(option, True, color)
            DISPLAYSURF.blit(text, (WINDOWWIDTH // 2 - 100, 200 + i * 60))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                if event.key == K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                if event.key == K_RETURN:  # Nhấn Enter để chọn
                    if selected_option == 0:  # Chơi ngay
                        return "play"
                    elif selected_option == 1:  # Xem thành tích
                        return "scores"
                    elif selected_option == 2:  # Thoát
                        pygame.quit()
                        sys.exit()

def get_player_name():
    font = pygame.font.Font(None, 50)
    input_text = ""
    while True:
        DISPLAYSURF.fill((0, 0, 0))
        text = font.render("Enter your name: " + input_text, True, (255, 255, 255))
        DISPLAYSURF.blit(text, (WINDOWWIDTH // 2 - 150, 300))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RETURN and input_text:  # Enter để xác nhận
                    return input_text
                elif event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode


def init_db():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT, 
                  score INTEGER)''')
    conn.commit()
    conn.close()

def save_score(name, score):
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("INSERT INTO scores (name, score) VALUES (?, ?)", (name, score))
    conn.commit()
    conn.close()

def show_scores():
    conn = sqlite3.connect("scores.db")
    c = conn.cursor()
    c.execute("SELECT name, score FROM scores ORDER BY score DESC LIMIT 10")
    scores = c.fetchall()
    conn.close()

    font = pygame.font.Font(None, 50)
    while True:
        DISPLAYSURF.fill((0, 0, 0))
        title = font.render("Top 10 highest score ", True, (255, 255, 0))
        DISPLAYSURF.blit(title, (WINDOWWIDTH // 2 - 150, 100))

        for i, (name, score) in enumerate(scores):
            text = font.render(f"{i+1}. {name}: {score}", True, (255, 255, 255))
            DISPLAYSURF.blit(text, (WINDOWWIDTH // 2 - 200, 200 + i * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_RETURN:  # Nhấn Enter để quay lại menu
                return

def main():
    init_db()  # Khởi tạo database
    while True:
        option = show_menu()

        if option == "play":
            player_name = get_player_name()
            run_game(player_name)
        elif option == "scores":
            show_scores()

# Vòng lặp trò chơi
def run_game(player_name):
    ship = Ship()
    chickens = [Chicken()]  # Danh sách gà
    monsters1 = []  # Quái 1
    monsters2 = []  # Quái 2
    monsters3 = []  # Quái 3
    monsters4 = []  # Quái 4 (boss)
    running = True
    level = 1
    score = 0
    font = pygame.font.Font(None, 36)
    last_level_time = pygame.time.get_ticks()  # Thời gian để tăng level

    while running:
        DISPLAYSURF.fill((0, 0, 0))
        scroll_background()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                ship.shoot()

        # Cập nhật phi thuyền
        ship.update()
        ship.draw()

        # Cập nhật đạn
        for bullet in ship.bullets[:]:
            bullet.update()
        ship.bullets = [bullet for bullet in ship.bullets if bullet.y > 0]

        # Cập nhật và vẽ các loại quái
        for chicken in chickens[:]:
            chicken.eggs = [egg for egg in chicken.eggs if egg.y < WINDOWHEIGHT]
            chicken.update()
            chicken.draw()

        for monster in monsters1[:]:
            monster.eggs = [egg for egg in monster.eggs if egg.y < WINDOWHEIGHT]
            monster.update()
            monster.draw()

        for monster in monsters2[:]:
            monster.eggs = [egg for egg in monster.eggs if egg.y < WINDOWHEIGHT]
            monster.update()
            monster.draw()

        for monster in monsters3[:]:
            monster.eggs = [egg for egg in monster.eggs if egg.y < WINDOWHEIGHT]
            monster.update()
            monster.draw()

        for monster in monsters4[:]:
            monster.eggs = [egg for egg in monster.eggs if egg.y < WINDOWHEIGHT]
            monster.update()
            monster.draw()

        # Kiểm tra va chạm với đạn
        bullet_rects = [pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height) for bullet in ship.bullets[:]]
        for bullet, bullet_rect in zip(ship.bullets[:], bullet_rects):
            # Với gà
            for chicken in chickens[:]:
                chicken_rect = pygame.Rect(chicken.x, chicken.y, chicken.width, chicken.height)
                if check_collision(bullet_rect, chicken_rect):
                    if bullet in ship.bullets:
                        ship.bullets.remove(bullet)
                    if chicken in chickens:
                        chickens.remove(chicken)
                    score += 1

            for monster in monsters1[:]:
                monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
                if check_collision(bullet_rect, monster_rect):
                    if bullet in ship.bullets:
                        ship.bullets.remove(bullet)
                    monster.health -= 1
                    if monster.health <= 0 and monster in monsters1:
                        monsters1.remove(monster)
                        score += 2

            for monster in monsters2[:]:
                monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
                if check_collision(bullet_rect, monster_rect):
                    if bullet in ship.bullets:
                        ship.bullets.remove(bullet)
                    monster.health -= 1
                    if monster.health <= 0 and monster in monsters2:
                        monsters2.remove(monster)
                        score += 3

            for monster in monsters3[:]:
                monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
                if check_collision(bullet_rect, monster_rect):
                    if bullet in ship.bullets:
                        ship.bullets.remove(bullet)
                    monster.health -= 1
                    if monster.health <= 0 and monster in monsters3:
                        monsters3.remove(monster)
                        score += 4

            for monster in monsters4[:]:
                monster_rect = pygame.Rect(monster.x, monster.y, monster.width, monster.height)
                if check_collision(bullet_rect, monster_rect):
                    if bullet in ship.bullets:
                        ship.bullets.remove(bullet)
                    monster.health -= 1
                    if monster.health <= 0 and monster in monsters4:
                        monsters4.remove(monster)
                        score += 10

        # Kiểm tra va chạm phi thuyền với quái/trứng
        ship_rect = pygame.Rect(ship.x, ship.y, ship.width, ship.height)
        for enemies in [chickens, monsters1, monsters2, monsters3, monsters4]:
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.width, enemy.height)
                if check_collision(enemy_rect, ship_rect):
                    game_over(player_name, score)
                for egg in enemy.eggs:
                    egg_rect = pygame.Rect(egg.x, egg.y, egg.width, egg.height)
                    if check_collision(egg_rect, ship_rect):
                        game_over(player_name, score)

        # Tăng level mỗi 10 giây
        current_time = pygame.time.get_ticks()
        if current_time - last_level_time > 10000:  # Mỗi 10 giây tăng level
            level += 1
            last_level_time = current_time

        # Tạo thêm quái nếu tổng số quái nhỏ hơn level
        total_enemies = len(chickens) + len(monsters1) + len(monsters2) + len(monsters3) + len(monsters4)
        if total_enemies < level:
            if level <= 3:
                chickens.append(Chicken())
            elif level <= 6:
                monsters1.append(Monster1())
            elif level <= 9:
                monsters2.append(Monster2())
            elif level <= 12:
                monsters3.append(Monster3())
            else:
                monsters4.append(Monster4())

        # Hiển thị điểm và level
        score_text = font.render(f"Score: {score} | Level: {level}", True, (255, 255, 255))
        DISPLAYSURF.blit(score_text, (10, 10))

        pygame.display.update()
        pygame.time.Clock().tick(60)

if __name__ == '__main__':
    main()
