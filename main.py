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
# Điều chỉnh kích thước
BULLET_IMG = pygame.image.load('image\\laser.png')
EGG_IMG = pygame.image.load('image\\egg.png')
EGG_IMG = pygame.transform.scale(EGG_IMG, (10, 10))

BG_IMG = pygame.image.load("image\\background (1).png")  # Tải ảnh nền
BG_HEIGHT = BG_IMG.get_height()
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


# Lớp đạn
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


# Lớp con gà
class Chicken():
    def __init__(self):
        self.x = random.randint(0, WINDOWWIDTH - CHICKEN_IMG.get_width())
        self.y = random.randint(50, 200)
        self.width = CHICKEN_IMG.get_width()
        self.height = CHICKEN_IMG.get_height()
        self.eggs = []
        self.speed = CHICKEN_SPEED
        self.direction = 1  # 1 là sang phải, -1 là sang trái

    def draw(self):
        DISPLAYSURF.blit(CHICKEN_IMG, (self.x, self.y))
        for egg in self.eggs:
            egg.draw()

    def update(self):
        """Di chuyển trái phải, đổi hướng khi chạm mép"""
        self.x += self.speed * self.direction

        if self.x <= 0 or self.x >= WINDOWWIDTH - self.width:
            self.direction *= -1  # Đổi hướng di chuyển

        if random.randint(1, 100) > 98:
            self.eggs.append(Egg(self.x + self.width // 2, self.y + self.height))

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


# Kiểm tra va chạm
def check_collision(rect1, rect2):
    return rect1.colliderect(rect2)


def game_over():
    """Hiển thị màn hình GAME OVER và cho phép chơi lại."""
    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, (255, 0, 0))
    text_rect = text.get_rect(center=(WINDOWWIDTH // 2, WINDOWHEIGHT // 2))

    DISPLAYSURF.blit(text, text_rect)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                waiting = False

    main()


# Vòng lặp trò chơi
def main():
    ship = Ship()
    chickens = [Chicken()]
    running = True
    move_left = move_right = False
    level = 1
    score = 0
    font = pygame.font.Font(None, 36)  # Font chữ
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    DISPLAYSURF.blit(score_text, (10, 10))
    last_spawn_time = pygame.time.get_ticks()

    while running:

        DISPLAYSURF.fill((0, 0, 0))
        scroll_background()  # Cập nhật vị trí và vẽ nền

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_left = True
                if event.key == K_RIGHT:
                    move_right = True
            if event.type == KEYUP:
                if event.key == K_LEFT:
                    move_left = False
                if event.key == K_RIGHT:
                    move_right = False
            if event.type == MOUSEBUTTONDOWN:
                ship.shoot()

        # Tạo thêm gà nếu số lượng hiện tại nhỏ hơn level
        if len(chickens) < level:
            new_chicken = Chicken()
            chickens.append(new_chicken)

            # Tăng level sau mỗi 10 giây
        if pygame.time.get_ticks() % 10000 < 16:
            level += 1


        ship.update()
        ship.draw()

        for bullet in ship.bullets[:]:
            bullet.update()

        # Xóa đạn khi ra khỏi màn hình
        ship.bullets = [bullet for bullet in ship.bullets if bullet.y > 0]

        # Xóa trứng khi rơi xuống dưới
        for chicken in chickens:
            chicken.eggs = [egg for egg in chicken.eggs if egg.y < WINDOWHEIGHT]
            chicken.update()
            chicken.draw()

        # Kiểm tra va chạm
        for bullet in ship.bullets[:]:  # Duyệt qua bản sao danh sách
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            for chicken in chickens[:]:  # Duyệt qua bản sao danh sách
                chicken_rect = pygame.Rect(chicken.x, chicken.y, chicken.width, chicken.height)
                if check_collision(bullet_rect, chicken_rect):
                    if bullet in ship.bullets:  # Kiểm tra xem đạn có trong danh sách không
                        ship.bullets.remove(bullet)  # Xóa đạn
                    if chicken in chickens:  # Kiểm tra xem gà có trong danh sách không
                        chickens.remove(chicken)  # Xóa gà
                    score += 1  # Tăng điểm

        for chicken in chickens:
            ship_rect = pygame.Rect(ship.x, ship.y, ship.height, ship.width)
            chicken_rect = pygame.Rect(chicken.x, chicken.y, chicken.width, chicken.height)
            if check_collision(chicken_rect, ship_rect):  # Nếu tàu chạm vào gà
                game_over()

            if chicken.eggs:  # Kiểm tra xem danh sách trứng có rỗng không
                for egg in chicken.eggs:
                    egg_rect = pygame.Rect(egg.x, egg.y, egg.width, egg.height)
                    if check_collision(egg_rect, ship_rect):
                        game_over()


        # Hiển thị điểm
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        DISPLAYSURF.blit(score_text, (10, 10))

        # Tăng số lượng gà theo thời gian
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time > 10000:  # Sau mỗi 10 giây
            level += 1
            last_spawn_time = current_time
            for _ in range(level):  # Thêm số lượng gà bằng level
                chickens.append(Chicken())


        pygame.display.update()
        pygame.time.Clock().tick(60)


if __name__ == '__main__':
    main()
